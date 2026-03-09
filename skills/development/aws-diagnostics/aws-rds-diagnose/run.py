#!/usr/bin/env python3
"""
AWS RDS Diagnose — Diagnosi approfondita RDS PostgreSQL per progetti LAIF.

Uso:
  python3 run.py --project <nome> --env <dev|prod> --mode <status|connections|logs|parameters|all>

Solo comandi read-only.
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_shared"))

from config import load_config, get_resource
from aws_runner import aws_cli
from output import format_table, format_metric_chart


def diagnose_status(config: dict):
    """Stato generale dell'istanza RDS."""
    print("\n### Status\n")

    result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    instances = result.get("DBInstances", [])
    if not instances:
        print("Istanza non trovata.")
        return

    db = instances[0]
    endpoint = db.get("Endpoint", {})

    rows = [
        ["Stato", db.get("DBInstanceStatus", "?")],
        ["Classe", db.get("DBInstanceClass", "?")],
        ["Engine", f"PostgreSQL {db.get('EngineVersion', '?')}"],
        ["Storage allocato", f"{db.get('AllocatedStorage', '?')} GB"],
        ["Storage max", f"{db.get('MaxAllocatedStorage', 'N/A')} GB"],
        ["Multi-AZ", str(db.get("MultiAZ", False))],
        ["Endpoint", endpoint.get("Address", "?")],
        ["Porta", str(endpoint.get("Port", "?"))],
        ["Backup retention", f"{db.get('BackupRetentionPeriod', '?')} giorni"],
        ["Maintenance window", db.get("PreferredMaintenanceWindow", "?")],
        ["Backup window", db.get("PreferredBackupWindow", "?")],
    ]

    # Pending modifications
    pending = db.get("PendingModifiedValues", {})
    if pending:
        rows.append(["Modifiche pending", str(pending)])

    print(format_table(["Proprieta", "Valore"], rows))


