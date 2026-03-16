"""Sample SQLAlchemy 2.0 model for testing the ER parser.

Based on real LAIF model patterns (jubatus email_sync).
Contains: 1 non-ORM class (Enum), 3 ORM tables with relationships.
"""
import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TicketStatus(enum.Enum):
    """Non-ORM class -- must be skipped by parser."""

    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"


class Mailbox(Base):
    __tablename__ = "mailboxes"
    __table_args__ = {"schema": "prs"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tickets: Mapped[list["EmailTicket"]] = relationship(
        back_populates="mailbox", cascade="all, delete-orphan"
    )


class EmailTicket(Base):
    __tablename__ = "email_tickets"
    __table_args__ = {"schema": "prs"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    mailbox_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("prs.mailboxes.id"), nullable=False, index=True
    )
    external_id: Mapped[str] = mapped_column(String(200), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    mailbox: Mapped["Mailbox"] = relationship(back_populates="tickets")
    messages: Mapped[list["EmailMessage"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan"
    )


class EmailMessage(Base):
    __tablename__ = "email_messages"
    __table_args__ = {"schema": "prs"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("prs.email_tickets.id"), nullable=False, index=True
    )
    body_text: Mapped[str | None] = mapped_column(Text)

    ticket: Mapped["EmailTicket"] = relationship(
        back_populates="messages", lazy="selectin"
    )
