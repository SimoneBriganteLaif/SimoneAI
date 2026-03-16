"""Unit tests for the SQLAlchemy model parser.

TDD RED phase: all tests written against expected behavior.
The extractor implementation does not exist yet -- all tests must FAIL.
"""
import json
from dataclasses import asdict

from parser.ir import ColumnIR, RelationshipIR, TableIR


def test_extract_tables(parsed_tables: list[TableIR]):
    """Given sample_model.py with 3 ORM classes + 1 Enum, extractor returns exactly 3 TableIR objects."""
    assert len(parsed_tables) == 3
    class_names = {t.class_name for t in parsed_tables}
    assert class_names == {"Mailbox", "EmailTicket", "EmailMessage"}
    table_names = {t.table_name for t in parsed_tables}
    assert table_names == {"mailboxes", "email_tickets", "email_messages"}


def test_extract_columns_basic(parsed_tables: list[TableIR]):
    """Given Mailbox table, extractor returns correct column types and constraints."""
    mailbox = next(t for t in parsed_tables if t.class_name == "Mailbox")
    cols = {c.name: c for c in mailbox.columns}

    # id: Integer, PK
    assert cols["id"].type == "Integer"
    assert cols["id"].primary_key is True
    assert cols["id"].nullable is False  # PK implies not nullable

    # email_address: String(255), not nullable
    assert cols["email_address"].type == "String(255)"
    assert cols["email_address"].nullable is False

    # display_name: String(100), nullable (Mapped[str | None])
    assert cols["display_name"].type == "String(100)"
    assert cols["display_name"].nullable is True

    # is_active: Boolean
    assert cols["is_active"].type == "Boolean"


def test_extract_columns_fk(parsed_tables: list[TableIR]):
    """Given EmailTicket.mailbox_id with ForeignKey, extractor returns correct FK string."""
    ticket = next(t for t in parsed_tables if t.class_name == "EmailTicket")
    mailbox_id_col = next(c for c in ticket.columns if c.name == "mailbox_id")
    assert mailbox_id_col.foreign_key == "prs.mailboxes.id"


def test_extract_columns_nullable(parsed_tables: list[TableIR]):
    """Mapped[str | None] -> nullable=True; Mapped[str] -> nullable=False."""
    mailbox = next(t for t in parsed_tables if t.class_name == "Mailbox")
    cols = {c.name: c for c in mailbox.columns}

    # Mapped[str | None] -> nullable
    assert cols["display_name"].nullable is True

    # Mapped[str] with nullable=False -> not nullable
    assert cols["email_address"].nullable is False

    # Mapped[int] (PK) -> not nullable
    assert cols["id"].nullable is False


def test_extract_columns_default(parsed_tables: list[TableIR]):
    """mapped_column(default=True) -> default='True'; server_default=text('now()') -> server_default='now()'."""
    mailbox = next(t for t in parsed_tables if t.class_name == "Mailbox")
    is_active = next(c for c in mailbox.columns if c.name == "is_active")
    assert is_active.default == "True"

    ticket = next(t for t in parsed_tables if t.class_name == "EmailTicket")
    created_at = next(c for c in ticket.columns if c.name == "created_at")
    assert created_at.server_default == "now()"


def test_extract_relationships(parsed_tables: list[TableIR]):
    """Given Mailbox.tickets relationship, extractor returns correct RelationshipIR."""
    mailbox = next(t for t in parsed_tables if t.class_name == "Mailbox")
    rels = {r.name: r for r in mailbox.relationships}

    assert "tickets" in rels
    assert rels["tickets"].target == "EmailTicket"
    assert rels["tickets"].back_populates == "mailbox"
    assert rels["tickets"].cascade == "all, delete-orphan"


def test_extract_relationship_uselist(parsed_tables: list[TableIR]):
    """list[X] annotation -> uselist=True; bare X -> uselist=False."""
    mailbox = next(t for t in parsed_tables if t.class_name == "Mailbox")
    tickets_rel = next(r for r in mailbox.relationships if r.name == "tickets")
    # Mapped[list["EmailTicket"]] -> uselist=True
    assert tickets_rel.uselist is True

    ticket = next(t for t in parsed_tables if t.class_name == "EmailTicket")
    mailbox_rel = next(r for r in ticket.relationships if r.name == "mailbox")
    # Mapped["Mailbox"] (no list) -> uselist=False
    assert mailbox_rel.uselist is False


def test_table_args_schema(parsed_tables: list[TableIR]):
    """__table_args__ = {'schema': 'prs'} -> schema='prs' on all tables."""
    for table in parsed_tables:
        assert table.schema == "prs", f"{table.class_name} should have schema='prs'"


def test_orm_detection_by_tablename(parsed_tables: list[TableIR]):
    """Class with __tablename__ is extracted; class without (Enum, Pydantic, mixin) is skipped."""
    class_names = {t.class_name for t in parsed_tables}
    # TicketStatus is an Enum -- no __tablename__, must NOT appear
    assert "TicketStatus" not in class_names
    # Base is the DeclarativeBase -- no __tablename__, must NOT appear
    assert "Base" not in class_names
    # The 3 ORM classes must appear
    assert "Mailbox" in class_names
    assert "EmailTicket" in class_names
    assert "EmailMessage" in class_names


def test_extract_columns_index(parsed_tables: list[TableIR]):
    """mapped_column(index=True) -> index=True."""
    ticket = next(t for t in parsed_tables if t.class_name == "EmailTicket")
    mailbox_id_col = next(c for c in ticket.columns if c.name == "mailbox_id")
    assert mailbox_id_col.index is True

    # Non-indexed column
    subject_col = next(c for c in ticket.columns if c.name == "subject")
    assert subject_col.index is False


def test_asdict_serializable(parsed_tables: list[TableIR]):
    """dataclasses.asdict(table_ir) produces a dict; json.dumps() succeeds."""
    for table in parsed_tables:
        d = asdict(table)
        assert isinstance(d, dict)
        # Must not raise
        serialized = json.dumps(d)
        assert isinstance(serialized, str)
        # Round-trip
        loaded = json.loads(serialized)
        assert loaded["class_name"] == table.class_name
