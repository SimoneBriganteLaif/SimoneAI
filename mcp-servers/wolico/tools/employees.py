"""Tool dipendente: dati contrattuali, stipendio, lista dipendenti."""

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_get
from helpers import build_search, paginated_search, truncation_warning, safe_call


async def handle_get_mio_stipendio(args: dict) -> list[TextContent]:
    async def _run():
        me = await api_get("/employees/myself")
        if not me:
            return [TextContent(type="text", text="Nessun dato dipendente trovato per l'utente corrente.")]

        nome = f"{me.get('des_name', '')} {me.get('des_surname', '')}".strip()
        lines = [f"Dati dipendente: {nome}\n"]
        lines.append(f"  Ruolo: {me.get('des_role', 'N/D')}")
        lines.append(f"  Company: {me.get('company', 'N/D')}")

        current = me.get("current_contract") or {}
        if current:
            lines.append(f"\nContratto attuale:")
            lines.append(f"  Tipo: {current.get('contract_type', 'N/D')}")
            lines.append(f"  Inizio: {current.get('dat_start', 'N/D')}")
            end = current.get("dat_end") or "indeterminato"
            lines.append(f"  Fine: {end}")
            lines.append(f"  Ore giornaliere minime: {current.get('min_daily_hour', 'N/D')}")

        salary_fields = ["amt_ral", "amt_monthly_ral", "amt_total_compensation", "amt_hourly_compensation"]
        salary_found = False
        for field in salary_fields:
            if me.get(field) is not None or (current and current.get(field) is not None):
                salary_found = True
                break

        if salary_found:
            lines.append(f"\nDati retributivi:")
            for source in [me, current]:
                if source.get("amt_ral"):
                    lines.append(f"  RAL: €{source['amt_ral']:,.0f}")
                if source.get("amt_monthly_ral"):
                    lines.append(f"  Mensile lordo: €{source['amt_monthly_ral']:,.0f}")
                if source.get("amt_total_compensation"):
                    lines.append(f"  Compenso totale: €{source['amt_total_compensation']:,.0f}")
                if source.get("amt_hourly_compensation"):
                    lines.append(f"  Tariffa oraria: €{source['amt_hourly_compensation']:,.2f}")
        else:
            lines.append(f"\nDati retributivi: non disponibili.")
            lines.append("I campi stipendio (RAL, compenso mensile, ecc.) non sono presenti nella risposta API.")
            lines.append("Probabilmente non hai i permessi per visualizzare queste informazioni.")

        contracts = me.get("contracts") or []
        if len(contracts) > 1:
            lines.append(f"\nStorico contratti ({len(contracts)}):")
            for c in contracts:
                end = c.get("dat_end") or "in corso"
                lines.append(f"  - {c.get('dat_start', '?')} → {end} ({c.get('contract_type', '?')})")

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_dipendenti(args: dict) -> list[TextContent]:
    nome = args.get("nome")
    ruolo = args.get("ruolo")
    company = args.get("company")
    solo_attivi = args.get("solo_attivi", True)

    async def _run():
        # Build search conditions
        conditions: list[dict] = []

        if nome:
            conditions.append({
                "_or": [
                    {"des_name": {"operator": "like", "value": nome}},
                    {"des_surname": {"operator": "like", "value": nome}},
                ]
            })

        if ruolo:
            conditions.append({"des_role": {"operator": "like", "value": ruolo}})

        if company:
            conditions.append({"company": {"operator": "eq", "value": company}})

        if solo_attivi:
            conditions.append({"user.flg_valid": {"operator": "checked", "value": True}})

        if not conditions:
            search = None
        elif len(conditions) == 1:
            search = conditions[0]
        else:
            search = {"_and": conditions}

        items, total = await paginated_search(
            "/employees/search",
            search,
            sort_by="des_surname",
            sort_order="asc",
        )

        if not items:
            return [TextContent(type="text", text="Nessun dipendente trovato con i filtri specificati.")]

        lines = [f"Dipendenti trovati: {total}\n"]
        for emp in items:
            name = f"{emp.get('des_name', '')} {emp.get('des_surname', '')}".strip()
            role = emp.get("des_role", "N/D")
            comp = emp.get("company", "N/D")
            lines.append(f"- {name} | {role} | {comp}")

        lines.append(truncation_warning(len(items), total))

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_mio_stipendio": {
        "definition": Tool(
            name="get_mio_stipendio",
            description="Recupera i dati contrattuali e di compenso del dipendente corrente. Potrebbe fallire se l'utente non ha i permessi necessari.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        "handler": handle_get_mio_stipendio,
    },
    "get_dipendenti": {
        "definition": Tool(
            name="get_dipendenti",
            description="Cerca dipendenti per nome, ruolo o company (laif, helia). Di default mostra solo i dipendenti attivi.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome o cognome del dipendente (ricerca parziale). Opzionale.",
                    },
                    "ruolo": {
                        "type": "string",
                        "description": "Ruolo del dipendente (ricerca parziale). Opzionale.",
                    },
                    "company": {
                        "type": "string",
                        "enum": ["laif", "helia"],
                        "description": "Company di appartenenza: laif o helia. Opzionale.",
                    },
                    "solo_attivi": {
                        "type": "boolean",
                        "description": "Se true (default), mostra solo dipendenti attivi. Opzionale.",
                        "default": True,
                    },
                },
                "required": [],
            },
        ),
        "handler": handle_get_dipendenti,
    },
}
