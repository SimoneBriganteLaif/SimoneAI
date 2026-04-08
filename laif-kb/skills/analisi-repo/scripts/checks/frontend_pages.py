"""C. Frontend: pagine custom, alberatura, modali."""

import re
from pathlib import Path


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)
    baseline_routes = set(baseline.get("frontend_routes", []))
    baseline_modals = set(baseline.get("frontend_template_modals", []))

    # Trova la directory app/
    app_dir = repo / "frontend" / "src" / "app"
    if not app_dir.exists():
        app_dir = repo / "frontend" / "app"
    if not app_dir.exists():
        return {"custom_pages": [], "custom_modals": [], "site_tree": ""}

    # C1: Pagine — trova tutti i page.tsx
    all_pages = []
    for page_file in app_dir.rglob("page.tsx"):
        rel_path = page_file.relative_to(app_dir)
        parts = [p for p in rel_path.parts[:-1] if not p.startswith("(")]
        route = "/" + "/".join(parts) if parts else "/"
        depth = len(parts)
        all_pages.append({"route": route, "depth": depth, "file": str(rel_path)})

    # Filtra custom
    custom_pages = [p for p in all_pages if p["route"] not in baseline_routes]
    custom_pages.sort(key=lambda p: p["route"])

    # C2: Alberatura custom
    site_tree = _build_tree(custom_pages)

    # C3: Modali custom
    frontend_dir = repo / "frontend"
    all_modals = []
    for tsx_file in frontend_dir.rglob("*.tsx"):
        if "node_modules" in str(tsx_file):
            continue
        rel_path = str(tsx_file.relative_to(frontend_dir))

        # Escludi qualsiasi cosa in template/
        if rel_path.startswith("template/"):
            continue
        # Escludi file del baseline
        if rel_path in baseline_modals:
            continue

        filename = tsx_file.name
        parent_dir = tsx_file.parent.name

        # Match: file con Modal/Dialog nel NOME, oppure file direttamente in una cartella modals/
        is_modal_file = filename.endswith("Modal.tsx") or filename.endswith("Dialog.tsx")
        is_in_modals_dir = parent_dir == "modals"

        if is_modal_file or is_in_modals_dir:
            all_modals.append(rel_path)

    all_modals.sort()

    return {
        "total_pages": len(all_pages),
        "custom_pages": custom_pages,
        "custom_page_count": len(custom_pages),
        "custom_modals": all_modals,
        "custom_modal_count": len(all_modals),
        "site_tree": site_tree,
    }


def _build_tree(pages: list) -> str:
    """Genera albero indentato delle route."""
    if not pages:
        return ""

    lines = []
    for p in pages:
        indent = "  " * p["depth"]
        name = p["route"].split("/")[-1] or "/"
        lines.append(f"{indent}{name}")
    return "\n".join(lines)
