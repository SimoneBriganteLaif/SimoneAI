"""F. Dipendenze: librerie extra backend e frontend vs template baseline."""

import json
import re
from pathlib import Path


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)

    extra_backend = _diff_backend(repo, baseline)
    extra_frontend = _diff_frontend(repo, baseline)

    return {
        "extra_backend": extra_backend,
        "extra_backend_count": len(extra_backend),
        "extra_frontend": extra_frontend,
        "extra_frontend_count": len(extra_frontend),
    }


def _diff_backend(repo: Path, baseline: dict) -> list:
    """Trova dipendenze backend non nel template."""
    pyproject = repo / "backend" / "pyproject.toml"
    if not pyproject.exists():
        return []

    content = pyproject.read_text(encoding="utf-8")

    # Parse dipendenze dal pyproject.toml (semplificato, senza toml lib)
    project_deps = _parse_pyproject_deps(content)

    baseline_deps = set()
    for name in baseline.get("backend_deps_core", {}):
        # Normalizza: rimuovi extras [tz], [bcrypt] etc
        clean = re.sub(r'\[.*?\]', '', name).strip().lower()
        baseline_deps.add(clean)
    for group_deps in baseline.get("backend_deps_optional", {}).values():
        for dep in group_deps:
            baseline_deps.add(dep.lower())

    extra = []
    for dep_name, dep_version in project_deps:
        clean_name = re.sub(r'\[.*?\]', '', dep_name).strip().lower()
        if clean_name not in baseline_deps:
            extra.append({"name": dep_name, "version": dep_version})

    return extra


def _diff_frontend(repo: Path, baseline: dict) -> list:
    """Trova dipendenze frontend non nel template."""
    pkg_json = repo / "frontend" / "package.json"
    if not pkg_json.exists():
        return []

    try:
        pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []

    all_deps = {}
    all_deps.update(pkg.get("dependencies", {}))
    all_deps.update(pkg.get("devDependencies", {}))

    baseline_fe = set(baseline.get("frontend_deps", {}).keys())

    extra = []
    for name, version in sorted(all_deps.items()):
        if name not in baseline_fe:
            extra.append({"name": name, "version": version})

    return extra


def _parse_pyproject_deps(content: str) -> list:
    """Parse semplificato delle dipendenze da pyproject.toml."""
    deps = []
    in_deps = False

    for line in content.split("\n"):
        stripped = line.strip()

        if stripped == "dependencies = [":
            in_deps = True
            continue
        if in_deps and stripped == "]":
            in_deps = False
            continue

        if in_deps and stripped.startswith('"'):
            # Estrai nome e versione
            dep_str = stripped.strip('",')
            match = re.match(r'^([a-zA-Z0-9_\-\[\]\.]+)\s*(.*)', dep_str)
            if match:
                deps.append((match.group(1), match.group(2)))

    return deps
