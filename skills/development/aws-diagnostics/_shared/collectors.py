"""
Funzioni di raccolta dati AWS — layer intermedio per report HTML e CLI.

Ogni funzione ritorna un dict strutturato (mai print).
In caso di errore: {"error": str}.
"""

import time
from datetime import datetime, timedelta, timezone

from config import get_resource
from aws_runner import aws_cli, logs_insights_query, s3_ls


# ---------------------------------------------------------------------------
# Helper generico CloudWatch Metrics
# ---------------------------------------------------------------------------

def _get_cloudwatch_metrics(config: dict, namespace: str, metric_name: str,
                            dimensions: list, hours: int = 24,
                            period: int = 3600) -> dict:
    """
    Recupera metriche CloudWatch.

    Args:
        dimensions: lista di tuple (Name, Value)

    Returns:
        {"values": [...], "timestamps": [...]} oppure {"error": str}
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)

    dim_args = []
    for d in dimensions:
        dim_args.append("Name=" + d[0] + ",Value=" + d[1])

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

    if "error" in result:
        return {"error": result["error"]}

    if not result.get("Datapoints"):
        return {"values": [], "timestamps": []}

    points = sorted(result["Datapoints"], key=lambda x: x["Timestamp"])
    values = [p.get("Average", 0) for p in points]
    timestamps = [p["Timestamp"][:16] for p in points]
    return {"values": values, "timestamps": timestamps}


# ---------------------------------------------------------------------------
# Triage
# ---------------------------------------------------------------------------

def collect_triage(config: dict) -> dict:
    """
    Health check rapido: ECS, RDS, CloudWatch Logs, S3.

    Returns:
        {
            "checks": [{"service": str, "status": str, "detail": str}, ...],
            "verdict": str  ("OK"|"WARN"|"FAIL")
        }
    """
    checks = []

    # ECS
    ecs_result = aws_cli(
        "ecs", "describe-services",
        [
            "--cluster", get_resource(config, "ecs_cluster"),
            "--services", get_resource(config, "ecs_service"),
        ],
        profile=config["aws_profile"],
        region=config["region"],
    )
    if "error" in ecs_result:
        checks.append({"service": "ECS", "status": "FAIL", "detail": ecs_result["error"]})
    else:
        services = ecs_result.get("services", [])
        if not services:
            checks.append({"service": "ECS", "status": "FAIL", "detail": "Servizio non trovato"})
        else:
            svc = services[0]
            status = svc.get("status", "UNKNOWN")
            desired = svc.get("desiredCount", 0)
            running = svc.get("runningCount", 0)
            deployments = svc.get("deployments", [])
            if status != "ACTIVE":
                checks.append({"service": "ECS", "status": "FAIL", "detail": f"Servizio {status}"})
            elif running < desired:
                checks.append({"service": "ECS", "status": "FAIL", "detail": f"{running}/{desired} task running"})
            elif len(deployments) > 1:
                checks.append({"service": "ECS", "status": "WARN",
                               "detail": f"{running}/{desired} task, deployment in corso"})
            else:
                rollout = deployments[0].get("rolloutState", "UNKNOWN") if deployments else "UNKNOWN"
                checks.append({"service": "ECS", "status": "OK",
                               "detail": f"{running}/{desired} task, {rollout}"})

    # RDS
    rds_result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )
    if "error" in rds_result:
        checks.append({"service": "RDS", "status": "FAIL", "detail": rds_result["error"]})
    else:
        instances = rds_result.get("DBInstances", [])
        if not instances:
            checks.append({"service": "RDS", "status": "FAIL", "detail": "Istanza non trovata"})
        else:
            db = instances[0]
            db_status = db.get("DBInstanceStatus", "unknown")
            db_class = db.get("DBInstanceClass", "unknown")
            if db_status == "available":
                checks.append({"service": "RDS", "status": "OK",
                               "detail": f"{db_status}, {db_class}"})
            elif db_status in ("backing-up", "maintenance", "modifying"):
                checks.append({"service": "RDS", "status": "WARN",
                               "detail": f"{db_status}, {db_class}"})
            else:
                checks.append({"service": "RDS", "status": "FAIL",
                               "detail": f"{db_status}, {db_class}"})

    # CloudWatch Logs — error count last 1h
    now = int(time.time())
    logs_result = logs_insights_query(
        log_group=get_resource(config, "log_group"),
        query="fields @timestamp, @message | filter @message like /ERROR|Exception|Traceback|CRITICAL/ | stats count(*) as error_count",
        start_time=now - 3600,
        end_time=now,
        profile=config["aws_profile"],
        region=config["region"],
    )
    if "error" in logs_result:
        checks.append({"service": "CloudWatch", "status": "WARN",
                       "detail": f"Query fallita: {logs_result['error']}"})
    else:
        error_count = 0
        for row in logs_result.get("results", []):
            for field in row:
                if field.get("field") == "error_count":
                    try:
                        error_count = int(field.get("value", 0))
                    except (ValueError, TypeError):
                        pass
        if error_count == 0:
            checks.append({"service": "CloudWatch", "status": "OK",
                           "detail": "0 errori nell'ultima ora"})
        elif error_count <= 10:
            checks.append({"service": "CloudWatch", "status": "WARN",
                           "detail": f"{error_count} errori nell'ultima ora"})
        else:
            checks.append({"service": "CloudWatch", "status": "FAIL",
                           "detail": f"{error_count} errori nell'ultima ora"})

    # S3 Data bucket
    bucket_name = get_resource(config, "s3_data_bucket")
    s3_result = aws_cli(
        "s3api", "head-bucket",
        ["--bucket", bucket_name],
        profile=config["aws_profile"],
        region=config["region"],
    )
    if "error" in s3_result:
        checks.append({"service": "S3 Data", "status": "FAIL",
                       "detail": "non accessibile"})
    else:
        checks.append({"service": "S3 Data", "status": "OK",
                       "detail": "accessibile"})

    # Verdetto
    statuses = [c["status"] for c in checks]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "WARN" in statuses:
        overall = "WARN"
    else:
        overall = "OK"

    return {"checks": checks, "verdict": overall}


# ---------------------------------------------------------------------------
# ECS
# ---------------------------------------------------------------------------

def collect_ecs_deployment(config: dict) -> dict:
    """
    Returns:
        {
            "deployments": [{"status", "rollout", "running", "desired", "task_def", "updated"}],
            "events": [{"timestamp": str, "message": str}]
        }
    """
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
        return {"error": result["error"]}

    services = result.get("services", [])
    if not services:
        return {"error": "Servizio non trovato"}

    svc = services[0]

    deployments = []
    for d in svc.get("deployments", []):
        deployments.append({
            "status": d.get("status", "?"),
            "rollout": d.get("rolloutState", "?"),
            "running": d.get("runningCount", 0),
            "desired": d.get("desiredCount", 0),
            "task_def": d.get("taskDefinition", "?").split("/")[-1],
            "updated": str(d.get("updatedAt", "?"))[:19],
        })

    events = []
    for ev in svc.get("events", [])[:10]:
        events.append({
            "timestamp": str(ev.get("createdAt", "?"))[:19],
            "message": ev.get("message", ""),
        })

    return {"deployments": deployments, "events": events}


def collect_ecs_task_failures(config: dict) -> dict:
    """
    Returns:
        {"tasks": [{"id", "exit_code", "stop_code", "reason", "started", "stopped"}]}
    """
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
        return {"error": result["error"]}

    task_arns = result.get("taskArns", [])
    if not task_arns:
        return {"tasks": []}

    task_arns = task_arns[:10]
    detail = aws_cli(
        "ecs", "describe-tasks",
        ["--cluster", get_resource(config, "ecs_cluster"), "--tasks"] + task_arns,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in detail:
        return {"error": detail["error"]}

    tasks = []
    for t in detail.get("tasks", []):
        containers = t.get("containers", [])
        exit_code = containers[0].get("exitCode", "?") if containers else "?"
        tasks.append({
            "id": t.get("taskArn", "?").split("/")[-1][:12],
            "exit_code": str(exit_code),
            "stop_code": t.get("stopCode", "?"),
            "reason": t.get("stoppedReason", "?")[:80],
            "started": str(t.get("startedAt", "?"))[:19],
            "stopped": str(t.get("stoppedAt", "?"))[:19],
        })

    return {"tasks": tasks}


def collect_ecs_instances(config: dict) -> dict:
    """
    Returns:
        {
            "container_instances": [{"ec2_id", "status", "agent", "running", "pending",
                                     "cpu_used", "cpu_total", "cpu_pct",
                                     "mem_used_mb", "mem_total_mb", "mem_pct"}],
            "ec2_details": [{"id", "type", "state", "az", "launch_time"}]
        }
    """
    cluster = get_resource(config, "ecs_cluster")
    profile = config["aws_profile"]
    region = config["region"]

    result = aws_cli(
        "ecs", "list-container-instances",
        ["--cluster", cluster],
        profile=profile, region=region,
    )

    if "error" in result:
        return {"error": result["error"]}

    ci_arns = result.get("containerInstanceArns", [])
    if not ci_arns:
        return {"container_instances": [], "ec2_details": []}

    detail = aws_cli(
        "ecs", "describe-container-instances",
        ["--cluster", cluster, "--container-instances"] + ci_arns,
        profile=profile, region=region,
    )

    if "error" in detail:
        return {"error": detail["error"]}

    container_instances = []
    ec2_ids = []
    for ci in detail.get("containerInstances", []):
        ec2_id = ci.get("ec2InstanceId", "?")
        ec2_ids.append(ec2_id)

        registered = {r["name"]: r["integerValue"] for r in ci.get("registeredResources", [])
                      if r["type"] == "INTEGER"}
        remaining = {r["name"]: r["integerValue"] for r in ci.get("remainingResources", [])
                     if r["type"] == "INTEGER"}

        cpu_reg = registered.get("CPU", 0)
        cpu_rem = remaining.get("CPU", 0)
        mem_reg = registered.get("MEMORY", 0)
        mem_rem = remaining.get("MEMORY", 0)

        container_instances.append({
            "ec2_id": ec2_id,
            "status": ci.get("status", "?"),
            "agent": ci.get("agentConnected", False),
            "running": ci.get("runningTasksCount", 0),
            "pending": ci.get("pendingTasksCount", 0),
            "cpu_used": cpu_reg - cpu_rem,
            "cpu_total": cpu_reg,
            "cpu_pct": ((cpu_reg - cpu_rem) / cpu_reg * 100) if cpu_reg else 0,
            "mem_used_mb": mem_reg - mem_rem,
            "mem_total_mb": mem_reg,
            "mem_pct": ((mem_reg - mem_rem) / mem_reg * 100) if mem_reg else 0,
        })

    ec2_details = []
    valid_ids = [i for i in ec2_ids if i != "?"]
    if valid_ids:
        ec2_result = aws_cli(
            "ec2", "describe-instances",
            ["--instance-ids"] + valid_ids,
            profile=profile, region=region,
        )
        if "error" not in ec2_result:
            for res in ec2_result.get("Reservations", []):
                for inst in res.get("Instances", []):
                    ec2_details.append({
                        "id": inst.get("InstanceId", "?"),
                        "type": inst.get("InstanceType", "?"),
                        "state": inst.get("State", {}).get("Name", "?"),
                        "az": inst.get("Placement", {}).get("AvailabilityZone", "?"),
                        "launch_time": str(inst.get("LaunchTime", "?"))[:19],
                    })

    return {"container_instances": container_instances, "ec2_details": ec2_details}


def collect_ecs_metrics(config: dict, hours: int = 24) -> dict:
    """
    Returns:
        {
            "cpu": {"values": [...], "timestamps": [...]},
            "memory": {"values": [...], "timestamps": [...]},
            "hours": int
        }
    """
    cluster = get_resource(config, "ecs_cluster")
    service = get_resource(config, "ecs_service")
    period = 3600 if hours <= 48 else 21600

    cpu = _get_cloudwatch_metrics(
        config, "AWS/ECS", "CPUUtilization",
        [("ClusterName", cluster), ("ServiceName", service)],
        hours=hours, period=period,
    )
    memory = _get_cloudwatch_metrics(
        config, "AWS/ECS", "MemoryUtilization",
        [("ClusterName", cluster), ("ServiceName", service)],
        hours=hours, period=period,
    )

    return {
        "cpu": cpu if "error" not in cpu else {"values": [], "timestamps": []},
        "memory": memory if "error" not in memory else {"values": [], "timestamps": []},
        "hours": hours,
    }


# ---------------------------------------------------------------------------
# RDS
# ---------------------------------------------------------------------------

def collect_rds_status(config: dict) -> dict:
    """
    Returns:
        {"properties": [{"name": str, "value": str}], "raw": dict}
    """
    result = aws_cli(
        "rds", "describe-db-instances",
        ["--db-instance-identifier", get_resource(config, "rds_identifier")],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return {"error": result["error"]}

    instances = result.get("DBInstances", [])
    if not instances:
        return {"error": "Istanza non trovata"}

    db = instances[0]
    endpoint = db.get("Endpoint", {})

    props = [
        {"name": "Stato", "value": db.get("DBInstanceStatus", "?")},
        {"name": "Classe", "value": db.get("DBInstanceClass", "?")},
        {"name": "Engine", "value": f"PostgreSQL {db.get('EngineVersion', '?')}"},
        {"name": "Storage allocato", "value": f"{db.get('AllocatedStorage', '?')} GB"},
        {"name": "Storage max", "value": f"{db.get('MaxAllocatedStorage', 'N/A')} GB"},
        {"name": "Multi-AZ", "value": str(db.get("MultiAZ", False))},
        {"name": "Endpoint", "value": endpoint.get("Address", "?")},
        {"name": "Porta", "value": str(endpoint.get("Port", "?"))},
        {"name": "Backup retention", "value": f"{db.get('BackupRetentionPeriod', '?')} giorni"},
        {"name": "Maintenance window", "value": db.get("PreferredMaintenanceWindow", "?")},
    ]

    return {"properties": props, "raw": db}


def collect_rds_metrics(config: dict, hours: int = 24) -> dict:
    """
    Returns:
        {
            "cpu": {"values", "timestamps"},
            "freeable_memory": {"values", "timestamps"},  (valori in MB)
            "connections": {"values", "timestamps"},
            "read_latency": {"values", "timestamps"},     (valori in ms)
            "write_latency": {"values", "timestamps"},    (valori in ms)
            "hours": int
        }
    """
    rds_id = get_resource(config, "rds_identifier")
    period = 3600 if hours <= 48 else 21600
    dims = [("DBInstanceIdentifier", rds_id)]

    cpu = _get_cloudwatch_metrics(config, "AWS/RDS", "CPUUtilization", dims, hours, period)
    mem = _get_cloudwatch_metrics(config, "AWS/RDS", "FreeableMemory", dims, hours, period)
    conn = _get_cloudwatch_metrics(config, "AWS/RDS", "DatabaseConnections", dims, hours, period)
    rl = _get_cloudwatch_metrics(config, "AWS/RDS", "ReadLatency", dims, hours, period)
    wl = _get_cloudwatch_metrics(config, "AWS/RDS", "WriteLatency", dims, hours, period)

    def safe(m):
        return m if "error" not in m else {"values": [], "timestamps": []}

    # Converti FreeableMemory bytes → MB
    mem_data = safe(mem)
    if mem_data["values"]:
        mem_data = {
            "values": [v / (1024 * 1024) for v in mem_data["values"]],
            "timestamps": mem_data["timestamps"],
        }

    # Converti latenze s → ms
    rl_data = safe(rl)
    if rl_data["values"]:
        rl_data = {"values": [v * 1000 for v in rl_data["values"]], "timestamps": rl_data["timestamps"]}

    wl_data = safe(wl)
    if wl_data["values"]:
        wl_data = {"values": [v * 1000 for v in wl_data["values"]], "timestamps": wl_data["timestamps"]}

    return {
        "cpu": safe(cpu),
        "freeable_memory": mem_data,
        "connections": safe(conn),
        "read_latency": rl_data,
        "write_latency": wl_data,
        "hours": hours,
    }


# ---------------------------------------------------------------------------
# CloudWatch Logs
# ---------------------------------------------------------------------------

QUERY_TEMPLATES = {
    "errors": {
        "description": "Errori ed eccezioni",
        "query": """fields @timestamp, @message, @logStream
