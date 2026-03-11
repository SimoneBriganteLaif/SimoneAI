"""Tool presenze in ufficio."""

from datetime import date

from mcp.types import TextContent, Tool, ToolAnnotations

from helpers import build_search, paginated_search, truncation_warning, safe_call, filter_by_employee_name, employee_name


def _format_presence(p: dict) -> str:
    emp = p.get("employee") or {}
    nome = employee_name(emp)
    cal = p.get("calendar") or {}
    giorno = cal.get("dat_calendar", "?")
    maybe = " (forse)" if p.get("flg_maybe") else ""
    return f"- {nome}: {giorno}{maybe}"


async def handle_get_presenze_giorno(args: dict) -> list[TextContent]:
    data_str = args.get("data") or str(date.today())

    async def _run():
        search = build_search(
            ("calendar.dat_calendar", "eq", data_str),
        )
        items, total = await paginated_search("/office-presence/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuna presenza registrata per il {data_str}.")]

        lines = [f"Presenze in ufficio — {data_str} ({len(items)} persone):\n"]
        lines.extend(_format_presence(p) for p in items)
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_presenze_persona(args: dict) -> list[TextContent]:
    query = args["nome"]
    dat_from = args.get("dat_from")
    dat_to = args.get("dat_to")

    async def _run():
        search = build_search(
            ("calendar.dat_calendar", "date_after", dat_from),
            ("calendar.dat_calendar", "date_before", dat_to),
        )

        items, total = await paginated_search("/office-presence/search", search)

        matching = filter_by_employee_name(items, query)
        if not matching:
            periodo = ""
            if dat_from:
                periodo += f" dal {dat_from}"
            if dat_to:
                periodo += f" al {dat_to}"
            return [TextContent(type="text", text=f"Nessuna presenza trovata per '{query}'{periodo}.")]

        lines = [f"Presenze di '{query}' ({len(matching)} record):\n"]
        lines.extend(_format_presence(p) for p in matching)

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_presenze_giorno": {
        "definition": Tool(
            name="get_presenze_giorno",
            description="Chi è in ufficio in un giorno specifico. Default: oggi.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Giorno di riferimento (YYYY-MM-DD). Default: oggi."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_presenze_giorno,
    },
    "get_presenze_persona": {
        "definition": Tool(
            name="get_presenze_persona",
            description="Storico presenze in ufficio di un dipendente, cercato per nome o cognome.",
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
        "handler": handle_get_presenze_persona,
    },
}
