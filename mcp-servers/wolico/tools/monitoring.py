"""Tool monitoring: applicazioni ed errori."""

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_post
from helpers import build_search, paginated_search, truncation_warning, safe_call


def _format_app(a: dict) -> str:
    name = a.get("app_name", "N/D")
    domain = a.get("app_domain", "")
    env = a.get("env", "")
    status = a.get("project_status", "")
    off = a.get("flg_turn_off", False)
    partner = a.get("partner") or {}
    cliente = partner.get("name") or partner.get("alias", "") if isinstance(partner, dict) else ""
    health_data = a.get("health") or {}
    health = ""
    if isinstance(health_data, dict):
        checks = []
        for k in ("database", "backend", "frontend"):
            v = health_data.get(k)
            if isinstance(v, dict) and "flg_passed" in v:
                checks.append(f"{k}:{'OK' if v['flg_passed'] else 'FAIL'}")
        health = ", ".join(checks) if checks else ""
    summary_data = a.get("summary") or {}
    summary = ""
    if isinstance(summary_data, dict):
        versions = summary_data.get("versions") or {}
        app_ver = versions.get("app_version", "").strip()
        if app_ver:
            summary = f"v{app_ver}"

    maintainers = a.get("application_maintainers") or []
    maint_names = ", ".join(
        f"{m.get('des_name', '')} {m.get('des_surname', '')}".strip()
        for m in maintainers if isinstance(m, dict)
    )

    parts = [f"- {name}"]
    if off:
        parts.append("[SPENTA]")
    elif status:
        parts.append(f"[{status}]")
    if health:
        parts.append(f"| health: {health}")
    if env:
        parts.append(f"| {env}")
    if cliente:
        parts.append(f"| cliente: {cliente}")
    if domain:
        parts.append(f"| {domain}")
    if maint_names:
        parts.append(f"| maintainer: {maint_names}")
    if summary:
        parts.append(f"| {summary[:80]}")
    return " ".join(parts)


def _format_error(e: dict, kind: str = "BE") -> str:
    path = e.get("cod_path", "")
    error = e.get("cod_error", "")
    occurrences = e.get("val_occurrences", 0)
    last = e.get("dat_last_occurrence", "")
    status = e.get("des_status", "")
    assigned = e.get("des_assigned_dev_email", "")
    component = e.get("cod_component", "")
    browser = e.get("des_browser", "")

    parts = [f"- [{kind}]"]
    if status:
        parts.append(f"[{status}]")
    if path:
        parts.append(path)
    if error:
        parts.append(f"| {error[:60]}")
    parts.append(f"| {occurrences}x")
    if last:
        parts.append(f"| ultimo: {last[:10]}")
    if assigned:
        parts.append(f"| dev: {assigned}")
    if component:
        parts.append(f"| comp: {component}")
    if browser:
        parts.append(f"| browser: {browser}")
    return " ".join(parts)


async def handle_get_applicazioni(args: dict) -> list[TextContent]:
    nome = args.get("nome")
    project_status = args.get("project_status")
    env = args.get("env")

    async def _run():
        search = build_search(
            ("app_name", "like", nome),
            ("project_status", "eq", project_status),
            ("env", "eq", env),
        )
        items, total = await paginated_search("/applications/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuna applicazione trovata{' per ' + repr(nome) if nome else ''}.")]

        active = [a for a in items if not a.get("flg_turn_off")]
        off = [a for a in items if a.get("flg_turn_off")]

        lines = [f"Applicazioni ({total} totali, {len(active)} attive, {len(off)} spente):\n"]
        lines.extend(_format_app(a) for a in items)
        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_errori_app(args: dict) -> list[TextContent]:
    app_name = args.get("app_name")
    status = args.get("status")

    async def _run():
        be_search = build_search(
            ("application.app_name", "like", app_name),
            ("des_status", "eq", status),
        )
        fe_search = build_search(
            ("application.app_name", "like", app_name),
            ("des_status", "eq", status),
        )

        be_items, be_total = await paginated_search(
            "/application/errors/backend/search", be_search,
            sort_by="dat_last_occurrence", sort_order="desc",
        )
        fe_items, fe_total = await paginated_search(
            "/application/errors/frontend/search", fe_search,
            sort_by="dat_last_occurrence", sort_order="desc",
        )

        total = len(be_items) + len(fe_items)
        if total == 0:
            return [TextContent(type="text", text="Nessun errore trovato con i filtri specificati.")]

        lines = [f"Errori applicazioni ({be_total + fe_total} totali: {be_total} backend, {fe_total} frontend):\n"]

        if be_items:
            lines.append("Backend:")
            lines.extend(_format_error(e, "BE") for e in be_items)
            be_warn = truncation_warning(len(be_items), be_total)
            if be_warn:
                lines.append(be_warn)
            lines.append("")

        if fe_items:
            lines.append("Frontend:")
            lines.extend(_format_error(e, "FE") for e in fe_items)
            fe_warn = truncation_warning(len(fe_items), fe_total)
            if fe_warn:
                lines.append(fe_warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_applicazioni": {
        "definition": Tool(
            name="get_applicazioni",
            description="Lista applicazioni LAIF con stato, health, cliente e maintainer. Filtrabile per nome app, status progetto (development, maintenance, retired) e ambiente (dev, prod).",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome dell'applicazione (ricerca parziale). Opzionale."},
                    "project_status": {"type": "string", "description": "Status del progetto: development, maintenance, retired. Opzionale.", "enum": ["development", "maintenance", "retired"]},
                    "env": {"type": "string", "description": "Ambiente: dev, prod. Opzionale.", "enum": ["dev", "prod"]},
                },
                "required": [],
            },
        ),
        "handler": handle_get_applicazioni,
    },
    "get_errori_app": {
        "definition": Tool(
            name="get_errori_app",
            description="Errori backend e frontend delle applicazioni. Filtrabile per nome app e status errore (unassigned, assigned, in_progress, fixed, to_ignore). Ordinati per data ultima occorrenza (decrescente).",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Nome dell'applicazione (ricerca parziale). Opzionale."},
                    "status": {"type": "string", "description": "Status dell'errore: unassigned, assigned, in_progress, fixed, to_ignore. Opzionale.", "enum": ["unassigned", "assigned", "in_progress", "fixed", "to_ignore"]},
                },
                "required": [],
            },
        ),
        "handler": handle_get_errori_app,
    },
}
