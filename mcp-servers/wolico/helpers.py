"""
Helper riutilizzabili cross-tool: date, filtri, formattazione, error handling, paginazione.
"""

from datetime import date, datetime, timedelta
from typing import Any, Callable, Awaitable

import httpx
from mcp.types import TextContent

from api import api_post


def week_bounds(data_str: str | None = None) -> tuple[str, str]:
    """Restituisce (lunedì, domenica) della settimana contenente `data_str`."""
    if data_str:
        d = datetime.strptime(data_str, "%Y-%m-%d").date()
    else:
        d = date.today()
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return str(monday), str(sunday)


def employee_name(emp: dict) -> str:
    """Estrae il nome completo da un record employee."""
    return f"{emp.get('des_name', '')} {emp.get('des_surname', '')}".strip() or "N/D"


def filter_by_employee_name(items: list[dict], query: str) -> list[dict]:
    """Filtra items per nome/cognome dipendente (case-insensitive, parziale)."""
    q = query.strip().lower()
    result = []
    for item in items:
        emp = item.get("employee") or {}
        nome = emp.get("des_name", "").lower()
        cognome = emp.get("des_surname", "").lower()
        nome_completo = f"{nome} {cognome}"
        if q in nome or q in cognome or q in nome_completo:
            result.append(item)
    return result


def group_by_employee(items: list[dict]) -> dict[str, list[dict]]:
    """Raggruppa items per nome dipendente. Chiave = nome display."""
    groups: dict[str, list[dict]] = {}
    for item in items:
        emp = item.get("employee") or {}
        name = employee_name(emp)
        groups.setdefault(name, []).append(item)
    return dict(sorted(groups.items()))


def format_date(iso_str: str | None) -> str:
    """Converte una data ISO in formato leggibile (dd/mm/yyyy). Restituisce '—' se vuota."""
    if not iso_str:
        return "—"
    try:
        d = datetime.strptime(iso_str[:10], "%Y-%m-%d")
        return d.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return iso_str


def build_search(*conditions: tuple[str, str, Any]) -> dict | None:
    """Costruisce il payload `search` da condizioni (campo, operatore, valore).

    Se più condizioni insistono su campi diversi, le mette tutte nel dict.
    Se ci sono più condizioni (>1), usa _and per combinarle.
    Ignora condizioni con value=None.
    """
    filtered = [(f, op, v) for f, op, v in conditions if v is not None]
    if not filtered:
        return None

    if len(filtered) == 1:
        field, operator, value = filtered[0]
        return {field: {"operator": operator, "value": value}}

    # Più condizioni → _and
    return {
        "_and": [
            {field: {"operator": operator, "value": value}}
            for field, operator, value in filtered
        ]
    }


async def paginated_search(
    endpoint: str,
    search: dict | None = None,
    *,
    sort_by: str | list[str] | None = None,
    sort_order: str | list[str] | None = None,
    max_results: int = 500,
    page_size: int = 200,
    email: str | None = None,
) -> tuple[list[dict], int]:
    """Recupera tutti i risultati paginando con offset.

    Ritorna (items, total) dove total è il conteggio server-side.
    """
    payload: dict[str, Any] = {"limit": page_size, "offset": 0}
    if search:
        payload["search"] = search
    if sort_by:
        payload["sort_by"] = sort_by
    if sort_order:
        payload["sort_order"] = sort_order

    data = await api_post(endpoint, payload, email=email)
    items = data.get("items", [])
    total = data.get("total", len(items))

    all_items = list(items)

    while len(all_items) < total and len(all_items) < max_results and len(items) == page_size:
        payload["offset"] = len(all_items)
        data = await api_post(endpoint, payload, email=email)
        items = data.get("items", [])
        all_items.extend(items)

    return all_items, total


def truncation_warning(shown: int, total: int) -> str:
    """Restituisce un warning se i risultati sono troncati, stringa vuota altrimenti."""
    if shown < total:
        return f"\n⚠️ Mostrati {shown} su {total} totali. Usa filtri più specifici per restringere."
    return ""


async def safe_call(
    coro: Callable[[], Awaitable[list[TextContent]]],
) -> list[TextContent]:
    """Wrappa un handler con try/except standard per errori API."""
    try:
        return await coro()
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (401, 403):
            return [TextContent(type="text", text=f"Permesso negato (HTTP {e.response.status_code}).")]
        return [TextContent(type="text", text=f"Errore API Wolico: {e.response.status_code} — {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Errore: {e}")]