| filter @message like /ERROR|Exception|Traceback|CRITICAL/
| sort @timestamp desc
| limit 100""",
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
    "status-codes": {
        "description": "Distribuzione status code HTTP",
        "query": """fields @timestamp, @message
| filter @message like /"status":\\s*\\d{3}|"status_code":\\s*\\d{3}/
| parse @message /"status":\\s*(?<statusCode>\\d{3})/
| stats count(*) as request_count by statusCode
| sort request_count desc""",
    },
    "db-issues": {
        "description": "Problemi connessione database",
        "query": """fields @timestamp, @message
| filter @message like /psycopg|connection refused|timeout|ConnectionError|OperationalError|too many connections|remaining connection slots/
| stats count(*) as occurrences by bin(5m)
| sort @timestamp desc""",
    },
    "recent": {
        "description": "Ultimi log (tail)",
        "query": """fields @timestamp, @message
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


def collect_logs_query(config: dict, query_type: str, time_window: str = "1h") -> dict:
    """
    Returns:
        {
            "query_type": str,
            "description": str,
            "results": [  list of rows, each row is [{"field": str, "value": str}] ],
            "headers": [str],
            "statistics": {"recordsMatched", "recordsScanned", "bytesScanned"},
            "result_count": int
        }
    """
    if query_type not in QUERY_TEMPLATES:
        return {"error": f"Query type sconosciuto: {query_type}"}

    template = QUERY_TEMPLATES[query_type]
    query = template["query"]
    description = template["description"]

    now = int(time.time())
    window_seconds = TIME_WINDOWS.get(time_window, 3600)
    start_time = now - window_seconds

    result = logs_insights_query(
        log_group=get_resource(config, "log_group"),
        query=query,
        start_time=start_time,
        end_time=now,
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in result:
        return {"error": result["error"]}

    results = result.get("results", [])

    # Estrai headers dal primo risultato
    headers = []
    if results:
        for field in results[0]:
            fname = field.get("field", "?")
            if fname != "@ptr":
                headers.append(fname)

    stats = result.get("statistics", {})

    return {
        "query_type": query_type,
        "description": description,
        "results": results,
        "headers": headers,
        "statistics": {
            "recordsMatched": stats.get("recordsMatched", 0),
            "recordsScanned": stats.get("recordsScanned", 0),
            "bytesScanned": stats.get("bytesScanned", 0),
        },
        "result_count": len(results),
    }


# ---------------------------------------------------------------------------
# S3
# ---------------------------------------------------------------------------

def collect_s3_overview(bucket_name: str, config: dict) -> dict:
    """
    Returns:
        {"bucket": str, "summary_lines": [str], "accessible": bool}
    """
    # Check accessibilita
    check = aws_cli(
        "s3api", "head-bucket",
        ["--bucket", bucket_name],
        profile=config["aws_profile"],
        region=config["region"],
    )

    if "error" in check:
        return {"bucket": bucket_name, "accessible": False, "summary_lines": [],
                "error": check["error"]}

    result = s3_ls(bucket_name, profile=config["aws_profile"], region=config["region"])

    if "error" in result:
        return {"bucket": bucket_name, "accessible": True, "summary_lines": [],
                "error": result["error"]}

    output = result.get("raw_output", "")
    summary_lines = []
    if output:
        lines = output.strip().split("\n")
        summary_lines = [l.strip() for l in lines if l.strip().startswith("Total")]

    return {"bucket": bucket_name, "accessible": True, "summary_lines": summary_lines}
