"""
Trasferimento dati tra database PostgreSQL via pg_dump | psql.

Versione generalizzata (nessuna dipendenza da progetto specifico).
Supporta: ARN AWS Secrets Manager, URL diretti, file .env.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import defaultdict, deque
from fnmatch import fnmatch
from typing import Iterable, Sequence

import click
import psycopg2
from rich import print
from rich.prompt import Prompt
from rich.status import Status
from rich.table import Table
from rich.console import Console

console = Console()

# ---------------------------------------------------------------------------
# Credential resolution
# ---------------------------------------------------------------------------

def _url_from_env(path: str, replace_host: bool = True) -> str:
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
    import boto3

    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    client = session.client("secretsmanager", region_name=arn.split(":")[3])
    secret = json.loads(client.get_secret_value(SecretId=arn)["SecretString"])

    return (
        f"postgresql://{secret['username']}:{secret['password']}"
        f"@{secret['host']}:{secret['port']}/{secret['dbname']}"
    )


def resolve_url(
    source: str, profile: str | None = None, replace_host: bool = True
) -> str:
    if source.startswith("arn:aws:secretsmanager:"):
        return _url_from_arn(source, profile)
    elif source.startswith("postgresql://"):
        return source
    else:
        return _url_from_env(source, replace_host)


# ---------------------------------------------------------------------------
# Table discovery & FK ordering
# ---------------------------------------------------------------------------

EXCLUDED_SCHEMAS = ("pg_catalog", "information_schema", "pg_toast")


def list_tables(conn) -> list[str]:
    sql = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN %s
        ORDER BY table_schema, table_name
    """
    with conn.cursor() as cur:
        cur.execute(sql, (EXCLUDED_SCHEMAS,))
        return [f"{r[0]}.{r[1]}" for r in cur]


def expand_tables(conn, patterns: Sequence[str]) -> list[str]:
    tables = list_tables(conn)
    selected: set[str] = set()
    for p in patterns:
        matched = [t for t in tables if fnmatch(t, p)]
        if not matched:
            print(f"[yellow]⚠ Pattern '{p}' non corrisponde a nessuna tabella[/]", file=sys.stderr)
        selected.update(matched)
    if not selected:
        raise SystemExit("Nessuna tabella corrisponde ai pattern forniti")
    return sorted(selected)


