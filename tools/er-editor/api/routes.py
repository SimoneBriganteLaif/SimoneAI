from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

_model_path: Path | None = None
_schema_cache: list[dict] | None = None


def set_model_path(path: Path):
    global _model_path, _schema_cache
    _model_path = path
    _schema_cache = None


def _get_sidecar_path() -> Path:
    """Return .er.json path next to model.py"""
    return _model_path.with_suffix('.er.json')


def _parse_schema() -> list[dict]:
    global _schema_cache
    if _schema_cache is not None:
        return _schema_cache
    from parser.extractor import extract_model
    source = _model_path.read_text(encoding='utf-8')
    tables = extract_model(source)
    _schema_cache = [asdict(t) for t in tables]
    return _schema_cache


@router.get("/schema")
def get_schema():
    if _model_path is None:
        raise HTTPException(status_code=500, detail="No model file configured")
    try:
        tables = _parse_schema()
        return {"tables": tables, "file": _model_path.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse model file. {str(e)}")


class LayoutData(BaseModel):
    positions: dict = {}
    collapsed: dict = {}
    viewport: dict = {}


@router.get("/layout")
def get_layout():
    sidecar = _get_sidecar_path()
    if sidecar.exists():
        data = json.loads(sidecar.read_text(encoding='utf-8'))
        return data
    return {"version": 1, "positions": {}, "collapsed": {}, "viewport": {"zoom": 1.0, "panX": 0, "panY": 0}}


@router.post("/layout")
def save_layout(data: LayoutData):
    sidecar = _get_sidecar_path()
    payload = {"version": 1, **data.model_dump()}
    sidecar.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return {"status": "saved"}
