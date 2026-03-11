"""Tool staffing settimanale."""

from datetime import date

from mcp.types import TextContent, Tool, ToolAnnotations

from helpers import (
    build_search,
    paginated_search,
    truncation_warning,
    safe_call,
    week_bounds,
    filter_by_employee_name,
    group_by_employee,
    employee_name,
)


def _format_staffing_entry(entry: dict) -> str:
    category = entry.get("category") or {}
    cat_name = category.get("des_category", "") if isinstance(category, dict) else ""
    sub_category = entry.get("sub_category") or {}
    sub_name = sub_category.get("des_sub_category", "") if isinstance(sub_category, dict) else ""
    sale = entry.get("sale") or {}
    lead = sale.get("lead") or {} if isinstance(sale, dict) else {}
    sale_name = lead.get("name", "") if isinstance(lead, dict) else ""
    if not sale_name and isinstance(lead, dict):
        sale_name = str(lead.get("cod_project", ""))

    hours = entry.get("num_hours", 0)
    parts = []
    if sale_name:
        parts.append(sale_name)
    if sub_name:
        parts.append(f"({sub_name})")
    elif cat_name:
        parts.append(f"({cat_name})")
    label = " ".join(parts) or "N/D"
    return f"  - {label}: {hours}h"


async def handle_get_staffing_persona(args: dict) -> list[TextContent]:
    query = args["nome"]
    data_str = args.get("data") or str(date.today())
    monday, _ = week_bounds(data_str)

    async def _run():
        search = build_search(
            ("dat_week", "eq", monday),
        )
        items, total = await paginated_search("/staffing/search", search)

        matching = filter_by_employee_name(items, query)
        if not matching:
            return [TextContent(type="text", text=f"Nessuno staffing trovato per '{query}' nella settimana del {monday}.")]

        groups = group_by_employee(matching)
        lines = []
        for name, entries in groups.items():
            total_hrs = sum(e.get("num_hours", 0) for e in entries)
            lines.append(f"{name} — settimana del {monday} ({total_hrs}h):")
            lines.extend(_format_staffing_entry(e) for e in entries)
            lines.append("")

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_staffing_team(args: dict) -> list[TextContent]:
    data_str = args.get("data") or str(date.today())
    monday, _ = week_bounds(data_str)

    async def _run():
        search = build_search(
            ("dat_week", "eq", monday),
        )
        items, total = await paginated_search("/staffing/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuno staffing trovato per la settimana del {monday}.")]

        groups = group_by_employee(items)
        lines = [f"Staffing team — settimana del {monday}:\n"]
        for name, entries in groups.items():
            total_hrs = sum(e.get("num_hours", 0) for e in entries)
            lines.append(f"{name} ({total_hrs}h):")
            lines.extend(_format_staffing_entry(e) for e in entries)
            lines.append("")

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_staffing_persona": {
        "definition": Tool(
            name="get_staffing_persona",
            description="Mostra lo staffing settimanale di un dipendente: su quali progetti è allocato e per quante ore.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome o cognome del dipendente (ricerca parziale)"},
                    "data": {"type": "string", "description": "Qualsiasi giorno nella settimana di interesse (YYYY-MM-DD). Default: settimana corrente."},
                },
                "required": ["nome"],
            },
        ),
        "handler": handle_get_staffing_persona,
    },
    "get_staffing_team": {
        "definition": Tool(
            name="get_staffing_team",
            description="Vista staffing settimanale di tutto il team: chi lavora su cosa e per quante ore.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Qualsiasi giorno nella settimana di interesse (YYYY-MM-DD). Default: settimana corrente."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_staffing_team,
    },
}
