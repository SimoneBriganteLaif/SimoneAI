"""Tool CRM: opportunità, ordini, clienti, contatti."""

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_post
from helpers import build_search, paginated_search, truncation_warning, safe_call


# ---------------------------------------------------------------------------
# Formattatori
# ---------------------------------------------------------------------------

def _format_lead(lead: dict) -> str:
    name = lead.get("name", "N/D")
    status = lead.get("status", "?")
    revenue = lead.get("amt_expected_revenue")
    partner = lead.get("partner") or {}
    cliente = partner.get("alias") or partner.get("name", "")
    user = lead.get("user") or {}
    owner = f"{user.get('des_name', '')} {user.get('des_surname', '')}".strip() if isinstance(user, dict) else ""
    tags = ", ".join(t.get("des_tag", "") for t in (lead.get("lead_tags") or []) if t.get("des_tag"))
    dat = lead.get("dat_creation", "")

    parts = [f"- {name}"]
    if cliente:
        parts.append(f"({cliente})")
    parts.append(f"| {status}")
    if revenue:
        parts.append(f"| €{revenue:,.0f}")
    if owner:
        parts.append(f"| ref: {owner}")
    if tags:
        parts.append(f"| tag: {tags}")
    if dat:
        parts.append(f"| {dat[:10]}")
    return " ".join(parts)


def _format_sale(sale: dict) -> str:
    lead = sale.get("lead") or {}
    name = lead.get("name", "N/D") if isinstance(lead, dict) else "N/D"
    partner = lead.get("partner") or {} if isinstance(lead, dict) else {}
    cliente = partner.get("alias") or partner.get("name", "") if isinstance(partner, dict) else ""
    untaxed = sale.get("amt_untaxed")
    tax = sale.get("amt_tax")
    status = sale.get("status", "?")
    year = sale.get("year", "")
    tl = sale.get("team_leader") or {}
    leader = f"{tl.get('des_name', '')} {tl.get('des_surname', '')}".strip() if isinstance(tl, dict) else ""

    parts = [f"- {name}"]
    if cliente:
        parts.append(f"({cliente})")
    parts.append(f"| {status}")
    if untaxed:
        total = untaxed + (tax or 0)
        parts.append(f"| €{untaxed:,.0f} (+IVA €{total:,.0f})")
    if leader:
        parts.append(f"| TL: {leader}")
    if year:
        parts.append(f"| {year}")
    return " ".join(parts)


def _format_partner(p: dict) -> str:
    name = p.get("name") or p.get("alias") or "N/D"
    alias = p.get("alias", "")
    sector = p.get("sector", "")
    city = p.get("city", "")
    email = p.get("email", "")
    leads = p.get("num_leads", 0)
    sales = p.get("num_sales", 0)

    parts = [f"- {name}"]
    if alias and alias != name:
        parts.append(f"({alias})")
    if sector:
        parts.append(f"| {sector}")
    if city:
        parts.append(f"| {city}")
    if email:
        parts.append(f"| {email}")
    if leads or sales:
        parts.append(f"| {leads} lead, {sales} ordini")
    return " ".join(parts)


def _format_contact(c: dict) -> str:
    nome = f"{c.get('des_name', '')} {c.get('des_surname', '')}".strip() or "N/D"
    role = c.get("des_role", "")
    email = c.get("des_email", "")
    phone = c.get("des_phone", "")
    partner = c.get("partner") or {}
    azienda = partner.get("name") or partner.get("alias", "") if isinstance(partner, dict) else ""

    parts = [f"- {nome}"]
    if role:
        parts.append(f"({role})")
    if azienda:
        parts.append(f"| {azienda}")
    if email:
        parts.append(f"| {email}")
    if phone:
        parts.append(f"| {phone}")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Handler
# ---------------------------------------------------------------------------

