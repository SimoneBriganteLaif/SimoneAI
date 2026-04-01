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
    vertices: dict = {}
    groups: list[dict] = []


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


# ---------------------------------------------------------------------------
# Save / Preview endpoints
# ---------------------------------------------------------------------------

class SchemaData(BaseModel):
    tables: list[dict]  # List of TableIR-like dicts
    deleted: list[str] = []  # List of deleted class names


class PreviewData(BaseModel):
    tables: list[dict]


def _dicts_to_ir(raw_tables: list[dict]):
    """Convert a list of plain dicts to TableIR dataclasses."""
    from parser.ir import TableIR, ColumnIR, RelationshipIR

    tables = []
    for t in raw_tables:
        columns = [ColumnIR(**c) for c in t.get("columns", [])]
        relationships = [RelationshipIR(**r) for r in t.get("relationships", [])]
        tables.append(TableIR(
            class_name=t["class_name"],
            table_name=t["table_name"],
            schema=t.get("schema"),
            columns=columns,
            relationships=relationships,
        ))
    return tables


@router.post("/schema")
def save_schema(data: SchemaData):
    """Save modified IR back to model.py, preserving comments and formatting."""
    if _model_path is None:
        raise HTTPException(status_code=500, detail="No model file configured")

    from parser.writer import apply_changes

    tables = _dicts_to_ir(data.tables)
    original_source = _model_path.read_text(encoding="utf-8")
    new_source = apply_changes(original_source, tables, set(data.deleted))
    _model_path.write_text(new_source, encoding="utf-8")

    # Invalidate schema cache
    global _schema_cache
    _schema_cache = None

    return {"status": "saved"}


@router.post("/preview")
def get_preview(data: PreviewData):
    """Generate preview Python source from IR (no disk write)."""
    from parser.writer import generate_preview

    tables = _dicts_to_ir(data.tables)
    code = generate_preview(tables)
    return {"code": code}
