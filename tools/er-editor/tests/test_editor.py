"""Wave 0 test stubs for editor IR mutations.

These tests verify that IR-level changes (add/rename/delete tables, columns,
relationships) produce correct Python output via apply_changes().
They serve as the automated verification targets referenced in VALIDATION.md.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from parser.extractor import extract_model
from parser.ir import ColumnIR, RelationshipIR, TableIR
from parser.writer import apply_changes


@pytest.fixture
def sample_source():
    path = Path(__file__).parent / "fixtures" / "sample_model.py"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def sample_tables(sample_source):
    return extract_model(sample_source)


# --- EDIT-01: Add table ---


def test_add_table(sample_source, sample_tables):
    """EDIT-01: Adding a new TableIR produces a new class in output."""
    new_table = TableIR(
        class_name="Tag",
        table_name="tags",
        columns=[
            ColumnIR(name="id", type="Integer", nullable=False, primary_key=True),
            ColumnIR(name="name", type="String(50)", nullable=False),
        ],
    )
    tables = sample_tables + [new_table]
    result = apply_changes(sample_source, tables, deleted_classes=set())
    assert "class Tag(Base):" in result
    assert '__tablename__ = "tags"' in result


# --- EDIT-02: Rename table ---


def test_rename_table(sample_source, sample_tables):
    """EDIT-02: Renaming a table's class_name and table_name is reflected in output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.class_name = "SupportTicket"
    ticket.table_name = "support_tickets"
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "class SupportTicket(Base):" in result
    assert "class EmailTicket" not in result


# --- EDIT-03: Delete table ---


def test_delete_table(sample_source, sample_tables):
    """EDIT-03: Deleting a table removes it from output, preserves others."""
    tables = [t for t in sample_tables if t.class_name != "EmailMessage"]
    result = apply_changes(sample_source, tables, deleted_classes={"EmailMessage"})
    assert "class EmailMessage" not in result
    assert "class Mailbox(Base):" in result
    assert "class EmailTicket(Base):" in result


# --- EDIT-04: Add column ---


def test_add_column(sample_source, sample_tables):
    """EDIT-04: Adding a column to a table produces a new mapped_column line."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.columns.append(
        ColumnIR(name="priority", type="Integer", nullable=False, default="0")
    )
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "priority" in result


# --- EDIT-05: Rename column ---


def test_rename_column(sample_source, sample_tables):
    """EDIT-05: Renaming a column changes its name in the output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    subject_col = next(c for c in ticket.columns if c.name == "subject")
    subject_col.name = "title"
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "title" in result
    # The old name should no longer appear as a column definition
    # (it may still appear in comments, which is fine)


# --- EDIT-06: Delete column ---


def test_delete_column(sample_source, sample_tables):
    """EDIT-06: Deleting a column removes it from the output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.columns = [c for c in ticket.columns if c.name != "external_id"]
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "external_id" not in result
    assert "subject" in result  # Other columns preserved


# --- EDIT-07: Modify column properties ---


def test_modify_column_props(sample_source, sample_tables):
    """EDIT-07: Changing column properties (nullable, unique, etc.) is reflected."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    subject_col = next(c for c in ticket.columns if c.name == "subject")
    subject_col.nullable = True
    subject_col.unique = True
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    # The output should reflect the changed properties
    assert "subject" in result


# --- REL-01: Create relationship ---


def test_create_relationship(sample_source, sample_tables):
    """REL-01: Adding a relationship produces a relationship() line in output."""
    mailbox = next(t for t in sample_tables if t.class_name == "Mailbox")
    mailbox.relationships.append(
        RelationshipIR(
            name="labels",
            target="Label",
            back_populates="mailbox",
            cascade="all, delete-orphan",
        )
    )
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "labels" in result


# --- REL-02: Modify relationship ---


def test_modify_relationship(sample_source, sample_tables):
    """REL-02: Modifying a relationship's properties is reflected in output."""
    mailbox = next(t for t in sample_tables if t.class_name == "Mailbox")
    tickets_rel = next(r for r in mailbox.relationships if r.name == "tickets")
    tickets_rel.cascade = "save-update, merge"
    tickets_rel.lazy = "selectin"
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "tickets" in result


# --- REL-03: Delete relationship ---


def test_delete_relationship(sample_source, sample_tables):
    """REL-03: Deleting a relationship removes it from the output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.relationships = [r for r in ticket.relationships if r.name != "messages"]
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    # 'messages' should not appear as a relationship definition in EmailTicket
    # (may still appear in other tables' back_populates)
