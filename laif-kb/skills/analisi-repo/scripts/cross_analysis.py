#!/usr/bin/env python3
"""
Analisi cross-progetto (Sezione I).

Legge tutti i JSON di analisi e produce metriche aggregate.

Uso:
    python3 cross_analysis.py --input output/ [--output output/cross_analysis.json]
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_analyses(input_dir: str) -> list:
    analyses = []
    for f in sorted(Path(input_dir).glob("*.json")):
        if f.name == "cross_analysis.json":
            continue
        try:
            analyses.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            pass
    return analyses


def ds_impact_matrix(analyses: list) -> dict:
    """I1: Matrice componente DS → progetti che lo usano."""
    matrix = defaultdict(list)
    for a in analyses:
        repo = a["repo"]
        for comp in a.get("frontend_components", {}).get("ds_components_used", {}):
            matrix[comp].append(repo)

    # Ordina per numero di progetti (decrescente)
    result = {}
    for comp, repos in sorted(matrix.items(), key=lambda x: -len(x[1])):
        result[comp] = {"repos_count": len(repos), "repos": repos}
    return result


def recurring_custom_components(analyses: list) -> list:
    """I2: Componenti custom con nome simile in 2+ progetti."""
    # Raccogli nomi file dei componenti custom
    comp_names = defaultdict(list)
    for a in analyses:
        repo = a["repo"]
        for comp_file in a.get("frontend_components", {}).get("custom_components", []):
            # Estrai nome file senza path
            name = Path(comp_file).stem
            comp_names[name].append(repo)

    # Filtra quelli in 2+ progetti
    recurring = []
    for name, repos in sorted(comp_names.items(), key=lambda x: -len(x[1])):
        if len(repos) >= 2:
            recurring.append({
                "component": name,
                "repos_count": len(repos),
                "repos": repos,
            })
    return recurring


def common_libs(analyses: list) -> dict:
    """I3: Librerie extra non-template più diffuse."""
    backend_counter = Counter()
    frontend_counter = Counter()

    for a in analyses:
        for dep in a.get("dependencies", {}).get("extra_backend", []):
            backend_counter[dep["name"]] += 1
        for dep in a.get("dependencies", {}).get("extra_frontend", []):
            frontend_counter[dep["name"]] += 1

    return {
        "backend": [{"name": n, "count": c} for n, c in backend_counter.most_common(20)],
        "frontend": [{"name": n, "count": c} for n, c in frontend_counter.most_common(20)],
    }


def integration_map(analyses: list) -> dict:
    """I4: Integrazioni esterne ricorrenti (basato su dipendenze extra)."""
    # Mappa pacchetti noti a servizi
    known_integrations = {
        "openai": "OpenAI", "pgvector": "OpenAI/Vectors",
        "pymssql": "MSSQL", "pyodbc": "ODBC", "cx_Oracle": "Oracle", "oracledb": "Oracle",
        "openpyxl": "Excel Processing", "xlsxwriter": "Excel Processing",
        "weasyprint": "PDF Generation", "pymupdf": "PDF Processing",
        "playwright": "Web Scraping", "selenium": "Web Scraping",
        "msgraph-sdk": "Microsoft Graph", "O365": "Microsoft 365",
        "google-api-python-client": "Google APIs",
        "elevenlabs": "ElevenLabs", "telnyx": "Telnyx",
        "ortools": "OR-Tools",
    }

    integrations = defaultdict(list)
    for a in analyses:
        repo = a["repo"]
        for dep in a.get("dependencies", {}).get("extra_backend", []):
            name_lower = dep["name"].lower().replace("-", "_")
            for key, service in known_integrations.items():
                if key in name_lower:
                    integrations[service].append(repo)
                    break

    result = {}
    for service, repos in sorted(integrations.items(), key=lambda x: -len(x[1])):
        result[service] = {"repos_count": len(repos), "repos": list(set(repos))}
    return result


def drift_ranking(analyses: list) -> list:
    """I5: Classifica progetti per urgenza aggiornamento."""
    ranking = []
    for a in analyses:
        v = a.get("versioning", {})
        delta = v.get("delta", {})
        template_files = len(v.get("modified_template_files", []))

        minor_behind = abs(delta.get("minor", 0)) if delta and delta.get("minor") is not None else 0
        score = minor_behind * 2 + template_files

        if score > 0:
            ranking.append({
                "repo": a["repo"],
                "template_version": v.get("template_version"),
                "minor_behind": minor_behind,
                "modified_template_files": template_files,
                "score": score,
            })

    ranking.sort(key=lambda x: -x["score"])
    return ranking


def main():
    parser = argparse.ArgumentParser(description="Analisi cross-progetto LAIF")
    parser.add_argument("--input", required=True, help="Directory con i JSON")
    parser.add_argument("--output", default=None, help="Path output JSON")
    args = parser.parse_args()

    analyses = load_analyses(args.input)
    if not analyses:
        print("Nessuna analisi trovata")
        return

    result = {
        "total_repos": len(analyses),
        "ds_impact_matrix": ds_impact_matrix(analyses),
        "recurring_custom_components": recurring_custom_components(analyses),
        "common_libs": common_libs(analyses),
        "integration_map": integration_map(analyses),
        "drift_ranking": drift_ranking(analyses),
    }

    output_path = args.output or str(Path(args.input) / "cross_analysis.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Cross-analysis: {output_path} ({len(analyses)} repos)")

    # Summary
    print(f"\n--- Cross-analysis Summary ---")
    print(f"DS Components: {len(result['ds_impact_matrix'])} componenti tracciati")
    print(f"Recurring custom: {len(result['recurring_custom_components'])} componenti in 2+ progetti")
    cl = result["common_libs"]
    if cl["backend"]:
        top_be = ", ".join(l["name"] + "(" + str(l["count"]) + ")" for l in cl["backend"][:5])
        print(f"Top lib backend: {top_be}")
    if cl["frontend"]:
        top_fe = ", ".join(l["name"] + "(" + str(l["count"]) + ")" for l in cl["frontend"][:5])
        print(f"Top lib frontend: {top_fe}")
    dr = result["drift_ranking"]
    if dr:
        print(f"Drift ranking top 5:")
        for r in dr[:5]:
            print(f"  {r['repo']}: v{r['template_version']} ({r['minor_behind']} minor behind)")


if __name__ == "__main__":
    main()
