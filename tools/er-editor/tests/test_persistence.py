"""Unit tests for .er.json sidecar read/write persistence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure er-editor root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from server import app
from api.routes import set_model_path


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


@pytest.fixture
def model_in_tmp(sample_model_path, tmp_path) -> Path:
    """Copy sample model to tmp_path so sidecar writes don't pollute fixtures."""
    model_copy = tmp_path / "model.py"
    model_copy.write_text(sample_model_path.read_text())
    set_model_path(model_copy)
    return model_copy


def test_save_layout(client, model_in_tmp):
    """POST /api/layout creates .er.json file next to model."""
    payload = {
        "positions": {"Mailbox": {"x": 100, "y": 50}},
        "collapsed": {"Mailbox": True},
        "viewport": {"zoom": 1.5, "panX": 10, "panY": 20},
    }
    response = client.post("/api/layout", json=payload)
    assert response.status_code == 200

    sidecar = model_in_tmp.with_suffix(".er.json")
    assert sidecar.exists()

    data = json.loads(sidecar.read_text())
    assert data["positions"]["Mailbox"]["x"] == 100
    assert data["collapsed"]["Mailbox"] is True
    assert data["viewport"]["zoom"] == 1.5


def test_load_layout_existing(client, model_in_tmp):
    """GET /api/layout returns content from existing .er.json."""
    sidecar = model_in_tmp.with_suffix(".er.json")
    layout_data = {
        "version": 1,
        "positions": {"EmailTicket": {"x": 200, "y": 300}},
        "collapsed": {},
        "viewport": {"zoom": 2.0, "panX": 50, "panY": 60},
    }
    sidecar.write_text(json.dumps(layout_data))

    response = client.get("/api/layout")
    assert response.status_code == 200
    data = response.json()
    assert data["positions"]["EmailTicket"]["x"] == 200
    assert data["viewport"]["zoom"] == 2.0


def test_load_layout_missing(client, model_in_tmp):
    """GET /api/layout returns default when no .er.json exists."""
    sidecar = model_in_tmp.with_suffix(".er.json")
    assert not sidecar.exists()

    response = client.get("/api/layout")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == 1
    assert data["positions"] == {}
    assert data["collapsed"] == {}
    assert data["viewport"]["zoom"] == 1.0
    assert data["viewport"]["panX"] == 0
    assert data["viewport"]["panY"] == 0


def test_sidecar_format(client, model_in_tmp):
    """After saving, .er.json has correct structure with version key."""
    payload = {
        "positions": {"Mailbox": {"x": 10, "y": 20}},
        "collapsed": {"Mailbox": False},
        "viewport": {"zoom": 1.0, "panX": 0, "panY": 0},
    }
    client.post("/api/layout", json=payload)

    sidecar = model_in_tmp.with_suffix(".er.json")
    data = json.loads(sidecar.read_text())

    assert "version" in data
    assert data["version"] == 1
    assert "positions" in data
    assert "collapsed" in data
    assert "viewport" in data


def test_save_overwrites(client, model_in_tmp):
    """Second save overwrites the first -- last write wins."""
    payload1 = {
        "positions": {"Mailbox": {"x": 100, "y": 50}},
        "collapsed": {},
        "viewport": {"zoom": 1.0, "panX": 0, "panY": 0},
    }
    client.post("/api/layout", json=payload1)

    payload2 = {
        "positions": {"Mailbox": {"x": 999, "y": 888}},
        "collapsed": {"Mailbox": True},
        "viewport": {"zoom": 2.5, "panX": 30, "panY": 40},
    }
    client.post("/api/layout", json=payload2)

    sidecar = model_in_tmp.with_suffix(".er.json")
    data = json.loads(sidecar.read_text())
    assert data["positions"]["Mailbox"]["x"] == 999
    assert data["positions"]["Mailbox"]["y"] == 888
    assert data["collapsed"]["Mailbox"] is True
    assert data["viewport"]["zoom"] == 2.5