async def handle_get_opportunita(args: dict) -> list[TextContent]:
    status = args.get("status")
    nome_cliente = args.get("nome_cliente")

    async def _run():
        search = build_search(
            ("status", "eq", status),
            ("partner.name", "like", nome_cliente),
        )
        items, total = await paginated_search(
            "/leads/search", search,
            sort_by="dat_creation", sort_order="desc",
        )

        if not items:
            return [TextContent(type="text", text="Nessuna opportunità trovata con i filtri specificati.")]

        lines = [f"Opportunità ({len(items)} risultati):\n"]
        lines.extend(_format_lead(i) for i in items)
        lines.append(truncation_warning(len(items), total))
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_ordini(args: dict) -> list[TextContent]:
    nome_cliente = args.get("nome_cliente")
    anno = args.get("anno")
    status = args.get("status")

    async def _run():
        search = build_search(
            ("year", "eq", anno),
            ("status", "eq", status),
            ("search_concat", "like", nome_cliente),
        )
        items, total = await paginated_search("/sales/basic-search", search)

        if not items:
            return [TextContent(type="text", text="Nessun ordine trovato con i filtri specificati.")]

        totale = sum((s.get("amt_untaxed") or 0) for s in items)
        lines = [f"Ordini ({len(items)} risultati, totale €{totale:,.0f}):\n"]
        lines.extend(_format_sale(i) for i in items)
        lines.append(truncation_warning(len(items), total))
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_clienti(args: dict) -> list[TextContent]:
    nome = args.get("nome")
    sector = args.get("sector")

    async def _run():
        search = build_search(
            ("name", "like", nome),
            ("sector", "eq", sector),
        )
        items, total = await paginated_search("/partners/search", search)

        if not items:
            return [TextContent(type="text", text=f"Nessun cliente trovato{' per ' + repr(nome) if nome else ''}.")]

        lines = [f"Clienti/Partner ({len(items)} risultati):\n"]
        lines.extend(_format_partner(i) for i in items)
        lines.append(truncation_warning(len(items), total))
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_contatti(args: dict) -> list[TextContent]:
    nome = args.get("nome")
    azienda = args.get("azienda")

    async def _run():
        # Build search with _or for nome across des_name and des_surname
        conditions = []
        if nome:
            conditions.append({
                "_or": [
                    {"des_name": {"operator": "like", "value": nome}},
                    {"des_surname": {"operator": "like", "value": nome}},
                ]
            })
        if azienda:
            conditions.append({"partner.name": {"operator": "like", "value": azienda}})

        if not conditions:
            search = None
        elif len(conditions) == 1:
            search = conditions[0]
        else:
            search = {"_and": conditions}

        items, total = await paginated_search("/contacts/search", search)

        if not items:
            filtro = ""
            if nome:
                filtro += f" nome='{nome}'"
            if azienda:
                filtro += f" azienda='{azienda}'"
            return [TextContent(type="text", text=f"Nessun contatto trovato{filtro}.")]

        lines = [f"Contatti ({len(items)} risultati):\n"]
        lines.extend(_format_contact(i) for i in items)
        lines.append(truncation_warning(len(items), total))
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = {
    "get_opportunita": {
        "definition": Tool(
            name="get_opportunita",
            description="Mostra lead/opportunità commerciali. Filtrabile per status e nome cliente.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Stato della lead (es. new, qualified, proposition, won, freezed, lost). Opzionale."},
                    "nome_cliente": {"type": "string", "description": "Nome del cliente/partner da cercare (ricerca parziale). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_opportunita,
    },
    "get_ordini": {
        "definition": Tool(
            name="get_ordini",
            description="Mostra gli ordini/vendite. Filtrabile per cliente, anno e status.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome_cliente": {"type": "string", "description": "Nome del cliente (ricerca parziale). Opzionale."},
                    "anno": {"type": "integer", "description": "Anno di riferimento (es. 2026). Opzionale."},
                    "status": {"type": "string", "description": "Stato dell'ordine (es. undefined_tranches, to_be_invoiced, partially_invoiced, totally_invoiced, invoiced_and_paid, invoiced_and_partially_paid). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_ordini,
    },
    "get_clienti": {
        "definition": Tool(
            name="get_clienti",
            description="Cerca clienti/partner con KPI (numero lead e ordini). Filtrabile per nome e settore.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome o alias del cliente (ricerca parziale). Opzionale."},
                    "sector": {"type": "string", "description": "Settore del cliente (es. manufacturing, financial_services, technology_software, professional_services, marketing_advertising, healthcare_life_sciences, retail_ecommerce, logistics_transportation, construction_real_estate, sports_entertainment). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_clienti,
    },
    "get_contatti": {
        "definition": Tool(
            name="get_contatti",
            description="Cerca contatti persone (nome, ruolo, email, telefono, azienda). Filtrabile per nome e azienda.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "Nome o cognome del contatto (ricerca parziale). Opzionale."},
                    "azienda": {"type": "string", "description": "Nome dell'azienda/partner (ricerca parziale). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_contatti,
    },
}
