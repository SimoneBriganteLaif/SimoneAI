#!/usr/bin/env python3
"""
Orchestratore analisi repository LAIF.

Esegue tutti i check su un singolo repo e produce un JSON strutturato.

Uso:
    python3 analyze.py --path /path/to/repo [--baseline baseline.json] [--output output/]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Aggiungi la directory corrente al path per import dei check
sys.path.insert(0, str(Path(__file__).parent))

from checks import versioning, datamodel, frontend_pages, frontend_components
from checks import api_routes, dependencies, background_tasks, git_stats


def load_baseline(baseline_path: str) -> dict:
    with open(baseline_path) as f:
        return json.load(f)


def analyze(repo_path: str, baseline: dict) -> dict:
    """Esegue tutti i check su un repository."""
    repo_name = Path(repo_path).name

    result = {
        "repo": repo_name,
        "path": str(Path(repo_path).resolve()),
        "analyzed_at": datetime.now().isoformat(),
        "baseline_version": baseline.get("version", "unknown"),
    }

    checks = [
        ("versioning", versioning),
        ("datamodel", datamodel),
        ("frontend_pages", frontend_pages),
        ("frontend_components", frontend_components),
        ("api_routes", api_routes),
        ("dependencies", dependencies),
        ("background_tasks", background_tasks),
        ("git_stats", git_stats),
    ]

    for name, module in checks:
        try:
            result[name] = module.run(repo_path, baseline)
        except Exception as e:
            result[name] = {"error": str(e)}
            print(f"  ERRORE in {name}: {e}", file=sys.stderr)

    return result


def print_summary(result: dict):
    """Stampa un riepilogo leggibile."""
    print(f"\n{'='*60}")
    print(f"ANALISI: {result['repo']}")
    print(f"{'='*60}")

    v = result.get("versioning", {})
    print(f"\nA. Template: v{v.get('template_version', '?')} (baseline: {v.get('baseline_version', '?')})")
    delta = v.get("delta", {})
    if delta and delta.get("behind"):
        print(f"   Delta: {delta.get('minor', '?')} minor indietro")

    dm = result.get("datamodel", {})
    print(f"\nB. Data model: {dm.get('custom_table_count', 0)} tabelle custom, {dm.get('materialized_view_count', 0)} materialized views")

    fp = result.get("frontend_pages", {})
    print(f"\nC. Frontend: {fp.get('custom_page_count', 0)} pagine custom, {fp.get('custom_modal_count', 0)} modali custom")
    for p in fp.get("custom_pages", []):
        print(f"   {p['route']}")

    fc = result.get("frontend_components", {})
    print(f"\nD. Componenti: {fc.get('ds_component_count', 0)} DS usati, {fc.get('custom_component_count', 0)} custom")
    ds_top = list(fc.get("ds_components_used", {}).items())[:10]
    if ds_top:
        print(f"   Top DS: {', '.join(f'{n}({c})' for n, c in ds_top)}")

    api = result.get("api_routes", {})
    print(f"\nE. API: {api.get('custom_endpoint_count', 0)} endpoint custom ({api.get('router_builder_count', 0)} RouterBuilder, {api.get('manual_count', 0)} manuali)")

    deps = result.get("dependencies", {})
    print(f"\nF. Dipendenze extra: {deps.get('extra_backend_count', 0)} backend, {deps.get('extra_frontend_count', 0)} frontend")

    bg = result.get("background_tasks", {})
    print(f"\nG. Background: {bg.get('background_task_count', 0)} task, {bg.get('etl_pipeline_count', 0)} ETL, {bg.get('ecs_job_count', 0)} ECS jobs")

    gs = result.get("git_stats", {})
    print(f"\nH. Git: {gs.get('contributor_count', 0)} contributor")
    for c in gs.get("contributors", [])[:5]:
        print(f"   {c['name']}: {c['commits']} commit")
    last = gs.get("last_commit")
    if last:
        print(f"   Ultimo: {last['date'][:10]} — {last['message'][:60]}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Analisi repository LAIF")
    parser.add_argument("--path", required=True, help="Path del repository")
    parser.add_argument("--baseline", default=str(Path(__file__).parent / "baseline.json"),
                        help="Path al baseline.json")
    parser.add_argument("--output", help="Directory output per il JSON")
    parser.add_argument("--quiet", action="store_true", help="Solo JSON, niente summary")
    args = parser.parse_args()

    repo_path = Path(args.path).resolve()
    if not repo_path.exists():
        print(f"ERRORE: path non trovato: {repo_path}", file=sys.stderr)
        sys.exit(1)

    baseline = load_baseline(args.baseline)
    result = analyze(str(repo_path), baseline)

    if not args.quiet:
        print_summary(result)

    # Salva JSON
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{result['repo']}.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Salvato: {output_file}")
    else:
        # Stampa JSON su stdout se quiet
        if args.quiet:
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
