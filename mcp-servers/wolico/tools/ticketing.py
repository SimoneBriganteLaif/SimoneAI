"""Tool ticketing: ticket applicazioni LAIF."""

from mcp.types import TextContent, Tool, ToolAnnotations

from api import api_get
from helpers import build_search, paginated_search, truncation_warning, safe_call


def _format_ticket(t: dict) -> str:
    title = t.get("des_title", "N/D")
    status = t.get("cod_status", "?")
    gravity = t.get("cod_gravity", "")
    owner = t.get("owner") or {}
    assegnato = f"{owner.get('des_name', '')} {owner.get('des_surname', '')}".strip() if isinstance(owner, dict) else ""
    app = t.get("application") or {}
    app_name = app.get("app_name", "") if isinstance(app, dict) else ""
    dat = t.get("dat_creation", "")
    msgs = t.get("messages") or []
    n_msgs = len(msgs)

    parts = [f"- [{status}]"]
    if gravity:
        parts.append(f"[{gravity}]")
    parts.append(title)
    if app_name:
        parts.append(f"| app: {app_name}")
    if assegnato:
        parts.append(f"| assegnato: {assegnato}")
    if n_msgs:
        parts.append(f"| {n_msgs} msg")
    if dat:
        parts.append(f"| {dat[:10]}")
    # Aggiungi ID per dettaglio
    tid = t.get("id")
    if tid:
        parts.append(f"| id:{tid}")
    return " ".join(parts)


def _format_ticket_detail(t: dict) -> str:
    title = t.get("des_title", "N/D")
    status = t.get("cod_status", "?")
    gravity = t.get("cod_gravity", "")
    owner = t.get("owner") or {}
    assegnato = f"{owner.get('des_name', '')} {owner.get('des_surname', '')}".strip() if isinstance(owner, dict) else ""
    app = t.get("application") or {}
    app_name = app.get("app_name", "") if isinstance(app, dict) else ""
    dat = t.get("dat_creation", "")
    description = t.get("des_description", "")

    lines = [
        f"Ticket: {title}",
        f"Status: {status}",
    ]
    if gravity:
        lines.append(f"Gravità: {gravity}")
    if app_name:
        lines.append(f"App: {app_name}")
    if assegnato:
        lines.append(f"Assegnato a: {assegnato}")
    if dat:
        lines.append(f"Creato: {dat[:10]}")
    if description:
        lines.append(f"\nDescrizione:\n{description}")

    msgs = t.get("messages") or []
    if msgs:
        lines.append(f"\nMessaggi ({len(msgs)}):")
        for m in msgs:
            user = m.get("user") or {}
            autore = f"{user.get('des_name', '')} {user.get('des_surname', '')}".strip() if isinstance(user, dict) else "?"
            msg_dat = m.get("dat_creation", "")[:10]
            msg_text = m.get("des_message", "")
            lines.append(f"  [{msg_dat}] {autore}: {msg_text}")

    updates = t.get("updates") or []
    if updates:
        lines.append(f"\nAggiornamenti ({len(updates)}):")
        for u in updates:
            lines.append(f"  - {u.get('des_update', '')}")

    return "\n".join(lines)


async def handle_get_ticket(args: dict) -> list[TextContent]:
    app_name = args.get("app_name")
    status = args.get("status")
    owner = args.get("owner")
    gravity = args.get("gravity")
    category = args.get("category")
    search_text = args.get("search_text")

    async def _run():
        # owner viene cercato via search_concat (la dot notation owner.des_name non è supportata)
        text_query = search_text or owner
        conditions = []
        if status:
            conditions.append(("cod_status", "eq", status))
        if gravity:
            conditions.append(("cod_gravity", "eq", gravity))
        if category:
            conditions.append(("cod_category", "eq", category))
        if app_name:
            conditions.append(("application.app_name", "like", app_name))
        if text_query:
            conditions.append(("search_concat", "like", text_query))

        search = build_search(*conditions)
        items, total = await paginated_search(
            "/application_ticket/search",
            search,
            sort_by="dat_creation",
            sort_order="desc",
        )

        if not items:
            return [TextContent(type="text", text="Nessun ticket trovato con i filtri specificati.")]

        lines = [f"Ticket ({len(items)} risultati, {total} totali):\n"]
        lines.extend(_format_ticket(t) for t in items)
        warning = truncation_warning(len(items), total)
        if warning:
            lines.append(warning)
        return [TextContent(type="text", text="\n".join(lines))]

    return await safe_call(_run)


async def handle_get_ticket_dettaglio(args: dict) -> list[TextContent]:
    ticket_id = args["id_ticket"]

    async def _run():
        data = await api_get(f"/application_ticket/{ticket_id}")
        if not data:
            return [TextContent(type="text", text=f"Ticket {ticket_id} non trovato.")]
        return [TextContent(type="text", text=_format_ticket_detail(data))]

    return await safe_call(_run)


TOOLS = {
    "get_ticket": {
        "definition": Tool(
            name="get_ticket",
            description=(
                "Cerca ticket delle applicazioni LAIF. Filtrabile per app, status, assegnatario, gravità, categoria e testo libero.\n\n"
                "Status: open, work_in_progress, feature, waiting_customer, solved, closed\n"
                "Gravità: low, medium, high\n"
                "Categoria: data_not_updated, incorrect_data, incorrect_behavior, visibility_issue\n\n"
                "Ordinati per data creazione (più recenti prima)."
            ),
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Nome dell'applicazione (ricerca parziale, case-insensitive). Opzionale."},
                    "status": {"type": "string", "description": "Status del ticket. Valori: open, work_in_progress, feature, waiting_customer, solved, closed. Opzionale."},
                    "owner": {"type": "string", "description": "Nome dell'assegnatario o creatore (ricerca full-text su titolo, messaggi, nomi). Opzionale."},
                    "gravity": {"type": "string", "description": "Gravità del ticket. Valori: low, medium, high. Opzionale."},
                    "category": {"type": "string", "description": "Categoria del ticket. Valori: data_not_updated, incorrect_data, incorrect_behavior, visibility_issue. Opzionale."},
                    "search_text": {"type": "string", "description": "Testo da cercare in titolo, messaggi, nomi (full-text). Opzionale."},
                },
                "required": [],
            },
        ),
        "handler": handle_get_ticket,
    },
    "get_ticket_dettaglio": {
        "definition": Tool(
            name="get_ticket_dettaglio",
            description="Dettaglio completo di un ticket: descrizione, messaggi, aggiornamenti. Richiede l'ID del ticket.",
            annotations=ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "id_ticket": {"type": "integer", "description": "ID numerico del ticket"},
                },
                "required": ["id_ticket"],
            },
        ),
        "handler": handle_get_ticket_dettaglio,
    },
}
