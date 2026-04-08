"""E. Backend API: endpoint custom, RouterBuilder vs manuali."""

import re
from pathlib import Path


ROUTE_DECORATOR = re.compile(
    r'@\w+\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
)
ROUTER_BUILDER = re.compile(r'RouterBuilder\s*\(')
ROUTER_BUILDER_METHOD = re.compile(
    r'\.(get_by_id|search|create|update|delete|download|upload|export|export_s3|'
    r'batch_create|batch_update|batch_delete|batch_upload|custom)\s*\('
)


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)
    baseline_prefixes = set(baseline.get("api_prefixes", []))

    endpoints = []
    by_controller = {}
    router_builder_count = 0
    manual_count = 0

    # Cerca solo in app/ (non template/)
    app_dir = repo / "backend" / "src" / "app"
    if not app_dir.exists():
        return {"custom_endpoints": [], "by_controller": {}, "router_builder": 0, "manual": 0}

    for py_file in app_dir.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        rel_path = str(py_file.relative_to(repo))
        controller_name = py_file.stem

        file_endpoints = []

        # Decoratori manuali
        for match in ROUTE_DECORATOR.finditer(content):
            method = match.group(1).upper()
            path = match.group(2)

            # Filtra endpoint del template (basato sul prefix)
            if not _is_template_prefix(path, baseline_prefixes):
                file_endpoints.append({
                    "method": method,
                    "path": path,
                    "type": "manual",
                    "file": rel_path,
                })
                manual_count += 1

        # RouterBuilder
        if ROUTER_BUILDER.search(content):
            methods = ROUTER_BUILDER_METHOD.findall(content)
            method_map = {
                "get_by_id": "GET", "search": "POST", "create": "POST",
                "update": "PUT", "delete": "DELETE", "download": "GET",
                "upload": "POST", "export": "POST", "export_s3": "POST",
                "batch_create": "POST", "batch_update": "PUT",
                "batch_delete": "DELETE", "batch_upload": "POST",
                "custom": "CUSTOM",
            }
            for m in methods:
                file_endpoints.append({
                    "method": method_map.get(m, "UNKNOWN"),
                    "path": f"[RouterBuilder:{m}]",
                    "type": "router_builder",
                    "file": rel_path,
                })
                router_builder_count += 1

        if file_endpoints:
            endpoints.extend(file_endpoints)
            by_controller[controller_name] = len(file_endpoints)

    # Breakdown per metodo
    by_method = {}
    for ep in endpoints:
        by_method[ep["method"]] = by_method.get(ep["method"], 0) + 1

    return {
        "custom_endpoints": endpoints,
        "custom_endpoint_count": len(endpoints),
        "by_method": by_method,
        "by_controller": dict(sorted(by_controller.items(), key=lambda x: -x[1])),
        "router_builder_count": router_builder_count,
        "manual_count": manual_count,
    }


def _is_template_prefix(path: str, baseline_prefixes: set) -> bool:
    """Verifica se un path appartiene a un prefix del template."""
    for prefix in baseline_prefixes:
        if path.startswith(prefix):
            return True
    return False
