#!/usr/bin/env python3
"""
AWS S3 Diagnose — Diagnosi bucket S3 per progetti LAIF.

Uso:
  python3 run.py --project <nome> --env <dev|prod> --bucket <data|frontend|all> --mode <overview|recent|large|all>

Solo comandi read-only.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_shared"))

from config import load_config, get_resource
from aws_runner import aws_cli, s3_ls
from output import format_table


def diagnose_overview(bucket_name: str, config: dict):
    """Overview: dimensione totale e conteggio oggetti."""
    print(f"\n**Overview: {bucket_name}**\n")

    result = s3_ls(bucket_name, profile=config["aws_profile"], region=config["region"])

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    output = result.get("raw_output", "")
    if output:
        # L'output di s3 ls --summarize contiene le ultime 2 righe con totali
        lines = output.strip().split("\n")
        summary_lines = [l.strip() for l in lines if l.strip().startswith("Total")]
        if summary_lines:
            for sl in summary_lines:
                print(f"  {sl}")
        else:
            print(f"  (output: {len(lines)} righe)")
    else:
        print("  Bucket vuoto o non accessibile.")


def diagnose_recent(bucket_name: str, config: dict):
    """Upload recenti (ultime 24h)."""
    print(f"\n**Upload recenti (24h): {bucket_name}**\n")

    result = aws_cli(
        "s3api", "list-objects-v2",
        ["--bucket", bucket_name, "--max-items", "100"],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    contents = result.get("Contents", [])
    if not contents:
        print("  Nessun oggetto trovato.")
        return

    # Filtra per ultime 24h
    cutoff = datetime.now(timezone.utc).timestamp() - 86400
    recent = []
    for obj in contents:
        last_modified = obj.get("LastModified", "")
        if last_modified:
            try:
                # AWS CLI ritorna timestamp ISO
                ts = datetime.fromisoformat(last_modified.replace("Z", "+00:00")).timestamp()
                if ts >= cutoff:
                    recent.append(obj)
            except (ValueError, TypeError):
                pass

    if not recent:
        print("  Nessun upload nelle ultime 24h.")
        return

    # Ordina per data, piu recente prima
    recent.sort(key=lambda x: x.get("LastModified", ""), reverse=True)

    rows = []
    for obj in recent[:20]:
        key = obj.get("Key", "?")
        size = obj.get("Size", 0)
        size_str = _format_size(size)
        modified = obj.get("LastModified", "?")[:19]
        rows.append([key[-60:] if len(key) > 60 else key, size_str, modified])

    print(format_table(["Key", "Dimensione", "Ultima modifica"], rows))


def diagnose_large(bucket_name: str, config: dict):
    """File piu grandi nel bucket."""
    print(f"\n**File piu grandi: {bucket_name}**\n")

    result = aws_cli(
        "s3api", "list-objects-v2",
        ["--bucket", bucket_name, "--max-items", "1000"],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    contents = result.get("Contents", [])
    if not contents:
        print("  Nessun oggetto trovato.")
        return

    # Ordina per dimensione decrescente
    contents.sort(key=lambda x: x.get("Size", 0), reverse=True)

    rows = []
    for obj in contents[:10]:
        key = obj.get("Key", "?")
        size = obj.get("Size", 0)
        size_str = _format_size(size)
        modified = obj.get("LastModified", "?")[:19]
        rows.append([key[-60:] if len(key) > 60 else key, size_str, modified])

    print(format_table(["Key", "Dimensione", "Ultima modifica"], rows))


def _format_size(size_bytes: int) -> str:
    """Formatta dimensione in unita leggibili."""
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024**3):.1f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024**2):.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes} B"


def run_for_bucket(bucket_key: str, label: str, config: dict, mode: str):
    """Esegue diagnosi per un singolo bucket."""
    try:
        bucket_name = get_resource(config, bucket_key)
    except SystemExit:
        print(f"\n⚠ Bucket '{label}' non configurato in aws-config.yaml, saltato.")
        return

    print(f"\n--- Bucket: {label} ({bucket_name}) ---")

    # Check accessibilita
    check = aws_cli(
        "s3api", "head-bucket",
        ["--bucket", bucket_name],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in check:
        print(f"ERRORE: bucket non accessibile - {check['error']}")
        return

    if mode in ("overview", "all"):
        diagnose_overview(bucket_name, config)
    if mode in ("recent", "all"):
        diagnose_recent(bucket_name, config)
    if mode in ("large", "all"):
        diagnose_large(bucket_name, config)


def main():
    parser = argparse.ArgumentParser(
        description="AWS S3 Diagnose - Diagnosi bucket S3",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--bucket", default="all",
                        choices=["data", "frontend", "all"],
                        help="Quale bucket (default: all)")
    parser.add_argument("--mode", default="overview",
                        choices=["overview", "recent", "large", "all"],
                        help="Cosa investigare (default: overview)")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    config = load_config(args.project, args.env, args.kb_root)

    print(f"\n## AWS S3 DIAGNOSE — {args.project} ({args.env})")

    if args.bucket in ("data", "all"):
        run_for_bucket("s3_data_bucket", "Data", config, args.mode)
    if args.bucket in ("frontend", "all"):
        run_for_bucket("s3_frontend_bucket", "Frontend", config, args.mode)


if __name__ == "__main__":
    main()