def diagnose_connections(config: dict):
    """Parametri connessione del database."""
    print("\n### Connections\n")

    # Ottieni parameter group name
    result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    instances = result.get("DBInstances", [])
    if not instances:
        print("Istanza non trovata.")
        return

    db = instances[0]
    param_groups = db.get("DBParameterGroups", [])
    if not param_groups:
        print("Nessun parameter group trovato.")
        return

    pg_name = param_groups[0].get("DBParameterGroupName", "")
    print(f"Parameter Group: {pg_name}")
    print(f"Apply Status: {param_groups[0].get('ParameterApplyStatus', '?')}")

    # Parametri rilevanti per le connessioni
    connection_params = [
        "max_connections", "shared_buffers", "work_mem",
        "effective_cache_size", "maintenance_work_mem",
        "idle_in_transaction_session_timeout", "statement_timeout",
        "log_min_duration_statement",
    ]

    params_result = aws_cli(
        "rds", "describe-db-parameters",
        ["--db-parameter-group-name", pg_name],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in params_result:
        print(f"ERRORE: {params_result['error']}")
        return

    params = params_result.get("Parameters", [])
    rows = []
    for p in params:
        name = p.get("ParameterName", "")
        if name in connection_params:
            value = p.get("ParameterValue", "default")
            source = p.get("Source", "?")
            rows.append([name, value or "default", source])

    if rows:
        print(f"\n" + format_table(["Parametro", "Valore", "Source"], rows))
    else:
        print("Nessun parametro di connessione trovato.")


def diagnose_logs(config: dict):
    """Log PostgreSQL recenti."""
    print("\n### Logs\n")

    rds_id = get_resource(config, "rds_identifier")

    # Lista file di log
    result = aws_cli(
        "rds", "describe-db-log-files",
        ["--db-instance-identifier", rds_id],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    log_files = result.get("DescribeDBLogFiles", [])
    if not log_files:
        print("Nessun file di log trovato.")
        return

    # Mostra ultimi 5 file
    log_files = sorted(log_files, key=lambda x: x.get("LastWritten", 0))
    recent_files = log_files[-5:]

    rows = []
    for lf in recent_files:
        name = lf.get("LogFileName", "?")
        size = lf.get("Size", 0)
        size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
        rows.append([name, size_str])

    print(format_table(["File", "Dimensione"], rows))

    # Scarica l'ultimo file
    latest = recent_files[-1]
    latest_name = latest.get("LogFileName", "")
    if latest_name:
        print(f"\n**Ultime righe di {latest_name}:**\n")

        dl_result = aws_cli(
            "rds", "download-db-log-file-portion",
            [
                "--db-instance-identifier", rds_id,
                "--log-file-name", latest_name,
                "--starting-token", "0",
            ],
            profile=config["aws_profile"],
            region=config["region"],
        )

        if "error" in dl_result:
            print(f"ERRORE: {dl_result['error']}")
            return

        log_data = dl_result.get("LogFileData", "")
        if log_data:
            # Mostra ultime 30 righe
            lines = log_data.strip().split("\n")
            for line in lines[-30:]:
                print(f"  {line}")
        else:
            print("  (log vuoto)")


def diagnose_parameters(config: dict):
    """Parametri custom (source=user) del parameter group."""
    print("\n### Parametri Custom\n")

    # Ottieni parameter group name
    result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    instances = result.get("DBInstances", [])
    if not instances:
        print("Istanza non trovata.")
        return

    pg_name = instances[0].get("DBParameterGroups", [{}])[0].get("DBParameterGroupName", "")
    if not pg_name:
        print("Parameter group non trovato.")
        return

    params_result = aws_cli(
        "rds", "describe-db-parameters",
        ["--db-parameter-group-name", pg_name, "--source", "user"],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in params_result:
        print(f"ERRORE: {params_result['error']}")
        return

    params = params_result.get("Parameters", [])
    if not params:
        print("Nessun parametro custom (tutti ai valori default).")
        return

    rows = []
    for p in sorted(params, key=lambda x: x.get("ParameterName", "")):
        rows.append([
            p.get("ParameterName", "?"),
            p.get("ParameterValue", "?"),
            p.get("ApplyType", "?"),
            "pending" if p.get("ApplyMethod") == "pending-reboot" else "immediato",
        ])

    print(format_table(["Parametro", "Valore", "Tipo", "Apply"], rows))


def _get_rds_metric(config: dict, metric_name: str, hours: int = 24, period: int = 3600) -> tuple:
    """Recupera metriche CloudWatch per RDS. Ritorna (values, timestamps)."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)
    rds_id = get_resource(config, "rds_identifier")

    result = aws_cli(
        "cloudwatch", "get-metric-statistics",
        [
            "--namespace", "AWS/RDS",
            "--metric-name", metric_name,
            "--start-time", start.strftime("%Y-%m-%dT%H:%M:%S"),
            "--end-time", now.strftime("%Y-%m-%dT%H:%M:%S"),
            "--period", str(period),
            "--statistics", "Average",
            "--dimensions", f"Name=DBInstanceIdentifier,Value={rds_id}",
        ],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result or not result.get("Datapoints"):
        return [], []

    points = sorted(result["Datapoints"], key=lambda x: x["Timestamp"])
    values = [p.get("Average", 0) for p in points]
    timestamps = [p["Timestamp"][:16] for p in points]
    return values, timestamps


def diagnose_metrics(config: dict, hours: int = 24):
    """Metriche CloudWatch per RDS: CPU, memoria, connessioni, I/O."""
    period_label = f"ultime {hours}h"
    print(f"\n### Metriche RDS ({period_label})\n")

    period = 3600 if hours <= 48 else 21600

    # CPU Utilization
    cpu_vals, cpu_ts = _get_rds_metric(config, "CPUUtilization", hours, period)
    if cpu_vals:
        print(format_metric_chart("CPU", cpu_vals, cpu_ts, unit="%"))
    else:
        print("  CPU: (nessun dato)")

    print()

    # FreeableMemory (bytes → MB)
    mem_vals, mem_ts = _get_rds_metric(config, "FreeableMemory", hours, period)
    if mem_vals:
        mem_mb = [v / (1024 * 1024) for v in mem_vals]
        print(format_metric_chart("RAM libera", mem_mb, mem_ts, unit="MB"))
    else:
        print("  RAM libera: (nessun dato)")

    print()

    # DatabaseConnections
    conn_vals, conn_ts = _get_rds_metric(config, "DatabaseConnections", hours, period)
    if conn_vals:
        print(format_metric_chart("Connessioni", conn_vals, conn_ts, unit=""))
    else:
        print("  Connessioni: (nessun dato)")

    print()

    # ReadLatency
    rl_vals, rl_ts = _get_rds_metric(config, "ReadLatency", hours, period)
    if rl_vals:
        rl_ms = [v * 1000 for v in rl_vals]
        print(format_metric_chart("Read latency", rl_ms, rl_ts, unit="ms"))
    else:
        print("  Read latency: (nessun dato)")

    print()

    # WriteLatency
    wl_vals, wl_ts = _get_rds_metric(config, "WriteLatency", hours, period)
    if wl_vals:
        wl_ms = [v * 1000 for v in wl_vals]
        print(format_metric_chart("Write latency", wl_ms, wl_ts, unit="ms"))
    else:
        print("  Write latency: (nessun dato)")


def main():
    parser = argparse.ArgumentParser(
        description="AWS RDS Diagnose - Diagnosi approfondita RDS PostgreSQL",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--mode", default="all",
                        choices=["status", "metrics", "connections", "logs", "parameters", "all"],
                        help="Cosa investigare (default: all)")
    parser.add_argument("--hours", type=int, default=24,
                        help="Finestra metriche in ore (default: 24)")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    config = load_config(args.project, args.env, args.kb_root)

    print(f"\n## AWS RDS DIAGNOSE — {args.project} ({args.env})")
    print(f"Istanza: {get_resource(config, 'rds_identifier')}")

    if args.mode in ("status", "all"):
        diagnose_status(config)
    if args.mode in ("metrics", "all"):
        diagnose_metrics(config, hours=args.hours)
    if args.mode in ("connections", "all"):
        diagnose_connections(config)
    if args.mode in ("logs", "all"):
        diagnose_logs(config)
    if args.mode in ("parameters", "all"):
        diagnose_parameters(config)


if __name__ == "__main__":
    main()
