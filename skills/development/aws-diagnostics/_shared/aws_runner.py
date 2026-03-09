"""
Wrapper per comandi AWS CLI via subprocess.

Tutti i comandi sono READ-ONLY. Nessun comando di scrittura e' permesso.
"""

import json
import subprocess
import sys
import time

# Whitelist comandi read-only permessi
ALLOWED_COMMANDS = {
    "ecs": ["describe-services", "describe-tasks", "describe-clusters",
            "describe-task-definition", "list-tasks", "list-services",
            "list-container-instances", "describe-container-instances"],
    "ec2": ["describe-instances"],
    "logs": ["describe-log-groups", "describe-log-streams", "get-log-events",
             "start-query", "get-query-results"],
    "rds": ["describe-db-instances", "describe-db-log-files",
            "download-db-log-file-portion", "describe-db-parameters",
            "describe-db-parameter-groups"],
    "s3api": ["list-buckets", "list-objects-v2", "head-bucket",
              "get-bucket-location"],
    "s3": ["ls"],
    "cloudwatch": ["get-metric-statistics", "get-metric-data", "list-metrics"],
}

DEFAULT_TIMEOUT = 30  # secondi


def _validate_command(service: str, command: str):
    """Verifica che il comando sia nella whitelist read-only."""
    allowed = ALLOWED_COMMANDS.get(service, [])
    if command not in allowed:
        print(f"ERRORE SICUREZZA: comando '{service} {command}' non nella whitelist read-only.")
        print(f"Comandi permessi per {service}: {', '.join(allowed)}")
        sys.exit(1)


def aws_cli(service: str, command: str, args: list = None,
            profile: str = None, region: str = None,
            timeout: int = DEFAULT_TIMEOUT, output_json: bool = True) -> dict:
    """
    Esegue un comando AWS CLI e ritorna il risultato.

    Args:
        service: servizio AWS (es. 'ecs', 'rds', 'logs')
        command: comando (es. 'describe-services')
        args: argomenti aggiuntivi come lista
        profile: nome profilo AWS CLI (obbligatorio)
        region: regione AWS (obbligatorio)
        timeout: timeout in secondi
        output_json: se True, parsa output come JSON

    Returns:
        dict con il risultato parsato, oppure {"raw_output": str} se non JSON.
        In caso di errore: {"error": str, "exit_code": int}
    """
    _validate_command(service, command)

    if not profile:
        print("ERRORE: profilo AWS non specificato. Usa --profile o configura aws-config.yaml")
        sys.exit(1)
    if not region:
        print("ERRORE: regione AWS non specificata.")
        sys.exit(1)

    cmd = ["aws", service, command, "--profile", profile, "--region", region]

    if output_json and service != "s3":
        cmd.extend(["--output", "json"])

    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout dopo {timeout}s: {' '.join(cmd)}", "exit_code": -1}
    except FileNotFoundError:
        return {"error": "AWS CLI non trovata. Installa: https://aws.amazon.com/cli/", "exit_code": -1}

    if result.returncode != 0:
        error_msg = result.stderr.strip()
        # Semplifica messaggi di errore comuni
        if "could not be found" in error_msg or "does not exist" in error_msg:
            return {"error": f"Risorsa non trovata: {error_msg}", "exit_code": result.returncode}
        if "Unable to locate credentials" in error_msg:
            return {"error": f"Credenziali non trovate per profilo '{profile}'", "exit_code": result.returncode}
        if "ExpiredToken" in error_msg:
            return {"error": f"Token scaduto per profilo '{profile}'. Rinnova le credenziali.", "exit_code": result.returncode}
        return {"error": error_msg, "exit_code": result.returncode}

    if not output_json or service == "s3":
        return {"raw_output": result.stdout.strip()}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw_output": result.stdout.strip()}


def logs_insights_query(log_group: str, query: str,
                        start_time: int, end_time: int,
                        profile: str, region: str,
                        max_wait: int = 30, poll_interval: int = 3) -> dict:
    """
    Esegue una query CloudWatch Logs Insights con polling automatico.

    Args:
        log_group: nome del log group
        query: query in sintassi Logs Insights
        start_time: epoch timestamp inizio
        end_time: epoch timestamp fine
        profile: profilo AWS
        region: regione AWS
        max_wait: tempo massimo di attesa in secondi
        poll_interval: intervallo tra i poll in secondi

    Returns:
        dict con:
          - results: lista di risultati (ogni risultato e' una lista di {field, value})
          - statistics: statistiche della query
          - status: stato finale (Complete, Failed, etc.)
        oppure {"error": str} in caso di errore.
    """
    # Step 1: Start query
    start_result = aws_cli("logs", "start-query", [
        "--log-group-name", log_group,
        "--start-time", str(start_time),
        "--end-time", str(end_time),
        "--query-string", query,
    ], profile=profile, region=region)

    if "error" in start_result:
        return start_result

    query_id = start_result.get("queryId")
    if not query_id:
        return {"error": "start-query non ha ritornato queryId"}

    # Step 2: Poll for results
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval

        result = aws_cli("logs", "get-query-results", [
            "--query-id", query_id,
        ], profile=profile, region=region)

        if "error" in result:
            return result

        status = result.get("status", "Unknown")

        if status == "Complete":
            return {
                "results": result.get("results", []),
                "statistics": result.get("statistics", {}),
                "status": "Complete",
            }
        elif status in ("Failed", "Cancelled", "Timeout"):
            return {"error": f"Query terminata con stato: {status}", "status": status}
        # else: Running o Scheduled, continua polling

    return {"error": f"Timeout: query non completata in {max_wait}s", "status": "Timeout"}


def s3_ls(bucket: str, profile: str, region: str, recursive: bool = True) -> dict:
    """
    Esegue 'aws s3 ls' su un bucket con --summarize.

    Returns:
        dict con raw_output (testo formattato da AWS CLI) o error.
    """
    args = [f"s3://{bucket}"]
    if recursive:
        args.extend(["--recursive", "--human-readable", "--summarize"])
    return aws_cli("s3", "ls", args, profile=profile, region=region, output_json=False)
