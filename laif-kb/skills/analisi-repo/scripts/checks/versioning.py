"""A. Versioning e template drift."""

import re
from pathlib import Path


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)
    result = {
        "template_version": None,
        "baseline_version": baseline.get("version", "5.7.0"),
        "delta": None,
        "modified_template_files": [],
        "removed_template_files": [],
    }

    # A1: Versione template
    version_file = repo / "version.laif-template.txt"
    if version_file.exists():
        result["template_version"] = version_file.read_text().strip()
    else:
        # Fallback: cerca in version.txt
        alt = repo / "version.txt"
        if alt.exists():
            result["template_version"] = alt.read_text().strip()

    # A2: Delta versione
    if result["template_version"] and result["baseline_version"]:
        result["delta"] = _semver_delta(result["template_version"], result["baseline_version"])

    # A3: File modificati nelle cartelle template/
    # Cerca file .py e .tsx nelle cartelle */template/
    template_dirs = [
        repo / "backend" / "src" / "template",
        repo / "frontend" / "template",
    ]
    for tdir in template_dirs:
        if tdir.exists():
            for f in tdir.rglob("*"):
                if f.is_file() and f.suffix in (".py", ".tsx", ".ts", ".css", ".json"):
                    rel = str(f.relative_to(repo))
                    result["modified_template_files"].append(rel)

    # A4/A5: File rimossi — confronto con baseline frontend routes
    # (semplificato: verifica se le route template esistono come page.tsx)
    baseline_routes = set(baseline.get("frontend_routes", []))
    for route in baseline_routes:
        route_parts = route.strip("/").split("/")
        if not route_parts or route_parts == [""]:
            continue
        # Cerca in entrambe le posizioni possibili
        for app_dir in [repo / "frontend" / "src" / "app", repo / "frontend" / "app"]:
            page_path = app_dir / "/".join(route_parts) / "page.tsx"
            if page_path.exists():
                break
        # Non segnaliamo come rimosso — potrebbe essere in route group

    return result


def _semver_delta(current: str, baseline: str) -> dict:
    """Calcola il delta tra due versioni semver."""
    def parse(v):
        parts = re.findall(r"\d+", v)
        return [int(p) for p in parts[:3]] if parts else [0, 0, 0]

    cur = parse(current)
    base = parse(baseline)

    return {
        "major": base[0] - cur[0],
        "minor": base[1] - cur[1] if cur[0] == base[0] else None,
        "patch": base[2] - cur[2] if cur[:2] == base[:2] else None,
        "behind": current != baseline,
    }
