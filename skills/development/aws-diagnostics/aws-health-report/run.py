#!/usr/bin/env python3
"""
AWS Health Report — Genera report HTML completo dell'infrastruttura AWS.

Uso:
  python3 run.py --project <nome> --env <dev|prod> [--hours 24] [--log-window 1h]

Output: projects/{project}/reports/aws-report-YYYY-MM-DD-HHMMSS.html

Solo comandi read-only. Nessuna modifica alle risorse AWS.
"""

import argparse
import os
import sys
from datetime import datetime

# Path setup
_this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_this_dir, "..", "_shared"))
sys.path.insert(0, _this_dir)

from config import load_config, get_resource, find_kb_root
from collectors import (
    collect_triage,
    collect_ecs_deployment,
    collect_ecs_task_failures,
    collect_ecs_instances,
    collect_ecs_metrics,
    collect_rds_status,
    collect_rds_metrics,
    collect_logs_query,
    collect_s3_overview,
)
from html_renderer import render_report


def progress(step: int, total: int, message: str, status: str = ""):
    """Stampa progress su stdout."""
    suffix = f" {status}" if status else ""
    print(f"  [{step}/{total}] {message}...{suffix}", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="AWS Health Report — Genera report HTML completo",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--hours", type=int, default=24,
                        help="Finestra metriche CloudWatch in ore (default: 24)")
    parser.add_argument("--log-window", default="1h",
                        choices=["15m", "1h", "6h", "24h"],
                        help="Finestra query log (default: 1h)")
    parser.add_argument("--output", help="Path output custom")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    # Config
    config = load_config(args.project, args.env, args.kb_root)
    kb_root = args.kb_root or find_kb_root()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = 8

    print(f"\nAWS Health Report — {args.project} ({args.env})")
    print(f"Profilo: {config['aws_profile']} | Regione: {config['region']}")
    print(f"Metriche: {args.hours}h | Log: {args.log_window}\n")

    # Raccolta dati
    report_data = {
        "project": args.project,
        "env": args.env,
        "timestamp": timestamp,
        "profile": config["aws_profile"],
        "region": config["region"],
        "hours": args.hours,
        "log_window": args.log_window,
    }

    # 1. Triage
    progress(1, total, "Triage")
    report_data["triage"] = collect_triage(config)
    verdict = report_data["triage"].get("verdict", "?")
    progress(1, total, "Triage", verdict)

    # 2. ECS deployment + instances
    progress(2, total, "ECS deployment + instances")
    report_data["ecs_deployment"] = collect_ecs_deployment(config)
    report_data["ecs_instances"] = collect_ecs_instances(config)
    progress(2, total, "ECS deployment + instances", "OK")

    # 3. ECS metrics
    progress(3, total, f"ECS metrics ({args.hours}h)")
    report_data["ecs_metrics"] = collect_ecs_metrics(config, hours=args.hours)
    progress(3, total, f"ECS metrics ({args.hours}h)", "OK")

    # 4. ECS task failures
    progress(4, total, "ECS task failures")
    report_data["ecs_failures"] = collect_ecs_task_failures(config)
    progress(4, total, "ECS task failures", "OK")

    # 5. RDS status + metrics
    progress(5, total, f"RDS status + metrics ({args.hours}h)")
    report_data["rds_status"] = collect_rds_status(config)
    report_data["rds_metrics"] = collect_rds_metrics(config, hours=args.hours)
    progress(5, total, f"RDS status + metrics ({args.hours}h)", "OK")

    # 6. Logs: errors
    progress(6, total, "Logs: errors")
    report_data["logs_errors"] = collect_logs_query(config, "errors", args.log_window)
    err_count = report_data["logs_errors"].get("result_count", 0)
    progress(6, total, "Logs: errors", f"{err_count} trovati")

    # 7. Logs: HTTP errors + status codes
    progress(7, total, "Logs: HTTP errors + status codes")
    report_data["logs_http_errors"] = collect_logs_query(config, "errors-http", args.log_window)
    report_data["logs_status_codes"] = collect_logs_query(config, "status-codes", args.log_window)
    http_count = report_data["logs_http_errors"].get("result_count", 0)
    progress(7, total, "Logs: HTTP errors + status codes", f"{http_count} HTTP errors")

    # 8. S3 buckets
    progress(8, total, "S3 buckets")
    try:
        data_bucket = get_resource(config, "s3_data_bucket")
        report_data["s3_data"] = collect_s3_overview(data_bucket, config)
    except SystemExit:
        report_data["s3_data"] = {"bucket": "N/A", "accessible": False,
                                  "summary_lines": [], "error": "non configurato"}
    try:
        fe_bucket = get_resource(config, "s3_frontend_bucket")
        report_data["s3_frontend"] = collect_s3_overview(fe_bucket, config)
    except SystemExit:
        report_data["s3_frontend"] = {"bucket": "N/A", "accessible": False,
                                      "summary_lines": [], "error": "non configurato"}
    progress(8, total, "S3 buckets", "OK")

    # Rendering HTML
    print("\nGenerazione HTML...", end=" ", flush=True)
    html_content = render_report(report_data)
    print("OK")

    # Output path
    if args.output:
        output_path = args.output
    else:
        ts_file = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        reports_dir = os.path.join(kb_root, "projects", args.project, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        output_path = os.path.join(reports_dir, f"aws-report-{ts_file}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\nReport generato: {output_path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
