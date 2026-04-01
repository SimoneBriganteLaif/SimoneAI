"""Smoke tests for FastAPI server and API endpoints."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure er-editor root is on sys.path so 'server' and 'api' resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import app
from api.routes import set_model_path, _schema_cache


@pytest.fixture(autouse=True)
def _reset_state():
    """Reset module-level state between tests."""
    import api.routes as routes
    routes._model_path = None
    routes._schema_cache = None
    yield
    routes._model_path = None
    routes._schema_cache = None


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_model_path() -> Path:
    return Path(__file__).parent / "fixtures" / "sample_model.py"


def test_server_starts(client):
    """GET / returns 200 and serves the HTML shell."""
    response = client.get("/")
    assert response.status_code == 200
    assert "ER Editor" in response.text


def test_schema_endpoint_no_model(client):
    """GET /api/schema without setting model_path returns 500."""
    response = client.get("/api/schema")
    assert response.status_code == 500


def test_schema_endpoint_with_model(client, sample_model_path):
    """GET /api/schema with a valid model returns parsed tables."""
    set_model_path(sample_model_path)
    response = client.get("/api/schema")
    assert response.status_code == 200
    data = response.json()
    assert "tables" in data
    assert len(data["tables"]) == 3  # Mailbox, EmailTicket, EmailMessage


def test_layout_endpoint_no_sidecar(client, sample_model_path, tmp_path):
    """GET /api/layout returns default when no .er.json exists."""
    # Copy sample model to tmp so there's no .er.json
    model_copy = tmp_path / "model.py"
    model_copy.write_text(sample_model_path.read_text())
    set_model_path(model_copy)

    response = client.get("/api/layout")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == 1
    assert data["positions"] == {}
    assert data["collapsed"] == {}
    assert data["viewport"]["zoom"] == 1.0


@pytest.fixture
def model_in_tmp(sample_model_path, tmp_path) -> Path:
    """Copy sample model to tmp dir so tests can write to it."""
    model_copy = tmp_path / "model.py"
    model_copy.write_text(sample_model_path.read_text(encoding="utf-8"), encoding="utf-8")
    set_model_path(model_copy)
    return model_copy


def test_layout_save_and_load(client, sample_model_path, tmp_path):
    """POST /api/layout saves, GET /api/layout returns same data."""
    model_copy = tmp_path / "model.py"
    model_copy.write_text(sample_model_path.read_text())
    set_model_path(model_copy)

    payload = {
        "positions": {"Mailbox": {"x": 100, "y": 50}},
        "collapsed": {},
        "viewport": {"zoom": 1.0, "panX": 0, "panY": 0},
    }
    response = client.post("/api/layout", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"

    response = client.get("/api/layout")
    assert response.status_code == 200
    data = response.json()
    assert data["positions"]["Mailbox"]["x"] == 100
    assert data["positions"]["Mailbox"]["y"] == 50


# ---------------------------------------------------------------------------
# Save / Preview endpoint tests
# ---------------------------------------------------------------------------


def test_save_schema(client, model_in_tmp):
    """POST /api/schema saves modified IR back to model file on disk."""
    # First get the current schema
    response = client.get("/api/schema")
    assert response.status_code == 200
    tables = response.json()["tables"]

    # Remove EmailMessage table
    filtered = [t for t in tables if t["class_name"] != "EmailMessage"]
    payload = {"tables": filtered, "deleted": ["EmailMessage"]}
    response = client.post("/api/schema", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"

    # Verify file on disk changed
    content = model_in_tmp.read_text(encoding="utf-8")
    assert "class EmailMessage" not in content
    assert "class Mailbox(Base):" in content
    assert "class EmailTicket(Base):" in content


def test_preview_endpoint(client, sample_model_path):
    """POST /api/preview returns generated Python source."""
    set_model_path(sample_model_path)
    response = client.get("/api/schema")
    tables = response.json()["tables"]

    response = client.post("/api/preview", json={"tables": tables})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    code = data["code"]
    assert "class Mailbox(Base):" in code
    assert "class EmailTicket(Base):" in code
    # Should be valid Python
    compile(code, "<preview>", "exec")


def test_save_preserves_comments(client, model_in_tmp):
    """POST /api/schema with unchanged IR preserves comments in file."""
    response = client.get("/api/schema")
    tables = response.json()["tables"]

    # Save unchanged schema
    response = client.post("/api/schema", json={"tables": tables, "deleted": []})
    assert response.status_code == 200

    content = model_in_tmp.read_text(encoding="utf-8")
    assert "Non-ORM class -- must be skipped by parser" in content
    assert "class TicketStatus(enum.Enum):" in content
