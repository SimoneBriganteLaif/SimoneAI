"""Confronta gli schema di due database PostgreSQL e produce un report delle differenze."""

import json
import os
import sys
from collections import defaultdict

import click
import psycopg2
from rich import print
from rich.table import Table
from rich.console import Console

console = Console()

# ---------------------------------------------------------------------------
# Credential resolution (same logic as transfer_data.py)
# ---------------------------------------------------------------------------

def _url_from_env(path: str, replace_host: bool = True) -> str:
    """Build a PostgreSQL URL from a .env file."""
    from dotenv import dotenv_values

    if not os.path.exists(path):
        raise ValueError(f"File .env non trovato: '{path}'")

    vals = dotenv_values(dotenv_path=path)
    required = ["DB_HOST", "DB_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]
    missing = [k for k in required if k not in vals]
    if missing:
        raise ValueError(f"Variabili mancanti nel .env: {missing}")

    host = vals["DB_HOST"]
    if replace_host and host == "db":
        host = "localhost"

    return (
        f"postgresql://{vals['POSTGRES_USER']}:{vals['POSTGRES_PASSWORD']}"
        f"@{host}:{vals['DB_PORT']}/{vals['POSTGRES_DB']}"
    )


def _url_from_arn(arn: str, profile: str | None = None) -> str:
    """Resolve an AWS Secrets Manager ARN to a PostgreSQL URL."""
    import boto3

    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    client = session.client("secretsmanager", region_name=arn.split(":")[3])
    secret = json.loads(client.get_secret_value(SecretId=arn)["SecretString"])

    return (
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
    )


def resolve_url(source: str, profile: str | None = None, replace_host: bool = True) -> str:
    if source.startswith("arn:aws:secretsmanager:"):
        return _url_from_arn(source, profile)
    elif source.startswith("postgresql://"):
        return source
    else:
        return _url_from_env(source, replace_host)


# ---------------------------------------------------------------------------
# Schema introspection
# ---------------------------------------------------------------------------

EXCLUDED_SCHEMAS = ("pg_catalog", "information_schema", "pg_toast")


def get_tables(conn) -> dict[str, list[str]]:
    """Return {schema: [table, ...]} for all user schemas."""
    sql = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN %s
        ORDER BY table_schema, table_name
    """
    with conn.cursor() as cur:
        cur.execute(sql, (EXCLUDED_SCHEMAS,))
        result: dict[str, list[str]] = defaultdict(list)
        for schema, table in cur:
            result[schema].append(table)
        return dict(result)


def get_columns(conn, schema: str, table: str) -> list[dict]:
    """Return column definitions for a table."""
    sql = """
        SELECT column_name, data_type, is_nullable, column_default,
               character_maximum_length, numeric_precision, numeric_scale
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(sql, (schema, table))
        return [
            {
                "name": r[0],
                "type": r[1],
                "nullable": r[2],
                "default": r[3],
                "max_length": r[4],
                "precision": r[5],
                "scale": r[6],
            }
            for r in cur
        ]


def get_table_stats(conn, schema: str, table: str) -> dict:
    """Return row count and estimated size for a table."""
    fqn = f'"{schema}"."{table}"'
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {fqn}")
        row_count = cur.fetchone()[0]
        cur.execute(f"SELECT pg_total_relation_size('{fqn}')")
        size_bytes = cur.fetchone()[0]
    return {"rows": row_count, "size_bytes": size_bytes}


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compare(src_conn, dest_conn) -> dict:
    """Compare schemas between source and destination databases."""
    src_tables = get_tables(src_conn)
    dest_tables = get_tables(dest_conn)

    src_fqn = {f"{s}.{t}" for s, tables in src_tables.items() for t in tables}
    dest_fqn = {f"{s}.{t}" for s, tables in dest_tables.items() for t in tables}

    only_source = sorted(src_fqn - dest_fqn)
    only_dest = sorted(dest_fqn - src_fqn)
    common = sorted(src_fqn & dest_fqn)

    diffs: list[dict] = []
    for fqn in common:
        schema, table = fqn.split(".", 1)
        src_cols = get_columns(src_conn, schema, table)
        dest_cols = get_columns(dest_conn, schema, table)

        src_map = {c["name"]: c for c in src_cols}
        dest_map = {c["name"]: c for c in dest_cols}

        table_diffs: list[str] = []

        # Columns only in source
        for col in sorted(set(src_map) - set(dest_map)):
            table_diffs.append(f"  + colonna '{col}' solo nel source ({src_map[col]['type']})")

        # Columns only in dest
        for col in sorted(set(dest_map) - set(src_map)):
            table_diffs.append(f"  - colonna '{col}' solo nella destination ({dest_map[col]['type']})")

        # Type mismatches
        for col in sorted(set(src_map) & set(dest_map)):
            s, d = src_map[col], dest_map[col]
            if s["type"] != d["type"]:
                table_diffs.append(f"  ~ colonna '{col}': tipo {s['type']} (src) vs {d['type']} (dest)")
            if s["nullable"] != d["nullable"]:
                table_diffs.append(f"  ~ colonna '{col}': nullable {s['nullable']} (src) vs {d['nullable']} (dest)")

        if table_diffs:
            diffs.append({"table": fqn, "issues": table_diffs})

    # Collect stats for source tables
    stats: list[dict] = []
    for fqn in sorted(src_fqn):
        schema, table = fqn.split(".", 1)
        try:
            s = get_table_stats(src_conn, schema, table)
            stats.append({"table": fqn, **s})
        except Exception as e:
            stats.append({"table": fqn, "rows": -1, "size_bytes": 0, "error": str(e)})

    return {
        "only_source": only_source,
        "only_dest": only_dest,
        "common_count": len(common),
        "diffs": diffs,
        "source_stats": stats,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _fmt_size(b: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if abs(b) < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024  # type: ignore
    return f"{b:.1f} TB"


def print_report(result: dict) -> None:
    """Print a human-readable comparison report."""
    # --- Schema diffs ---
    if result["diffs"]:
        console.rule("[bold red]Differenze di schema")
        for d in result["diffs"]:
            print(f"\n[bold]{d['table']}[/]")
            for issue in d["issues"]:
                print(issue)
    else:
        console.rule("[bold green]Schema allineati")
        print(f"Tutte le {result['common_count']} tabelle in comune hanno schema identico.\n")

    if result["only_source"]:
        console.rule("[yellow]Tabelle solo nel SOURCE")
        for t in result["only_source"]:
            print(f"  {t}")

    if result["only_dest"]:
        console.rule("[yellow]Tabelle solo nella DESTINATION")
        for t in result["only_dest"]:
            print(f"  {t}")

    # --- Source table stats ---
    console.rule("[bold]Tabelle source — dimensioni")

    # Group by schema
    by_schema: dict[str, list[dict]] = defaultdict(list)
    for s in result["source_stats"]:
        schema = s["table"].split(".")[0]
        by_schema[schema].append(s)

    for schema in sorted(by_schema):
        tables = by_schema[schema]
        total_rows = sum(t["rows"] for t in tables if t["rows"] >= 0)
        total_size = sum(t["size_bytes"] for t in tables)
        print(f"\n[bold]Schema: {schema}[/] ({len(tables)} tabelle, ~{total_rows:,} righe, ~{_fmt_size(total_size)})")

        tbl = Table(show_header=True, header_style="bold")
        tbl.add_column("Tabella", style="cyan")
        tbl.add_column("Righe", justify="right")
        tbl.add_column("Dimensione", justify="right")

        for t in sorted(tables, key=lambda x: x["table"]):
            rows_str = f"{t['rows']:,}" if t["rows"] >= 0 else "[red]errore[/]"
            tbl.add_row(t["table"], rows_str, _fmt_size(t["size_bytes"]))

        console.print(tbl)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.command()
@click.option("--source", "-s", required=True, help="Source: ARN, URL, o file .env")
@click.option("--destination", "-d", required=True, help="Destination: ARN, URL, o file .env")
@click.option("--src-profile", default=None, help="AWS profile per il source")
@click.option("--dest-profile", default=None, help="AWS profile per la destination")
@click.option("--no-replace-db-host", is_flag=True, default=False)
@click.option("--json-output", is_flag=True, default=False, help="Output JSON invece del report formattato")
def main(
    source: str,
    destination: str,
    src_profile: str | None,
    dest_profile: str | None,
    no_replace_db_host: bool,
    json_output: bool,
):
    """Confronta gli schema di due database PostgreSQL."""
    replace = not no_replace_db_host

    print("Connessione ai database... ", end="", flush=True)
    try:
        src_url = resolve_url(source, src_profile, replace)
        dest_url = resolve_url(destination, dest_profile, replace)
    except Exception as e:
        print(f"[red]Errore[/]: {e}")
        sys.exit(1)

    try:
        src_conn = psycopg2.connect(src_url)
        dest_conn = psycopg2.connect(dest_url)
    except Exception as e:
        print(f"[red]Errore connessione[/]: {e}")
        sys.exit(1)

    print("[green]OK[/]")

    try:
        result = compare(src_conn, dest_conn)
    finally:
        src_conn.close()
        dest_conn.close()

    if json_output:
        print(json.dumps(result, indent=2, default=str))
    else:
        print_report(result)

    # Exit code: 0 = no diffs, 1 = diffs found
    if result["diffs"] or result["only_source"] or result["only_dest"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
