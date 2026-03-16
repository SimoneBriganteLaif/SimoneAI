from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ColumnIR:
    name: str
    type: str  # Display type from mapped_column() first arg, e.g. "String(50)", "Integer"
    nullable: bool = True
    primary_key: bool = False
    foreign_key: str | None = None  # Full FK string, e.g. "prs.mailboxes.id"
    unique: bool = False
    index: bool = False
    default: str | None = None  # Python default value as string
    server_default: str | None = None  # SQL server_default as string


@dataclass
class RelationshipIR:
    name: str  # Attribute name, e.g. "tickets"
    target: str  # Target class name, e.g. "EmailTicket"
    back_populates: str | None = None
    cascade: str | None = None
    lazy: str | None = None
    uselist: bool = True
    order_by: str | None = None


@dataclass
class TableIR:
    class_name: str  # e.g. "EmailTicket"
    table_name: str  # from __tablename__
    schema: str | None = None
    columns: list[ColumnIR] = field(default_factory=list)
    relationships: list[RelationshipIR] = field(default_factory=list)
