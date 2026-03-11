"""
MCP Server Wolico — Ferie, Staffing, Economics, Dipendenti.

Entry point per:
- Transport stdio (locale, Docker)
- Transport Streamable HTTP (Lambda, remoto)

La logica dei tool è in tools/*.py, le API in api.py.
MCP Resources espongono dati semi-statici (dipendenti, app, clienti, enum).
"""

import asyncio
import os
import time
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool, Resource

from tools import ALL_TOOLS
from api import api_post
from helpers import employee_name

server = Server("wolico")


# ---------------------------------------------------------------------------
# MCP Resources — dati semi-statici con cache TTL
# ---------------------------------------------------------------------------

_resource_cache: dict[str, tuple[float, str]] = {}
_CACHE_TTL = 300  # 5 minuti


def _cache_get(key: str) -> str | None:
    if key in _resource_cache:
        ts, data = _resource_cache[key]
        if time.time() - ts < _CACHE_TTL:
            return data
    return None


def _cache_set(key: str, data: str) -> None:
    _resource_cache[key] = (time.time(), data)


async def _fetch_dipendenti() -> str:
    cached = _cache_get("dipendenti")
    if cached:
        return cached

    payload = {"limit": 500, "offset": 0, "search": {"user.flg_valid": {"operator": "eq", "value": True}}}
    data = await api_post("/employees/search", payload)
    items = data.get("items", [])

    lines = [f"Dipendenti attivi ({len(items)}):\n"]
    for emp in items:
        name = employee_name(emp)
        role = emp.get("des_role", "")
        company = emp.get("company", "")
        emp_id = emp.get("id", "")
        parts = [f"- {name}"]
        if role:
            parts.append(f"({role})")
        if company:
            parts.append(f"[{company}]")
        if emp_id:
            parts.append(f"id:{emp_id}")
        lines.append(" ".join(parts))

    result = "\n".join(lines)
    _cache_set("dipendenti", result)
    return result


async def _fetch_applicazioni() -> str:
    cached = _cache_get("applicazioni")
    if cached:
        return cached

    payload = {"limit": 500, "offset": 0}
    data = await api_post("/applications/search", payload)
    items = data.get("items", [])

    lines = [f"Applicazioni ({len(items)}):\n"]
    for app in items:
        app_name = app.get("app_name", "N/D")
        env = app.get("env", "")
        status = app.get("project_status", "")
        partner = app.get("partner") or {}
        partner_name = partner.get("name", "") if isinstance(partner, dict) else ""
        parts = [f"- {app_name}"]
        if env:
            parts.append(f"[{env}]")
        if status:
            parts.append(f"({status})")
        if partner_name:
            parts.append(f"| cliente: {partner_name}")
        lines.append(" ".join(parts))

    result = "\n".join(lines)
    _cache_set("applicazioni", result)
    return result


async def _fetch_clienti() -> str:
    cached = _cache_get("clienti")
    if cached:
        return cached

    payload = {"limit": 500, "offset": 0}
    data = await api_post("/partners/search", payload)
    items = data.get("items", [])

    lines = [f"Clienti/Partner ({len(items)}):\n"]
    for p in items:
        name = p.get("name", "N/D")
        alias = p.get("alias", "")
        sector = p.get("cod_sector", "")
        parts = [f"- {name}"]
        if alias:
            parts.append(f"({alias})")
        if sector:
            parts.append(f"[{sector}]")
        lines.append(" ".join(parts))

    result = "\n".join(lines)
    _cache_set("clienti", result)
    return result


def _get_enum_resource() -> str:
    return """Valori enum disponibili nel sistema Wolico:

TicketStatus: open, work_in_progress, feature, waiting_customer, solved, closed
TicketGravity: low, medium, high
TicketCategory: data_not_updated, incorrect_data, incorrect_behavior, visibility_issue

ErrorStatus: unassigned, assigned, in_progress, fixed, to_ignore

ProjectStatus: development, maintenance, retired

LeadStatus: new, qualified, proposition, won, freezed, lost

SalesStatus: undefined_tranches, to_be_invoiced, partially_invoiced, totally_invoiced, invoiced_and_paid, invoiced_and_partially_paid

PartnerSector: manufacturing, financial_services, technology_software, healthcare, energy, retail, public_sector, logistics, food, other

Companies: laif, helia

OutageType: ferie, permesso, malattia, smartworking, trasferta
"""


RESOURCES = {
    "wolico://dipendenti": {
        "resource": Resource(
            uri="wolico://dipendenti",
            name="Lista dipendenti attivi",
            description="Elenco completo dei dipendenti attivi con nome, ruolo e company. Utile per risolvere nomi ambigui.",
            mimeType="text/plain",
        ),
        "handler": _fetch_dipendenti,
    },
    "wolico://applicazioni": {
        "resource": Resource(
            uri="wolico://applicazioni",
            name="Lista applicazioni LAIF",
            description="Elenco completo delle applicazioni gestite con nome, ambiente, stato e cliente.",
            mimeType="text/plain",
        ),
        "handler": _fetch_applicazioni,
    },
    "wolico://clienti": {
        "resource": Resource(
            uri="wolico://clienti",
            name="Lista clienti/partner",
            description="Elenco completo dei clienti e partner con nome, alias e settore.",
            mimeType="text/plain",
        ),
        "handler": _fetch_clienti,
    },
    "wolico://enum": {
        "resource": Resource(
            uri="wolico://enum",
            name="Valori enum sistema",
            description="Tutti i valori enum disponibili: status ticket, gravità, categorie, status errori, status progetti, status lead/ordini, settori partner, company.",
            mimeType="text/plain",
        ),
        "handler": _get_enum_resource,
    },
}


@server.list_resources()
async def list_resources() -> list[Resource]:
    return [r["resource"] for r in RESOURCES.values()]


@server.read_resource()
async def read_resource(uri: str) -> str:
    uri_str = str(uri)
    entry = RESOURCES.get(uri_str)
    if not entry:
        raise ValueError(f"Resource sconosciuta: {uri_str}")
    handler = entry["handler"]
    if asyncio.iscoroutinefunction(handler):
        return await handler()
    return handler()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [t["definition"] for t in ALL_TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handler = ALL_TOOLS.get(name, {}).get("handler")
    if handler:
        return await handler(arguments)
    return [TextContent(type="text", text=f"Tool sconosciuto: {name}")]


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------

async def _run_stdio():
    """Transport stdio per uso locale."""
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            server.create_initialization_options(),
        )


def _create_http_app():
    """Crea app ASGI con Streamable HTTP per deploy remoto (Lambda/container)."""
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.applications import Starlette
    from starlette.routing import Mount

    session_manager = StreamableHTTPSessionManager(
        app=server,
        stateless=True,
        json_response=True,
    )

    app = Starlette(
        routes=[
            Mount("/mcp", app=session_manager.handle_request),
        ],
    )
    return app


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "http":
        import uvicorn
        app = _create_http_app()
        port = int(os.getenv("PORT", "8080"))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        asyncio.run(_run_stdio())
