"""Tool rendicontazione ore."""

from datetime import date

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_get
from helpers import build_search, paginated_search, truncation_warning, safe_call, filter_by_employee_name, group_by_employee, employee_name


def _format_reporting_entry(r: dict) -> str:
    cat = r.get("category") or {}
    cat_name = cat.get("des_category", "") if isinstance(cat, dict) else ""
    sub = r.get("sub_category") or {}
    sub_name = sub.get("des_sub_category", "") if isinstance(sub, dict) else ""
    sale = r.get("sale") or {}
    lead = sale.get("lead") or {} if isinstance(sale, dict) else {}
    project = lead.get("name", "") if isinstance(lead, dict) else ""

    hours = r.get("num_hours", 0)
    day = r.get("dat_day", "")

    parts = []
    if project:
        parts.append(project)
    if sub_name:
        parts.append(f"({sub_name})")
    elif cat_name:
        parts.append(f"({cat_name})")
    label = " ".join(parts) or "N/D"
    day_str = f" [{day}]" if day else ""
    return f"  - {label}: {hours}h{day_str}"


async def handle_get_rendicontazione_persona(args: dict) -> list[TextContent]:
    query = args["nome"]
    dat_from = args.get("dat_from")
    dat_to = args.get("dat_to")

    async def _run():
        search = build_search(
            ("dat_month", "date_after", dat_from),
            ("dat_month", "date_before", dat_to),
        )

        items, total = await paginated_search("/reporting/search", search)

        matching = filter_by_employee_name(items, query)
        if not matching:
            periodo = ""
            if dat_from:
                periodo += f" dal {dat_from}"
            if dat_to:
                periodo += f" al {dat_to}"
            return [TextContent(type="text", text=f"Nessuna rendicontazione trovata per '{query}'{periodo}.")]

        # Raggruppa per progetto/categoria e somma ore
        totale = sum(e.get("num_hours", 0) for e in matching)
        per_progetto: dict[str, float] = {}
        for e in matching:
            cat = e.get("category") or {}
            sub = e.get("sub_category") or {}
            sale = e.get("sale") or {}
            lead = sale.get("lead") or {} if isinstance(sale, dict) else {}
            project = lead.get("name", "") if isinstance(lead, dict) else ""
            sub_name = sub.get("des_sub_category", "") if isinstance(sub, dict) else ""
            cat_name = cat.get("des_category", "") if isinstance(cat, dict) else ""
            key = project or sub_name or cat_name or "Altro"
            per_progetto[key] = per_progetto.get(key, 0) + (e.get("num_hours", 0) or 0)

        emp = matching[0].get("employee") or {}
        nome = employee_name(emp)
        lines = [f"Rendicontazione {nome} — {totale}h totali:\n"]
        for proj, hrs in sorted(per_progetto.items(), key=lambda x: -x[1]):
            lines.append(f"  - {proj}: {hrs}h")

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_rendicontazione_team(args: dict) -> list[TextContent]:
    dat_from = args["dat_from"]
    dat_to = args.get("dat_to", dat_from)

    async def _run():
        search = build_search(
            ("dat_month", "date_after", dat_from),
            ("dat_month", "date_before", dat_to),
        )

        items, total = await paginated_search("/reporting/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuna rendicontazione trovata dal {dat_from} al {dat_to}.")]

        groups = group_by_employee(items)
        lines = [f"Rendicontazione team — {dat_from} → {dat_to}:\n"]
        for name, entries in groups.items():
            total_hrs = sum(e.get("num_hours", 0) for e in entries)
            lines.append(f"{name} ({total_hrs}h):")
            # Raggruppa per progetto
            per_proj: dict[str, float] = {}
            for e in entries:
                sale = e.get("sale") or {}
                lead = sale.get("lead") or {} if isinstance(sale, dict) else {}
                project = lead.get("name", "") if isinstance(lead, dict) else ""
                cat = e.get("category") or {}
                cat_name = cat.get("des_category", "") if isinstance(cat, dict) else ""
                key = project or cat_name or "Altro"
                per_proj[key] = per_proj.get(key, 0) + (e.get("num_hours", 0) or 0)
            for proj, hrs in sorted(per_proj.items(), key=lambda x: -x[1]):
                lines.append(f"  - {proj}: {hrs}h")
            lines.append("")

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_ore_lavorate(args: dict) -> list[TextContent]:
    anno = args.get("anno", 2026)
    company = args.get("company", "laif")

    async def _run():
        data = await api_get(f"/reporting/employee-working-hours/{anno}/{company}")
        items = data if isinstance(data, list) else data.get("items", data.get("data", []))

        if not items:
            return [TextContent(type="text", text=f"Nessun dato ore lavorate trovato (anno: {anno}, company: {company}).")]

        months_names = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                        "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

        # API: lista piatta [{id_employee, des_name, des_surname, dat_month, total_work_hours, ...}]
        # Raggruppa per dipendente
        by_employee: dict[str, dict[int, float]] = {}
        for item in items:
            name = f"{item.get('des_name', '')} {item.get('des_surname', '')}".strip() or "N/D"
            month_str = item.get("dat_month", "")
            hours = item.get("total_work_hours") or 0
            if month_str:
                try:
                    month_num = int(month_str[5:7])
                except (ValueError, IndexError):
                    month_num = 0
                by_employee.setdefault(name, {})[month_num] = hours

        lines = [f"Ore lavorate per dipendente — {anno} ({company}):\n"]
        for name in sorted(by_employee.keys()):
            months = by_employee[name]
            total = sum(months.values())
            month_parts = [f"{months_names[m - 1]}:{int(h)}h" for m, h in sorted(months.items()) if h and 1 <= m <= 12]
            lines.append(f"- {name}: {int(total)}h totali | {', '.join(month_parts)}")

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_rendicontazione_persona": {
        "definition": Tool(
            name="get_rendicontazione_persona",
            description="Ore rendicontate da un dipendente, raggruppate per progetto. Cercato per nome o cognome.",
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
                    "dat_from": {"type": "string", "description": "Data inizio (YYYY-MM-DD, opzionale)"},
                    "dat_to": {"type": "string", "description": "Data fine (YYYY-MM-DD, opzionale)"},
                },
                "required": ["nome"],
            },
        ),
        "handler": handle_get_rendicontazione_persona,
    },
    "get_rendicontazione_team": {
        "definition": Tool(
            name="get_rendicontazione_team",
            description="Ore rendicontate da tutto il team in un periodo, raggruppate per persona e progetto.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "dat_from": {"type": "string", "description": "Data inizio (YYYY-MM-DD)"},
                    "dat_to": {"type": "string", "description": "Data fine (YYYY-MM-DD, opzionale — default: dat_from)"},
                },
                "required": ["dat_from"],
            },
        ),
        "handler": handle_get_rendicontazione_team,
    },
    "get_ore_lavorate": {
        "definition": Tool(
            name="get_ore_lavorate",
            description="Ore lavorate per dipendente, mese per mese, in un anno. Utile per confronti e analisi carichi.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "anno": {"type": "integer", "description": "Anno di riferimento (default: 2026)."},
                    "company": {"type": "string", "description": "Nome o ID della company (default: laif). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_ore_lavorate,
    },
}
