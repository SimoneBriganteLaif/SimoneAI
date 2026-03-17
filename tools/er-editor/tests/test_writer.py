"""TDD tests for the round-trip writer (libcst CSTTransformer).

Tests verify that apply_changes() modifies model.py source correctly,
preserving comments, blank lines, and formatting on identity transform.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from parser.extractor import extract_model
from parser.ir import ColumnIR, RelationshipIR, TableIR
from parser.writer import apply_changes, generate_preview


@pytest.fixture
def sample_source():
    path = Path(__file__).parent / "fixtures" / "sample_model.py"
    return path.read_text(encoding="utf-8")


@pytest.fixture
def sample_tables(sample_source):
    return extract_model(sample_source)


def test_roundtrip_identity(sample_source, sample_tables):
    """Unchanged IR produces identical output (byte-for-byte minus trailing ws)."""
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert result.rstrip() == sample_source.rstrip()


def test_rename_table(sample_source, sample_tables):
    """Renaming class_name and table_name is reflected in output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.class_name = "SupportTicket"
    ticket.table_name = "support_tickets"
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "class SupportTicket(Base):" in result
    assert '__tablename__ = "support_tickets"' in result
    assert "class EmailTicket" not in result
    # Other classes and comments unchanged
    assert "class Mailbox(Base):" in result
    assert "class TicketStatus(enum.Enum):" in result


def test_delete_table(sample_source, sample_tables):
    """Deleted table removed from output, others preserved, comments preserved."""
    tables = [t for t in sample_tables if t.class_name != "EmailMessage"]
    result = apply_changes(sample_source, tables, deleted_classes={"EmailMessage"})
    assert "class EmailMessage" not in result
    assert "class Mailbox(Base):" in result
    assert "class EmailTicket(Base):" in result
    # Non-ORM classes preserved
    assert "class TicketStatus(enum.Enum):" in result
    assert "Non-ORM class -- must be skipped by parser" in result


def test_add_column(sample_source, sample_tables):
    """Adding a column to a table produces a new mapped_column line."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.columns.append(
        ColumnIR(name="priority", type="Integer", nullable=False, default="0")
    )
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "priority" in result
    assert "mapped_column" in result.split("priority")[1].split("\n")[0]


def test_delete_column(sample_source, sample_tables):
    """Deleting a column removes it, other columns preserved."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.columns = [c for c in ticket.columns if c.name != "external_id"]
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    assert "external_id" not in result
    assert "subject" in result
    assert "mailbox_id" in result


def test_modify_column_nullable(sample_source, sample_tables):
    """Changing column nullable is reflected in output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    subject_col = next(c for c in ticket.columns if c.name == "subject")
    subject_col.nullable = True
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    # subject line should exist and reflect nullable change
    assert "subject" in result
    # The line should no longer have nullable=False
    for line in result.split("\n"):
        if "subject" in line and "mapped_column" in line:
            assert "nullable=False" not in line
            break


def test_add_new_table(sample_source, sample_tables):
    """Adding a new TableIR appends a class at end with PEP 8 spacing."""
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
    # Should have 2 blank lines before the new class (PEP 8)
    idx = result.index("class Tag(Base):")
    before = result[:idx]
    # Count trailing newlines before the class
    lines_before = before.rstrip(" ").split("\n")
    # Last 2 lines before class should be empty
    assert lines_before[-1].strip() == ""
    assert lines_before[-2].strip() == ""


def test_add_relationship(sample_source, sample_tables):
    """Adding a relationship produces a relationship() line in output."""
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
    assert "relationship(" in result.split("labels")[1].split("\n")[0]


def test_delete_relationship(sample_source, sample_tables):
    """Deleting a relationship removes it from output."""
    ticket = next(t for t in sample_tables if t.class_name == "EmailTicket")
    ticket.relationships = [r for r in ticket.relationships if r.name != "messages"]
    result = apply_changes(sample_source, sample_tables, deleted_classes=set())
    # 'messages' should not appear as a relationship definition in EmailTicket
    # It may still appear in EmailMessage's back_populates, which is fine
    lines = result.split("\n")
    in_ticket = False
    for line in lines:
        if "class EmailTicket" in line:
            in_ticket = True
        elif in_ticket and line.strip().startswith("class "):
            in_ticket = False
        elif in_ticket and "messages" in line and "relationship(" in line:
            pytest.fail("messages relationship should be deleted from EmailTicket")


def test_generate_preview(sample_tables):
    """generate_preview produces valid Python source from IR."""
    code = generate_preview(sample_tables)
    assert "class Mailbox(Base):" in code
    assert "class EmailTicket(Base):" in code
    assert "class EmailMessage(Base):" in code
    # Should be syntactically valid Python
    compile(code, "<preview>", "exec")
