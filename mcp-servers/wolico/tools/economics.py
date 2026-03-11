"""Tool economics: tranche fatturazione, revenue overview, marginalità, bilancio, costi cloud, ricavi ricorrenti."""

from datetime import date

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_get
from helpers import safe_call


async def handle_get_tranche_fatturazione(args: dict) -> list[TextContent]:
    company = args.get("company", "laif")

    async def _run():
        data = await api_get(f"/economics/revenues/to-issue/{company}")
        items = data if isinstance(data, list) else data.get("items", data.get("data", []))
        if not items:
            return [TextContent(type="text", text=f"Nessuna tranche da emettere trovata (company: {company}).")]

        lines = [f"Tranche di fatturazione da emettere — {company} ({len(items)} tranche):\n"]
        for item in items:
            sale = item.get("sale") or {}
            lead = sale.get("lead") or {} if isinstance(sale, dict) else {}
            project_name = lead.get("name", "") if isinstance(lead, dict) else ""
            cod_project = lead.get("cod_project", "") if isinstance(lead, dict) else ""
            partner = lead.get("partner", {}) if isinstance(lead, dict) else {}
            partner_name = partner.get("alias") or partner.get("name", "") if isinstance(partner, dict) else ""

            month = item.get("dat_month", "?")
            amount = item.get("amt_untaxed", 0)
            tax = item.get("amt_tax", 0)
            tranche_order = item.get("tranche_order", "")
            issued = "emessa" if item.get("flg_issued") else "da emettere"
            team_leader = sale.get("team_leader", {}) if isinstance(sale, dict) else {}
            tl_name = f"{team_leader.get('des_name', '')} {team_leader.get('des_surname', '')}".strip() if isinstance(team_leader, dict) else ""

            label = project_name or f"Progetto {cod_project}" or "N/D"
            if partner_name:
                label = f"{partner_name} — {label}"

            parts = [f"- {label}: €{amount:,.0f} (+IVA €{tax:,.0f}) — {month[:7]}"]
            if tranche_order:
                parts.append(f"[{tranche_order}]")
            parts.append(f"— {issued}")
            if tl_name:
                parts.append(f"(TL: {tl_name})")

            lines.append(" ".join(parts))

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_revenues_overview(args: dict) -> list[TextContent]:
    company = args.get("company", "laif")
    year = args.get("year", date.today().year)

    async def _run():
        data = await api_get(f"/economics/revenues/chart-data/{company}/{year}")
        if not data:
            return [TextContent(type="text", text=f"Nessun dato revenue trovato (company: {company}, anno: {year}).")]

        months_names = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                        "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]

        if isinstance(data, list):
            lines = [f"Revenue overview {year} — {company}:\n"]
            lines.append(f"{'Mese':<6} {'Fatturato':>12} {'Forecast':>12} {'Starting':>12} {'Probabile':>12} {'Totale':>12}")
            lines.append("-" * 72)

            total_year = 0
            for item in data:
                m_num = item.get("month_num", 0)
                m_name = months_names[m_num - 1] if 1 <= m_num <= 12 else f"M{m_num}"

                issued = item.get("project_issued", 0) + item.get("recurrent_issued", 0)
                forecast = item.get("project_forecast", 0) + item.get("recurrent_forecast", 0)
                starting = item.get("project_starting", 0) + item.get("recurrent_starting", 0)
                probable = item.get("project_probable", 0) + item.get("recurrent_probable", 0)
                total = issued + forecast + starting + probable
                total_year += total

                lines.append(
                    f"{m_name:<6} {issued:>12,.0f} {forecast:>12,.0f} {starting:>12,.0f} {probable:>12,.0f} {total:>12,.0f}"
                )

            lines.append("-" * 72)
            lines.append(f"{'TOT':<6} {'':>12} {'':>12} {'':>12} {'':>12} {total_year:>12,.0f}")
        else:
            lines = [f"Revenue overview {year}: {data}"]

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_ricavi_ricorrenti_in_scadenza(args: dict) -> list[TextContent]:
    company = args.get("company", "laif")

    async def _run():
        data = await api_get(f"/economics/revenues/expiring-recurring/{company}")
        items = data if isinstance(data, list) else data.get("items", data.get("data", []))

        if not items:
            return [TextContent(type="text", text=f"Nessun ricavo ricorrente in scadenza trovato (company: {company}).")]

        lines = [f"Ricavi ricorrenti in scadenza — {company} ({len(items)} record):\n"]
        for item in items:
            partner = item.get("partner_name", "N/D")
            lead = item.get("lead_name", "")
            amount = item.get("amt_lead") or 0
            expiry = item.get("dat_expiration") or "—"
            renew = item.get("flg_renew")
            tl = f"{item.get('tl_name') or ''} {item.get('tl_surname') or ''}".strip()

            label = f"{partner} — {lead}" if lead else partner
            parts = [f"- {label}: €{amount:,.0f}"]
            if expiry != "—":
                parts.append(f"| scadenza {expiry[:10]}")
            if renew is not None:
                parts.append(f"| {'rinnovo' if renew else 'non rinnova'}")
            if tl:
                parts.append(f"| TL: {tl}")
            lines.append(" ".join(parts))

        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


TOOLS = {
    "get_tranche_fatturazione": {
        "definition": Tool(
            name="get_tranche_fatturazione",
            description="Mostra le tranche di fatturazione da emettere questo mese per una company specifica.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Nome o ID della company (opzionale). Se omesso, viene usata la prima company disponibile."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_tranche_fatturazione,
    },
    "get_revenues_overview": {
        "definition": Tool(
            name="get_revenues_overview",
            description="Panoramica revenue annuale per mese: fatturato, forecast, progetti in partenza e probabili.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Nome o ID della company (opzionale)."},
                    "year": {"type": "integer", "description": "Anno di riferimento (default: anno corrente)."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_revenues_overview,
    },
    "get_ricavi_ricorrenti_in_scadenza": {
        "definition": Tool(
            name="get_ricavi_ricorrenti_in_scadenza",
            description="Ricavi ricorrenti in scadenza: deal, cliente, data scadenza e importo.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "Nome o ID della company (default: laif). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_ricavi_ricorrenti_in_scadenza,
    },
}
