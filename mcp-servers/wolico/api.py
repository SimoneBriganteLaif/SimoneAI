"""
Wolico API client — autenticazione JWT e HTTP helpers.

Login via OAuth2PasswordRequestForm, token in memoria con retry su 401.

Modalità:
- Locale (stdio): credenziali da .env
- Lambda (remoto): email dall'header X-Wolico-Email, password da Secrets Manager
"""

import json as _json
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

BASE_URL = os.getenv("WOLICO_BASE_URL", "https://wolico.app.laifgroup.com/api/")
EMAIL = os.getenv("WOLICO_EMAIL", "")
PASSWORD = os.getenv("WOLICO_PASSWORD", "")

# Cache JWT per-email (per multi-utente Lambda)
_jwt_cache: dict[str, str] = {}

# Cache credenziali Secrets Manager
_secrets_cache: dict | None = None


def _get_secrets() -> dict:
    """Carica credenziali da AWS Secrets Manager (solo in Lambda)."""
    global _secrets_cache
    if _secrets_cache is not None:
        return _secrets_cache

    secret_name = os.getenv("WOLICO_SECRET_NAME")
    if not secret_name:
        _secrets_cache = {}
        return _secrets_cache

    try:
        import boto3
        client = boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION", "eu-west-1"))
        resp = client.get_secret_value(SecretId=secret_name)
        _secrets_cache = _json.loads(resp["SecretString"])
    except Exception:
        _secrets_cache = {}
    return _secrets_cache


def get_password_for_email(email: str) -> str:
    """Risolve la password per un'email: env locale o Secrets Manager."""
    if email == EMAIL and PASSWORD:
        return PASSWORD
    secrets = _get_secrets()
    pwd = secrets.get(email, "")
    if not pwd:
        raise ValueError(f"Credenziali non trovate per {email}")
    return pwd


async def _get_token(email: str | None = None) -> str:
    """Ottiene il JWT via form-urlencoded (OAuth2PasswordRequestForm)."""
    _email = email or EMAIL
    if _email in _jwt_cache:
        return _jwt_cache[_email]

    _password = get_password_for_email(_email)

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        resp = await client.post(
            "/auth/login",
            data={"username": _email, "password": _password},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise ValueError(f"Token non trovato nella risposta: {list(data.keys())}")
        _jwt_cache[_email] = token
        return token


async def api_request(
    method: str,
    path: str,
    *,
    json: dict | None = None,
    params: dict | None = None,
    email: str | None = None,
) -> Any:
    """Richiesta HTTP autenticata generica. Rinnova il token su 401."""
    _email = email or EMAIL
    token = await _get_token(_email)

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        kwargs: dict[str, Any] = {
            "headers": {"Authorization": f"Bearer {token}"},
            "timeout": 30,
        }
        if json is not None:
            kwargs["json"] = json
        if params is not None:
            kwargs["params"] = params

        resp = await client.request(method, path, **kwargs)

        if resp.status_code == 401:
            _jwt_cache.pop(_email, None)
            token = await _get_token(_email)
            kwargs["headers"] = {"Authorization": f"Bearer {token}"}
            resp = await client.request(method, path, **kwargs)

        resp.raise_for_status()
        return resp.json()


async def api_get(path: str, params: dict | None = None, *, email: str | None = None) -> Any:
    return await api_request("GET", path, params=params, email=email)


async def api_post(path: str, payload: dict | None = None, *, email: str | None = None) -> Any:
    return await api_request("POST", path, json=payload, email=email)
