#!/usr/bin/env python3
"""
AWS Triage — Health check rapido di tutti i servizi AWS di un progetto LAIF.

Uso:
  python3 run.py --project <nome> --env <dev|prod>

Esempio:
  python3 run.py --project jubatus --env dev

Solo comandi read-only. Nessuna modifica alle risorse AWS.
"""

import argparse
import os
import sys
import time

# Aggiungi _shared al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_shared"))

from config import load_config, get_resource
from aws_runner import aws_cli, logs_insights_query
from output import semaphore, format_table, format_report, verdict


def check_ecs(config: dict) -> tuple:
    """Check ECS service status. Returns (status, detail)."""
    result = aws_cli(
        "ecs", "describe-services",
        [
            "--cluster", get_resource(config, "ecs_cluster"),
            "--services", get_resource(config, "ecs_service"),
        ],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return "FAIL", result["error"]

    services = result.get("services", [])
    if not services:
        return "FAIL", "Servizio non trovato"

    svc = services[0]
    status = svc.get("status", "UNKNOWN")
    desired = svc.get("desiredCount", 0)
    running = svc.get("runningCount", 0)
    deployments = svc.get("deployments", [])

    if status != "ACTIVE":
        return "FAIL", f"Servizio {status}"

    if running < desired:
        return "FAIL", f"{running}/{desired} task running"

    if len(deployments) > 1:
        return "WARN", f"{running}/{desired} task, deployment in corso ({len(deployments)} deployment)"

    rollout = deployments[0].get("rolloutState", "UNKNOWN") if deployments else "UNKNOWN"
    return "OK", f"{running}/{desired} task, {rollout}"


def check_rds(config: dict) -> tuple:
    """Check RDS instance status. Returns (status, detail)."""
    result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return "FAIL", result["error"]

    instances = result.get("DBInstances", [])
    if not instances:
        return "FAIL", "Istanza non trovata"

    db = instances[0]
    db_status = db.get("DBInstanceStatus", "unknown")
    db_class = db.get("DBInstanceClass", "unknown")

    if db_status == "available":
        return "OK", f"{db_status}, {db_class}"
    elif db_status in ("backing-up", "maintenance", "modifying"):
        return "WARN", f"{db_status}, {db_class}"
    else:
        return "FAIL", f"{db_status}, {db_class}"


def check_logs(config: dict) -> tuple:
    """Check recent errors in CloudWatch. Returns (status, detail)."""
    now = int(time.time())
    one_hour_ago = now - 3600

    result = logs_insights_query(
        log_group=get_resource(config, "log_group"),
        query="fields @timestamp, @message | filter @message like /ERROR|Exception|Traceback|CRITICAL/ | stats count(*) as error_count",
        start_time=one_hour_ago,
        end_time=now,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return "WARN", f"Query fallita: {result['error']}"

    results = result.get("results", [])
    error_count = 0
    for row in results:
        for field in row:
            if field.get("field") == "error_count":
                try:
                    error_count = int(field.get("value", 0))
                except (ValueError, TypeError):
                    error_count = 0

    if error_count == 0:
        return "OK", "0 errori nell'ultima ora"
    elif error_count <= 10:
        return "WARN", f"{error_count} errori nell'ultima ora"
    else:
        return "FAIL", f"{error_count} errori nell'ultima ora"


def check_s3(config: dict, bucket_key: str, label: str) -> tuple:
    """Check S3 bucket accessibility. Returns (status, detail)."""
    bucket_name = get_resource(config, bucket_key)
    result = aws_cli(
        "s3api", "head-bucket",
        ["--bucket", bucket_name],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return "FAIL", f"non accessibile ({result['error'][:80]})"
    return "OK", "accessibile"


def main():
    parser = argparse.ArgumentParser(
        description="AWS Triage - Health check rapido servizi AWS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Esempio: python3 run.py --project jubatus --env dev",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    # Carica config
    config = load_config(args.project, args.env, args.kb_root)

    print(f"\n## AWS TRIAGE — {args.project} ({args.env})")
    print(f"Profilo: {config['aws_profile']} | Regione: {config['region']}\n")

    # Esegui check
    checks = []

    print("Checking ECS...", end=" ", flush=True)
    ecs_status, ecs_detail = check_ecs(config)
    checks.append(("ECS Service", ecs_status, ecs_detail))
    print(semaphore(ecs_status))

    print("Checking RDS...", end=" ", flush=True)
    rds_status, rds_detail = check_rds(config)
    checks.append(("RDS", rds_status, rds_detail))
    print(semaphore(rds_status))

    print("Checking CloudWatch...", end=" ", flush=True)
    logs_status, logs_detail = check_logs(config)
    checks.append(("CloudWatch", logs_status, logs_detail))
    print(semaphore(logs_status))

    print("Checking S3 Data...", end=" ", flush=True)
    s3d_status, s3d_detail = check_s3(config, "s3_data_bucket", "Data")
    checks.append(("S3 Data", s3d_status, s3d_detail))
    print(semaphore(s3d_status))

    # Report
    print("\n" + format_table(
        ["Servizio", "Stato", "Dettaglio"],
        [[name, semaphore(status), detail] for name, status, detail in checks],
    ))

    overall = verdict([status for _, status, _ in checks])
    print(f"\nVerdetto: {semaphore(overall)}")

    # Suggerimenti
    problem_services = [(name, status) for name, status, _ in checks if status != "OK"]
    if problem_services:
        print("\nAzione consigliata:")
        base = "skills/development/aws-diagnostics"
        for name, status in problem_services:
            if "ECS" in name:
                print(f"  ECS: python3 {base}/aws-ecs-diagnose/run.py --project {args.project} --env {args.env} --mode all")
            elif "RDS" in name:
                print(f"  RDS: python3 {base}/aws-rds-diagnose/run.py --project {args.project} --env {args.env} --mode status")
            elif "CloudWatch" in name:
                print(f"  Logs: python3 {base}/aws-logs-diagnose/run.py --project {args.project} --env {args.env} --query-type errors --time-window 1h")
            elif "S3" in name:
                print(f"  S3: python3 {base}/aws-s3-diagnose/run.py --project {args.project} --env {args.env} --mode overview")


if __name__ == "__main__":
    main()
