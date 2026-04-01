#!/usr/bin/env python3
"""
Microsoft Graph API client per Claude Code.

Usa Device Code Flow con app registration custom per accedere a
email, calendario, chat, SharePoint tramite Microsoft Graph API.

Uso:
    # Prima autenticazione (apre browser)
    python3 graph_client.py login

    # Chiamate Graph API
    python3 graph_client.py get /me
    python3 graph_client.py get '/me/mailFolders/sentItems/messages?$top=5&$select=subject,sentDateTime'
    python3 graph_client.py get '/me/calendarView?startDateTime=2026-03-23T00:00:00Z&endDateTime=2026-03-24T00:00:00Z'
    python3 graph_client.py post /me/sendMail --body '{"message":{...}}'

    # Stato autenticazione
    python3 graph_client.py status
"""

from __future__ import annotations

import json
import sys
import os
import argparse
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import msal

# --- Configurazione ---

CLIENT_ID = "1a3217aa-10bc-447b-b860-896d37803ed7"
TENANT_ID = "9d2d3235-3ba1-432b-a3bd-c6af84e530ed"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

SCOPES = [
    "User.Read",
    "Mail.Read",
    "Mail.ReadWrite",
    "Calendars.Read",
    "Calendars.Read.Shared",
    "Calendars.ReadBasic",
    "Calendars.ReadWrite",
    "Chat.Read",
    "ChatMessage.Read",
    "Contacts.Read",
    "Files.Read",
    "Files.Read.All",
    "MailboxSettings.Read",
    "OnlineMeetings.Read",
    "OnlineMeetingArtifact.Read.All",
    "People.Read",
]

# Token cache persistente
SCRIPT_DIR = Path(__file__).resolve().parent
TOKEN_CACHE_FILE = SCRIPT_DIR / ".token_cache.json"


def _get_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_FILE.exists():
        cache.deserialize(TOKEN_CACHE_FILE.read_text())
    return cache


def _save_cache(cache: msal.SerializableTokenCache) -> None:
    if cache.has_state_changed:
        TOKEN_CACHE_FILE.write_text(cache.serialize())
        TOKEN_CACHE_FILE.chmod(0o600)


def _get_app(cache: msal.SerializableTokenCache) -> msal.PublicClientApplication:
    return msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache,
    )


def _get_token_silent(app: msal.PublicClientApplication) -> dict | None:
    accounts = app.get_accounts()
    if not accounts:
        return None
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if result and "access_token" in result:
        return result
    return None


def do_login() -> str:
    cache = _get_cache()
    app = _get_app(cache)

    # Prova silent refresh prima
    result = _get_token_silent(app)
    if result:
        _save_cache(cache)
        account = app.get_accounts()[0]
        print(json.dumps({
            "status": "already_authenticated",
            "account": account.get("username", "unknown"),
        }))
        return result["access_token"]

    # Device Code Flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(json.dumps({"error": "Device code flow failed", "details": flow}), file=sys.stderr)
        sys.exit(1)

    # Mostra istruzioni all'utente
    print(json.dumps({
        "action": "device_code_login",
        "message": flow["message"],
        "user_code": flow["user_code"],
        "verification_uri": flow.get("verification_uri", "https://microsoft.com/devicelogin"),
    }))

    # Attende completamento (blocca fino a login o timeout)
    result = app.acquire_token_by_device_flow(flow)
    _save_cache(cache)

    if "access_token" in result:
        account = result.get("id_token_claims", {}).get("preferred_username", "unknown")
        print(json.dumps({"status": "login_successful", "account": account}))
        return result["access_token"]
    else:
        print(json.dumps({"error": "Login failed", "details": result}), file=sys.stderr)
        sys.exit(1)


def get_token() -> str:
    cache = _get_cache()
    app = _get_app(cache)
    result = _get_token_silent(app)
    if result:
        _save_cache(cache)
        return result["access_token"]

    print(json.dumps({"error": "Not authenticated. Run: python3 graph_client.py login"}), file=sys.stderr)
    sys.exit(1)


def graph_request(method: str, path: str, body: str | None = None) -> None:
    token = get_token()

    url = path if path.startswith("http") else f"{GRAPH_BASE}{path if path.startswith('/') else '/' + path}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = Request(url, method=method.upper(), headers=headers)
    if body:
        req.data = body.encode("utf-8")

    try:
        with urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            if data:
                print(json.dumps(json.loads(data), ensure_ascii=False, indent=2))
            else:
                print(json.dumps({"status": "success", "http_code": resp.status}))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
        except json.JSONDecodeError:
            error_json = {"raw": error_body}
        print(json.dumps({
            "error": True,
            "http_code": e.code,
            "details": error_json,
        }, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


def do_status() -> None:
    cache = _get_cache()
    app = _get_app(cache)
    accounts = app.get_accounts()

    if not accounts:
        print(json.dumps({"authenticated": False, "message": "No cached account. Run: python3 graph_client.py login"}))
        return

    result = _get_token_silent(app)
    _save_cache(cache)

    print(json.dumps({
        "authenticated": result is not None,
        "account": accounts[0].get("username", "unknown"),
        "token_valid": "access_token" in result if result else False,
    }))


def main():
    parser = argparse.ArgumentParser(description="Microsoft Graph API client")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("login", help="Authenticate via Device Code Flow")
    sub.add_parser("status", help="Show authentication status")

    get_p = sub.add_parser("get", help="GET request to Graph API")
    get_p.add_argument("path", help="Graph API path (e.g. /me/messages)")

    post_p = sub.add_parser("post", help="POST request to Graph API")
    post_p.add_argument("path", help="Graph API path")
    post_p.add_argument("--body", required=True, help="JSON body")

    patch_p = sub.add_parser("patch", help="PATCH request to Graph API")
    patch_p.add_argument("path", help="Graph API path")
    patch_p.add_argument("--body", required=True, help="JSON body")

    del_p = sub.add_parser("delete", help="DELETE request to Graph API")
    del_p.add_argument("path", help="Graph API path")

    args = parser.parse_args()

    if args.command == "login":
        do_login()
    elif args.command == "status":
        do_status()
    elif args.command in ("get", "post", "patch", "delete"):
        body = getattr(args, "body", None)
        graph_request(args.command, args.path, body)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
