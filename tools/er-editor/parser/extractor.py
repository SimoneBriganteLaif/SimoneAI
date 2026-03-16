"""SQLAlchemy model extractor using libcst.

TDD RED phase: stub only -- extract_model returns empty list.
Implementation will be added in Task 2 (GREEN phase).
"""
from __future__ import annotations

from .ir import TableIR


class ModelExtractor:
    """Stub -- not yet implemented."""

    pass


def extract_model(source: str) -> list[TableIR]:
    """Parse SQLAlchemy model source and return list of TableIR.

    Stub implementation for TDD RED phase -- returns empty list.
    """
    return []