def get_foreign_keys(conn) -> list[tuple[str, str]]:
    sql = """
        SELECT
            ccu.table_schema, ccu.table_name,
            tc.table_schema, tc.table_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
             ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema   = kcu.table_schema
        JOIN information_schema.constraint_column_usage ccu
             ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        return [(f"{r[0]}.{r[1]}", f"{r[2]}.{r[3]}") for r in cur.fetchall()]


def build_graph(
    edges: Sequence[tuple[str, str]], all_nodes: Iterable[str]
) -> tuple[dict[str, set[str]], set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set(all_nodes)
    for parent, child in edges:
        if parent != child:  # skip self-references
            graph[parent].add(child)
            nodes.update([parent, child])
    return graph, nodes


def filter_graph(
    graph: dict[str, set[str]], nodes: set[str], selected: Iterable[str]
) -> tuple[dict[str, set[str]], set[str]]:
    sel = set(selected)
    filtered: dict[str, set[str]] = defaultdict(set)
    for u in sel:
        for v in graph.get(u, ()):
            if v in sel:
                filtered[u].add(v)
    return filtered, sel


def topo_sort(graph: dict[str, set[str]], nodes: set[str]) -> list[str]:
    indegree = {n: 0 for n in nodes}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque(n for n, d in indegree.items() if d == 0)
    order: list[str] = []
    while queue:
        n = queue.popleft()
        order.append(n)
        for m in graph.get(n, ()):
            indegree[m] -= 1
            if indegree[m] == 0:
                queue.append(m)

    if len(order) != len(nodes):
        cyclic = sorted(nodes - set(order))
        print(f"[yellow]⚠️  Ciclo FK rilevato tra {len(cyclic)} tabelle — verranno aggiunte in fondo.[/]")
        print(f"[yellow]   I constraint FK verranno disabilitati durante la copia.[/]")
        order.extend(cyclic)
    return order


def resolve_table_order(conn, table_patterns: Sequence[str]) -> list[str]:
    """Expand patterns and sort by FK dependencies."""
    tables = expand_tables(conn, table_patterns)
    edges = get_foreign_keys(conn)
    graph, nodes = build_graph(edges, tables)
    graph, nodes = filter_graph(graph, nodes, tables)
    return topo_sort(graph, nodes)


# ---------------------------------------------------------------------------
# Data operations
# ---------------------------------------------------------------------------

def count_entries(db_url: str, table: str) -> int:
    cmd = f"psql --dbname={db_url} --tuples-only -c 'SELECT COUNT(*) FROM {table};'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'Errore conteggio "{table}": {result.stderr.strip()}')
    return int(result.stdout.strip())


def print_table_counts(db_url: str, tables: list[str], label: str = "") -> None:
    if label:
        print(f"\n[bold]{label}[/]")
    max_len = max(len(t) for t in tables) if tables else 0
    for table in tables:
        try:
            count = count_entries(db_url, table)
            print(f"    {table:<{max_len}}  {count:>10,} righe")
        except RuntimeError as e:
            print(f"    {table:<{max_len}}  [red]errore[/]")


def dest_existing_tables(dest_url: str) -> set[str]:
    """Return set of schema-qualified table names that exist in the destination DB."""
    conn = psycopg2.connect(dest_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_schema, table_name FROM information_schema.tables "
                "WHERE table_type = 'BASE TABLE' AND table_schema NOT IN %s",
                (EXCLUDED_SCHEMAS,),
            )
            return {f"{r[0]}.{r[1]}" for r in cur}
    finally:
        conn.close()


def truncate_tables(db_url: str, tables: list[str], existing: set[str]) -> None:
    for table in tables:
        if table not in existing:
            print(f'  [dim]"{table}" non esiste nella destination, skip[/]')
            continue

        try:
            count = count_entries(db_url, table)
        except RuntimeError:
            count = -1

        if count == 0:
            print(f'  [dim]"{table}" già vuota, skip[/]')
            continue

        print(f'  Truncate "{table}"...', end=" ")
        cmd = f"psql --dbname={db_url} -c 'TRUNCATE TABLE {table} CASCADE;'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[red]errore[/]: {result.stderr.strip()}")
        else:
            print("[green]OK[/]")


def copy_tables(
    src_url: str, dest_url: str, tables: list[str],
    existing: set[str], status: Status | None = None,
    disable_fk: bool = False,
) -> list[str]:
    errors: list[str] = []
    fk_prefix = b"SET session_replication_role = 'replica';\n" if disable_fk else b""

    for table in tables:
        # Count source entries
        try:
            entry_count = count_entries(src_url, table)
        except RuntimeError:
            entry_count = -1

        # If table doesn't exist in destination, include DDL (no --data-only)
        data_only = "--data-only" if table in existing else ""
        mode_label = "" if table in existing else " [cyan][+schema][/]"

        count_str = f"{entry_count:,}" if entry_count >= 0 else "?"
        if status:
            status.update(f'[bold]Copia [green]"{table}"[/] ({count_str} righe){mode_label}')
        else:
            print(f'Copia "{table}" ({count_str} righe){mode_label}...')

        pg_dump = subprocess.Popen(
            f'pg_dump --no-owner --table="{table}" {data_only} --dbname="{src_url}"',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        psql_proc = subprocess.Popen(
            f'psql --dbname="{dest_url}"',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        dump_out, dump_err = pg_dump.communicate()
        psql_out, psql_err = psql_proc.communicate(fk_prefix + dump_out)

        if pg_dump.returncode != 0 or psql_proc.returncode != 0:
            msg = f'Errore su "{table}"'
            if pg_dump.returncode != 0:
                msg += f"\n  [pg_dump] {dump_err.decode().strip()}"
            if psql_proc.returncode != 0:
                msg += f"\n  [psql]    {psql_err.decode().strip()}"
            errors.append(msg)
            print(f"  ❌ {table}")
        elif len(psql_out.decode().strip()) == 0 and entry_count > 0:
            warning = f"⚠️ Output psql vuoto per {table} ({count_str} righe nel source)"
            errors.append(warning)
            print(f"  ⚠️  {table}")
        else:
            print(f"  ✅ {table}")

    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.command()
@click.argument("source")
@click.argument("destination")
@click.option(
    "--tables", "-t", multiple=True,
    help="Pattern tabelle da trasferire (es. 'template.*', 'prs.users'). Ripetibile.",
)
@click.option("--truncate", is_flag=True, default=False, help="Truncate destination prima della copia")
@click.option("--print-src-tables", is_flag=True, default=False, help="Mostra conteggio tabelle source")
@click.option("--no-replace-db-host", is_flag=True, default=False)
@click.option("--src-profile-name", default=None, help="AWS profile per source")
@click.option("--dest-profile-name", default=None, help="AWS profile per destination")
@click.option("-y", "--yes", is_flag=True, default=False, help="Skip conferma interattiva")
def main(
    source: str,
    destination: str,
    tables: tuple[str, ...],
    truncate: bool,
    print_src_tables: bool,
    no_replace_db_host: bool,
    src_profile_name: str | None,
    dest_profile_name: str | None,
    yes: bool,
):
    """Trasferisce dati da un database PostgreSQL a un altro.

    SOURCE e DESTINATION possono essere: ARN AWS Secrets Manager, URL PostgreSQL,
    o percorso a un file .env.

    Le tabelle possono contenere wildcard (es. -t 'template.*' -t 'prs.predictions').
    """
    if not tables:
        print("[red]Nessuna tabella specificata.[/] Usa -t per indicare i pattern.")
        print("Esempio: -t 'template.*' -t 'prs.*'")
        sys.exit(1)

    replace = not no_replace_db_host
    src_profile = src_profile_name or os.getenv("AWS_PROFILE_NAME")
    dest_profile = dest_profile_name or os.getenv("AWS_PROFILE_NAME")

    print("Recupero credenziali... ", end="", flush=True)
    try:
        src_url = resolve_url(source, src_profile, replace)
        dest_url = resolve_url(destination, dest_profile, replace)
    except Exception as e:
        print(f"[red]Errore[/]: {e}")
        sys.exit(1)
    print("[green]OK[/]")

    # Mask passwords in display
    def _mask(url: str) -> str:
        import re
        return re.sub(r"://([^:]+):([^@]+)@", r"://\1:***@", url)

    print(f"\n[bold]SOURCE:[/]      {_mask(src_url)}")
    print(f"[bold]DESTINATION:[/] {_mask(dest_url)}")

    # Resolve and sort tables
    with Status("Risoluzione tabelle e dipendenze FK...") as st:
        src_conn = psycopg2.connect(src_url)
        try:
            resolved = resolve_table_order(src_conn, list(tables))
        finally:
            src_conn.close()

    print(f"\n[bold]{len(resolved)} tabelle[/] ordinate per dipendenze FK:")
    for i, t in enumerate(resolved, 1):
        print(f"  {i:3}. {t}")

    if print_src_tables:
        print_table_counts(src_url, resolved, "Conteggio SOURCE:")

    print_table_counts(dest_url, resolved, "Conteggio DESTINATION:")

    # Check which tables already exist in destination
    existing = dest_existing_tables(dest_url)
    new_tables = [t for t in resolved if t not in existing]
    if new_tables:
        print(f"\n[cyan]{len(new_tables)} tabelle non presenti nella destination (verranno create con schema):[/]")
        for t in new_tables:
            print(f"  [cyan]+[/] {t}")

    # Confirmation
    if not yes:
        msg = f"\n⚠️  Stai per modificare: {_mask(dest_url)}"
        if truncate:
            msg += "\n[bold red]TRUNCATE richiesto — tutti i dati nella destination verranno cancellati![/]"

        confirm = Prompt.ask(f"{msg}\nContinuare? [y/N]").strip().lower()
        if confirm != "y":
            print("Operazione annullata.")
            return

    # Truncate
    if truncate:
        print("\n[bold]Truncate destination...[/]")
        truncate_tables(dest_url, resolved, existing)

    # Copy
    print("\n[bold]Copia tabelle...[/]")
    print("[dim]FK constraint disabilitati durante la copia (session_replication_role = replica)[/]")
    with Status("...") as st:
        errors = copy_tables(src_url, dest_url, resolved, existing, st, disable_fk=True)

    # Post-copy verification
    print_table_counts(dest_url, resolved, "Conteggio DESTINATION dopo copia:")

    if errors:
        console.rule("[bold red]Errori durante il trasferimento")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        console.rule("[bold green]Trasferimento completato con successo")


if __name__ == "__main__":
    main()
