#!/usr/bin/env python3
"""
AWS ECS Diagnose — Diagnosi approfondita ECS per progetti LAIF.

Uso:
  python3 run.py --project <nome> --env <dev|prod> --mode <deployment|task-failure|capacity|config|all>

Solo comandi read-only.
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_shared"))

from config import load_config, get_resource
from aws_runner import aws_cli
from output import semaphore, format_table, format_metric_chart


def diagnose_deployment(config: dict):
    """Analizza deployment e rollout del servizio ECS."""
    print("\n### Deployment\n")

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
        print(f"ERRORE: {result['error']}")
        return

    services = result.get("services", [])
    if not services:
        print("Servizio non trovato.")
        return

    svc = services[0]

    # Deployments
    deployments = svc.get("deployments", [])
    if deployments:
        rows = []
        for d in deployments:
            rows.append([
                d.get("status", "?"),
                d.get("rolloutState", "?"),
                f"{d.get('runningCount', 0)}/{d.get('desiredCount', 0)}",
                d.get("taskDefinition", "?").split("/")[-1],
                d.get("updatedAt", "?"),
            ])
        print(format_table(
            ["Status", "Rollout", "Running/Desired", "Task Def", "Aggiornato"],
            rows,
        ))
    else:
        print("Nessun deployment trovato.")

    # Events (ultimi 10)
    events = svc.get("events", [])[:10]
    if events:
        print("\n**Ultimi 10 eventi:**\n")
        for ev in events:
            ts = str(ev.get("createdAt", "?"))[:19]
            msg = ev.get("message", "")
            print(f"  [{ts}] {msg}")


def diagnose_task_failure(config: dict):
    """Analizza task stoppati: exit code, stopped reason."""
    print("\n### Task Failure\n")

    # Lista task stoppati
    result = aws_cli(
        "ecs", "list-tasks",
        [
            "--cluster", get_resource(config, "ecs_cluster"),
            "--service-name", get_resource(config, "ecs_service"),
            "--desired-status", "STOPPED",
        ],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    task_arns = result.get("taskArns", [])
    if not task_arns:
        print("Nessun task stoppato trovato.")
        return

    # Dettagli task (max 10)
    task_arns = task_arns[:10]
    detail = aws_cli(
        "ecs", "describe-tasks",
        ["--cluster", get_resource(config, "ecs_cluster"), "--tasks"] + task_arns,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in detail:
        print(f"ERRORE: {detail['error']}")
        return

    tasks = detail.get("tasks", [])
    rows = []
    for t in tasks:
        task_id = t.get("taskArn", "?").split("/")[-1][:12]
        stop_code = t.get("stopCode", "?")
        stopped_reason = t.get("stoppedReason", "?")[:60]
        containers = t.get("containers", [])
        exit_code = containers[0].get("exitCode", "?") if containers else "?"
        started = str(t.get("startedAt", "?"))[:19]
        stopped = str(t.get("stoppedAt", "?"))[:19]
        rows.append([task_id, str(exit_code), stop_code, stopped_reason, started, stopped])

    print(format_table(
        ["Task ID", "Exit", "Stop Code", "Motivo", "Avviato", "Fermato"],
        rows,
    ))

    # Analisi exit code
    exit_codes = [r[1] for r in rows if r[1] != "?"]
    if "137" in exit_codes:
        print("\n⚠ Exit code 137 = SIGKILL (probabile OOM). Verifica memoria con aws-logs-diagnose --query-type memory")
    if "1" in exit_codes:
        print("\n⚠ Exit code 1 = errore applicativo. Verifica log con aws-logs-diagnose --query-type errors")


def diagnose_capacity(config: dict):
    """Analizza capacity del cluster ECS."""
    print("\n### Cluster Capacity\n")

    result = aws_cli(
        "ecs", "describe-clusters",
        [
            "--clusters", get_resource(config, "ecs_cluster"),
            "--include", "STATISTICS",
            "--include", "ATTACHMENTS",
        ],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    clusters = result.get("clusters", [])
    if not clusters:
        print("Cluster non trovato.")
        return

    cl = clusters[0]
    print(f"Nome: {cl.get('clusterName', '?')}")
    print(f"Stato: {cl.get('status', '?')}")
    print(f"Container instances registrate: {cl.get('registeredContainerInstancesCount', '?')}")
    print(f"Task running: {cl.get('runningTasksCount', '?')}")
    print(f"Task pending: {cl.get('pendingTasksCount', '?')}")
    print(f"Servizi attivi: {cl.get('activeServicesCount', '?')}")

    # Statistiche
    stats = cl.get("statistics", [])
    if stats:
        print("\n**Statistiche:**")
        for s in stats:
            print(f"  {s.get('name', '?')}: {s.get('value', '?')}")

    # Capacity providers
    providers = cl.get("capacityProviders", [])
    if providers:
        print(f"\nCapacity Providers: {', '.join(providers)}")


def diagnose_config(config: dict):
    """Ispeziona task definition: CPU, memoria, env vars."""
    print("\n### Task Definition Config\n")

    result = aws_cli(
        "ecs", "describe-task-definition",
        ["--task-definition", get_resource(config, "ecs_task_family")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    td = result.get("taskDefinition", {})
    print(f"Famiglia: {td.get('family', '?')}")
    print(f"Revisione: {td.get('revision', '?')}")
    print(f"Task Role: {td.get('taskRoleArn', 'N/A').split('/')[-1]}")
    print(f"Network Mode: {td.get('networkMode', '?')}")

    containers = td.get("containerDefinitions", [])
    for c in containers:
        print(f"\n**Container: {c.get('name', '?')}**")
        print(f"  CPU: {c.get('cpu', '?')}")
        print(f"  Memory (hard limit): {c.get('memory', 'N/A')}")
        print(f"  Memory (soft limit): {c.get('memoryReservation', 'N/A')}")
        print(f"  Essential: {c.get('essential', '?')}")

        # Port mappings
        ports = c.get("portMappings", [])
        if ports:
            port_str = ", ".join(f"{p.get('containerPort', '?')}/{p.get('protocol', 'tcp')}" for p in ports)
            print(f"  Porte: {port_str}")

        # Environment variables
        env_vars = c.get("environment", [])
        if env_vars:
            print(f"  Environment ({len(env_vars)} vars):")
            for ev in sorted(env_vars, key=lambda x: x.get("name", "")):
                name = ev.get("name", "?")
                value = ev.get("value", "?")
                # Nascondi valori sensibili
                if any(sensitive in name.upper() for sensitive in ["SECRET", "KEY", "TOKEN", "PASSWORD", "ARN"]):
                    value = "***REDACTED***"
                print(f"    {name}={value}")

        # Health check
        hc = c.get("healthCheck")
        if hc:
            print(f"  Health check: {' '.join(hc.get('command', []))}")
            print(f"    Interval: {hc.get('interval', '?')}s, Timeout: {hc.get('timeout', '?')}s, Retries: {hc.get('retries', '?')}")


def _get_cloudwatch_metrics(config: dict, namespace: str, metric_name: str,
                            dimensions: list, hours: int = 24, period: int = 3600) -> tuple:
    """Recupera metriche CloudWatch. Ritorna (values, timestamps)."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)

    dim_args = []
    for d in dimensions:
        dim_args.extend(["Name=" + d[0] + ",Value=" + d[1]])

    result = aws_cli(
        "cloudwatch", "get-metric-statistics",
        [
            "--namespace", namespace,
            "--metric-name", metric_name,
            "--start-time", start.strftime("%Y-%m-%dT%H:%M:%S"),
            "--end-time", now.strftime("%Y-%m-%dT%H:%M:%S"),
            "--period", str(period),
            "--statistics", "Average",
            "--dimensions",
        ] + dim_args,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result or not result.get("Datapoints"):
        return [], []

    # Ordina per timestamp
    points = sorted(result["Datapoints"], key=lambda x: x["Timestamp"])
    values = [p.get("Average", 0) for p in points]
    timestamps = [p["Timestamp"][:16] for p in points]
    return values, timestamps


def diagnose_instances(config: dict):
    """Analizza le EC2 container instances del cluster."""
    print("\n### EC2 Container Instances\n")

    cluster = get_resource(config, "ecs_cluster")
    profile = config["aws_profile"]
    region = config["region"]

    # Lista container instances
    result = aws_cli(
        "ecs", "list-container-instances",
        ["--cluster", cluster],
        profile=profile, region=region,
    )

    if "error" in result:
        print(f"ERRORE: {result['error']}")
        return

    ci_arns = result.get("containerInstanceArns", [])
    if not ci_arns:
        print("Nessuna container instance registrata (Fargate?).")
        return

    # Dettagli container instances
    detail = aws_cli(
        "ecs", "describe-container-instances",
        ["--cluster", cluster, "--container-instances"] + ci_arns,
        profile=profile, region=region,
    )

    if "error" in detail:
        print(f"ERRORE: {detail['error']}")
        return

    instances = detail.get("containerInstances", [])
    ec2_ids = []
    rows = []
    for ci in instances:
        ec2_id = ci.get("ec2InstanceId", "?")
        ec2_ids.append(ec2_id)
        status = ci.get("status", "?")
        running = ci.get("runningTasksCount", 0)
        pending = ci.get("pendingTasksCount", 0)
        agent_connected = ci.get("agentConnected", False)

        # Risorse registrate vs rimanenti
        registered = {r["name"]: r["integerValue"] for r in ci.get("registeredResources", [])
                      if r["type"] == "INTEGER"}
        remaining = {r["name"]: r["integerValue"] for r in ci.get("remainingResources", [])
                     if r["type"] == "INTEGER"}

        cpu_reg = registered.get("CPU", 0)
        cpu_rem = remaining.get("CPU", 0)
        mem_reg = registered.get("MEMORY", 0)
        mem_rem = remaining.get("MEMORY", 0)

        cpu_used_pct = ((cpu_reg - cpu_rem) / cpu_reg * 100) if cpu_reg else 0
        mem_used_pct = ((mem_reg - mem_rem) / mem_reg * 100) if mem_reg else 0

        rows.append([
            ec2_id,
            status,
            "Si" if agent_connected else "No",
            f"{running}/{pending}",
            f"{cpu_reg - cpu_rem}/{cpu_reg} ({cpu_used_pct:.0f}%)",
            f"{(mem_reg - mem_rem)}MB/{mem_reg}MB ({mem_used_pct:.0f}%)",
        ])

    print(format_table(
        ["EC2 Instance", "Stato", "Agent", "Task Run/Pend", "CPU usata/tot", "Memoria usata/tot"],
        rows,
    ))

    # Dettagli EC2
    if ec2_ids and ec2_ids[0] != "?":
        ec2_result = aws_cli(
            "ec2", "describe-instances",
            ["--instance-ids"] + ec2_ids,
            profile=profile, region=region,
        )
        if "error" not in ec2_result:
            reservations = ec2_result.get("Reservations", [])
            for res in reservations:
                for inst in res.get("Instances", []):
                    iid = inst.get("InstanceId", "?")
                    itype = inst.get("InstanceType", "?")
                    state = inst.get("State", {}).get("Name", "?")
                    launch = str(inst.get("LaunchTime", "?"))[:19]
                    az = inst.get("Placement", {}).get("AvailabilityZone", "?")
                    print(f"\n  {iid}: {itype} | {state} | AZ: {az} | Avviata: {launch}")


def diagnose_metrics(config: dict, hours: int = 24):
    """Recupera metriche CPU e Memory del servizio ECS dalle ultime ore."""
    period_label = f"ultime {hours}h"
    print(f"\n### Metriche ECS ({period_label})\n")

    cluster = get_resource(config, "ecs_cluster")
    service = get_resource(config, "ecs_service")

    # Periodo: 1 datapoint ogni ora per 24h, ogni 6h per 7d
    period = 3600 if hours <= 48 else 21600

    # CPU Utilization (servizio)
    cpu_vals, cpu_ts = _get_cloudwatch_metrics(
        config, "AWS/ECS", "CPUUtilization",
        [("ClusterName", cluster), ("ServiceName", service)],
        hours=hours, period=period,
    )
    if cpu_vals:
        print(format_metric_chart("CPU", cpu_vals, cpu_ts, unit="%"))
    else:
        print("  CPU: (nessun dato CloudWatch disponibile)")

    print()

    # Memory Utilization (servizio)
    mem_vals, mem_ts = _get_cloudwatch_metrics(
        config, "AWS/ECS", "MemoryUtilization",
        [("ClusterName", cluster), ("ServiceName", service)],
        hours=hours, period=period,
    )
    if mem_vals:
        print(format_metric_chart("Memoria", mem_vals, mem_ts, unit="%"))
    else:
        print("  Memoria: (nessun dato CloudWatch disponibile)")


def main():
    parser = argparse.ArgumentParser(
        description="AWS ECS Diagnose - Diagnosi approfondita ECS",
    )
    parser.add_argument("--project", required=True, help="Nome progetto nella KB")
    parser.add_argument("--env", required=True, choices=["dev", "prod"], help="Ambiente")
    parser.add_argument("--mode", default="all",
                        choices=["deployment", "task-failure", "capacity", "instances", "metrics", "config", "all"],
                        help="Cosa investigare (default: all)")
    parser.add_argument("--hours", type=int, default=24,
                        help="Finestra metriche in ore (default: 24)")
    parser.add_argument("--kb-root", help="Path root KB (auto-detect se omesso)")
    args = parser.parse_args()

    config = load_config(args.project, args.env, args.kb_root)

    print(f"\n## AWS ECS DIAGNOSE — {args.project} ({args.env})")
    print(f"Cluster: {get_resource(config, 'ecs_cluster')}")
    print(f"Servizio: {get_resource(config, 'ecs_service')}")

    if args.mode in ("deployment", "all"):
        diagnose_deployment(config)
    if args.mode in ("instances", "all"):
        diagnose_instances(config)
    if args.mode in ("metrics", "all"):
        diagnose_metrics(config, hours=args.hours)
    if args.mode in ("task-failure", "all"):
        diagnose_task_failure(config)
    if args.mode in ("capacity", "all"):
        diagnose_capacity(config)
    if args.mode in ("config", "all"):
        diagnose_config(config)


if __name__ == "__main__":
    main()
