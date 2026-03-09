#!/usr/bin/env python3
"""
AWS Logs Diagnose — Query CloudWatch Logs Insights per progetti LAIF.

Uso:
  python3 run.py --project <nome> --env <dev|prod> --query-type <tipo> --time-window <finestra>

Query types: errors, db-issues, slow-requests, status-codes, recent, memory, custom

Solo comandi read-only.
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_shared"))

from config import load_config, get_resource
from aws_runner import logs_insights_query
from output import format_table

# Query templates
QUERY_TEMPLATES = {
    "errors": {
        "description": "Errori ed eccezioni",
        "query": """fields @timestamp, @message, @logStream
| filter @message like /ERROR|Exception|Traceback|CRITICAL/
| sort @timestamp desc
| limit 100""",
    },
    "db-issues": {
        "description": "Problemi connessione database",
        "query": """fields @timestamp, @message
| filter @message like /psycopg|connection refused|timeout|ConnectionError|OperationalError|too many connections|remaining connection slots/
| stats count(*) as occurrences by bin(5m)
| sort @timestamp desc""",
    },
    "slow-requests": {
        "description": "Request lente",
        "query": """fields @timestamp, @message
| filter @message like /took \\d{4,}ms|duration.*[1-9]\\d{3,}/
| sort @timestamp desc
| limit 50""",
    },
    "status-codes": {
        "description": "Distribuzione status code HTTP",
        "query": """fields @timestamp, @message
| filter @message like /"status":\\s*\\d{3}|"status_code":\\s*\\d{3}/
| parse @message /"status":\\s*(?<statusCode>\\d{3})/
| stats count(*) as request_count by statusCode
| sort request_count desc""",
    },
    "errors-http": {
        "description": "Errori HTTP (4xx e 5xx)",
        "query": """fields @timestamp, @message
| filter @message like /"status":\\s*(4|5)\\d{2}/
| parse @message /"status":\\s*(?<statusCode>\\d{3})/
| parse @message /"path":\\s*"(?<path>[^"]+)"/
| parse @message /"method":\\s*"(?<method>[^"]+)"/
| display @timestamp, method, path, statusCode, @message
| sort @timestamp desc
| limit 100""",
    },
    "recent": {
        "description": "Ultimi log (tail)",
        "query": """fields @timestamp, @message
| sort @timestamp desc
| limit 50""",
    },
    "memory": {
        "description": "Problemi di memoria",
        "query": """fields @timestamp, @message
| filter @message like /MemoryError|OOM|OutOfMemory|memory|Cannot allocate/
| sort @timestamp desc
| limit 50""",
    },
}

TIME_WINDOWS = {
    "15m": 15 * 60,
    "1h": 3600,
    "6h": 6 * 3600,
    "24h": 24 * 3600,
}


def format_results(results: list) -> str:
    """Formatta risultati Logs Insights in tabella."""
    if not results:
        return "Nessun risultato trovato."

    # Estrai headers dai campi del primo risultato
    headers = []
    for field in results[0]:
        fname = field.get("field", "?")
        if fname != "@ptr":  # Escludi pointer interno
            headers.append(fname)

    if not headers:
        return "Nessun campo nei risultati."

    # Estrai righe
    rows = []
    for result in results[:50]:  # Max 50 righe in output
        row = []
        for field in result:
            fname = field.get("field", "?")
            if fname != "@ptr":
                value = field.get("value", "")
                # Tronca messaggi lunghi
                if fname == "@message" and len(value) > 120:
                    value = value[:120] + "..."
                row.append(value)
        if row:
            rows.append(row)

    return format_table(headers, rows)


def main():
    parser = argparse.ArgumentParser(
        description="AWS Logs Diagnose - Query CloudWatch Logs Insights",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--query-type", default="errors",
                        choices=list(QUERY_TEMPLATES.keys()) + ["custom"],
                        help="Tipo di query (default: errors)")
    parser.add_argument("--time-window", default="1h",
                        choices=list(TIME_WINDOWS.keys()),
                        help="Finestra temporale (default: 1h)")
    parser.add_argument("--custom-query", help="Query Logs Insights custom (solo con --query-type custom)")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    if args.query_type == "custom" and not args.custom_query:
        print("ERRORE: --custom-query richiesto con --query-type custom")
        sys.exit(1)

    config = load_config(args.project, args.env, args.kb_root)
    log_group = get_resource(config, "log_group")

    # Determina query
    if args.query_type == "custom":
        query = args.custom_query
        description = "Query custom"
    else:
        template = QUERY_TEMPLATES[args.query_type]
        query = template["query"]
        description = template["description"]

    # Calcola finestra temporale
    now = int(time.time())
    window_seconds = TIME_WINDOWS[args.time_window]
    start_time = now - window_seconds

    print(f"\n## AWS LOGS DIAGNOSE — {args.project} ({args.env})")
    print(f"Log Group: {log_group}")
    print(f"Query: {description}")
    print(f"Finestra: ultimi {args.time_window}")
    print(f"\nEsecuzione query...", end=" ", flush=True)

    # Esegui query
    result = logs_insights_query(
        log_group=log_group,
        query=query,
        start_time=start_time,
        end_time=now,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"\nERRORE: {result['error']}")
        sys.exit(1)

    print("completata.")

    # Statistiche
    stats = result.get("statistics", {})
    records_matched = stats.get("recordsMatched", 0)
    records_scanned = stats.get("recordsScanned", 0)
    bytes_scanned = stats.get("bytesScanned", 0)

    print(f"Record trovati: {records_matched} (scansionati: {records_scanned}, bytes: {bytes_scanned})")

    # Risultati
    results = result.get("results", [])
    print(f"\n### Risultati ({len(results)})\n")
    print(format_results(results))


if __name__ == "__main__":
    main()
