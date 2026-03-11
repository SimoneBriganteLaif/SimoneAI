"""Tool ferie e assenze."""

from datetime import date

from mcp.types import TextContent, Tool, ToolAnnotations

from helpers import build_search, paginated_search, truncation_warning, safe_call, week_bounds, filter_by_employee_name, employee_name, format_date


def _format_outage(o: dict) -> str:
    employee = o.get("employee", {})
    nome = f"{employee.get('des_name', '')} {employee.get('des_surname', '')}".strip() or "N/D"
    dat_from = o.get("dat_from", "?")
    dat_to = o.get("dat_to") or "—"
    am_pm = o.get("am_pm")
    note = o.get("des_note", "")
    approvato = "approvata" if o.get("tms_approval") else ("rifiutata" if o.get("flg_declined") else "in attesa")

    parts = [f"- {nome}: {dat_from} → {dat_to}"]
    if am_pm:
        parts.append(f"({am_pm})")
    parts.append(f"| {approvato}")
    if note:
        parts.append(f"| nota: {note}")
    return " ".join(parts)


async def handle_get_ferie_team(args: dict) -> list[TextContent]:
    dat_from = args["dat_from"]
    dat_to = args.get("dat_to", dat_from)

    async def _run():
        search = build_search(
            ("dat_from", "date_after", dat_from),
            ("dat_to", "date_before", dat_to),
        )
        items, total = await paginated_search("/outages/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuna assenza trovata dal {dat_from} al {dat_to}.")]
        lines = [f"Assenze dal {dat_from} al {dat_to} ({len(items)} record):\n"]
        lines.extend(_format_outage(o) for o in items)

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_ferie_persona(args: dict) -> list[TextContent]:
    query = args["nome"]
    dat_from = args.get("dat_from")
    dat_to = args.get("dat_to")

    async def _run():
        search = build_search(
            ("dat_from", "date_after", dat_from),
            ("dat_to", "date_before", dat_to),
        )
        items, total = await paginated_search("/outages/search", search)

        matching = filter_by_employee_name(items, query)
        if not matching:
            periodo = f" dal {dat_from} al {dat_to}" if dat_from else ""
            return [TextContent(type="text", text=f"Nessuna assenza trovata per '{query}'{periodo}.")]
        lines = [f"Assenze di '{query}' ({len(matching)} record):\n"]
        lines.extend(_format_outage(o) for o in matching)

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_calendario_settimana(args: dict) -> list[TextContent]:
    data_str = args.get("data") or str(date.today())
    dat_from, dat_to = week_bounds(data_str)

    async def _run():
        search = build_search(
            ("dat_from", "date_after", dat_from),
            ("dat_to", "date_before", dat_to),
        )
        items, total = await paginated_search("/outages/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessuno è assente nella settimana {dat_from} — {dat_to}.")]
        lines = [f"Calendario assenze settimana {dat_from} — {dat_to} ({len(items)} record):\n"]
        lines.extend(_format_outage(o) for o in items)

        warn = truncation_warning(len(items), total)
        if warn:
            lines.append(warn)

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_ferie_team": {
        "definition": Tool(
            name="get_ferie_team",
            description="Recupera tutte le assenze/ferie del team in un intervallo di date. Utile per sapere chi è assente in un periodo.",
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
        "handler": handle_get_ferie_team,
    },
    "get_ferie_persona": {
        "definition": Tool(
            name="get_ferie_persona",
            description="Recupera le assenze/ferie di un dipendente specifico, cercato per nome o cognome.",
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
        "handler": handle_get_ferie_persona,
    },
    "get_calendario_settimana": {
        "definition": Tool(
            name="get_calendario_settimana",
            description="Vista rapida: mostra chi è assente in una settimana specifica. Default: settimana corrente.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Qualsiasi giorno nella settimana di interesse (YYYY-MM-DD). Default: oggi."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_calendario_settimana,
    },
}
