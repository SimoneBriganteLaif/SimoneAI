"""G. ETL e background task."""

import re
from pathlib import Path

TASK_PATTERNS = {
    "repeat_every": re.compile(r'repeat_every'),
    "BackgroundTask": re.compile(r'BackgroundTask'),
    "asyncio_task": re.compile(r'asyncio\.create_task'),
    "scheduler": re.compile(r'APScheduler|schedule\.\w+'),
    "celery": re.compile(r'from celery|import celery', re.IGNORECASE),
}

# ETL: solo indicatori forti, non parole generiche
ETL_STRONG_INDICATORS = {
    "external_db": re.compile(r'pyodbc|pymssql|cx_Oracle|oracledb|ibm_db|pymongo'),
    "etl_import": re.compile(r'from.+etl|import.+etl', re.IGNORECASE),
}


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)

    tasks = []
    etl_pipelines = []
    ecs_jobs = []

    backend_src = repo / "backend" / "src" / "app"
    if not backend_src.exists():
        return {"background_tasks": [], "etl_pipelines": [], "ecs_jobs": []}

    # G1: Background task
    for py_file in backend_src.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        rel_path = str(py_file.relative_to(repo))

        for pattern_name, pattern in TASK_PATTERNS.items():
            if pattern.search(content):
                tasks.append({"type": pattern_name, "file": rel_path})

    # G2: ETL pipeline — directory esplicite + driver DB esterni
    # Cerca directory etl/ nel progetto
    etl_dirs = ["etl", "import_storico", "data_import", "sync", "ingestion"]
    for dirname in etl_dirs:
        etl_dir = backend_src / dirname
        if etl_dir.exists() and etl_dir.is_dir():
            py_files = list(etl_dir.rglob("*.py"))
            if py_files:
                etl_pipelines.append({
                    "type": "etl_directory",
                    "directory": str(etl_dir.relative_to(repo)),
                    "file_count": len(py_files),
                })

    # Cerca driver DB esterni nel codice (indicatori forti di ETL)
    for py_file in backend_src.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        rel_path = str(py_file.relative_to(repo))
        for indicator_name, pattern in ETL_STRONG_INDICATORS.items():
            if pattern.search(content):
                etl_pipelines.append({"type": indicator_name, "file": rel_path})
                break

    # G3: Job ECS/Fargate
    # Dockerfile multipli (escludi quelli standard: backend/Dockerfile, db/Dockerfile)
    standard_dockerfiles = {"backend/Dockerfile", "db/Dockerfile"}
    for df in repo.glob("**/Dockerfile*"):
        if "node_modules" in str(df):
            continue
        rel = str(df.relative_to(repo))
        if rel not in standard_dockerfiles:
            ecs_jobs.append({"type": "extra_dockerfile", "file": rel})

    # Entry point CLI alternativi (typer)
    for py_file in backend_src.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        if "typer" in content and ("app = typer" in content or "def main(" in content):
            rel = str(py_file.relative_to(repo))
            ecs_jobs.append({"type": "cli_entrypoint", "file": rel})

    return {
        "background_tasks": tasks,
        "background_task_count": len(tasks),
        "etl_pipelines": etl_pipelines,
        "etl_pipeline_count": len(etl_pipelines),
        "ecs_jobs": ecs_jobs,
        "ecs_job_count": len(ecs_jobs),
    }
