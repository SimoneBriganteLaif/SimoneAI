"""D. Frontend componenti: uso laif-ds, componenti custom."""

import re
from pathlib import Path


DS_IMPORT = re.compile(r'import\s*\{([^}]+)\}\s*from\s*["\']laif-ds["\']')


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)

    ds_usage = {}  # componente → count
    custom_components = []

    # Cerca in tutto il frontend (src/ e template/)
    frontend_dir = repo / "frontend"
    if not frontend_dir.exists():
        return {"ds_components_used": {}, "ds_components_not_used": [], "custom_components": []}

    # D1: Componenti laif-ds usati
    for tsx_file in frontend_dir.rglob("*.tsx"):
        if "node_modules" in str(tsx_file):
            continue
        try:
            content = tsx_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        for match in DS_IMPORT.finditer(content):
            components = [c.strip() for c in match.group(1).split(",")]
            for comp in components:
                comp = comp.strip()
                if comp:
                    ds_usage[comp] = ds_usage.get(comp, 0) + 1

    # Anche parse import con singoli apici
    ds_import_single = re.compile(r"import\s*\{([^}]+)\}\s*from\s*'laif-ds'")
    for tsx_file in frontend_dir.rglob("*.tsx"):
        if "node_modules" in str(tsx_file):
            continue
        try:
            content = tsx_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        for match in ds_import_single.finditer(content):
            components = [c.strip() for c in match.group(1).split(",")]
            for comp in components:
                comp = comp.strip()
                if comp and comp not in ds_usage:
                    ds_usage[comp] = 0
                if comp:
                    ds_usage[comp] = ds_usage.get(comp, 0) + 1

    # D2: Componenti DS non usati — richiederebbe la lista completa del DS
    # Per ora lasciamo vuoto, da popolare quando avremo l'elenco completo
    ds_not_used = []

    # D3: Componenti custom — file .tsx in src/features/ e src/components/
    custom_dirs = [
        frontend_dir / "src" / "features",
        frontend_dir / "src" / "components",
    ]
    for cdir in custom_dirs:
        if cdir.exists():
            for tsx_file in cdir.rglob("*.tsx"):
                rel = str(tsx_file.relative_to(frontend_dir))
                custom_components.append(rel)

    custom_components.sort()

    return {
        "ds_components_used": dict(sorted(ds_usage.items(), key=lambda x: -x[1])),
        "ds_component_count": len(ds_usage),
        "ds_components_not_used": ds_not_used,
        "custom_components": custom_components,
        "custom_component_count": len(custom_components),
    }
