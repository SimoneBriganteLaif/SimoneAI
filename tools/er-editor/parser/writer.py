"""Round-trip writer using libcst CSTTransformer.

Applies IR changes to the original model.py source, preserving all
comments, whitespace, and formatting. This is the inverse of the
ModelExtractor (CSTVisitor).
"""
from __future__ import annotations

from typing import Optional, Sequence, Set, Union

import libcst as cst

from .ir import ColumnIR, RelationshipIR, TableIR
from .extractor import extract_model


# ---------------------------------------------------------------------------
# Type annotation helpers
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "Integer": "int",
    "String": "str",
    "Text": "str",
    "Boolean": "bool",
    "Float": "float",
    "DateTime": "datetime",
    "Date": "date",
    "UUID": "uuid.UUID",
    "JSON": "dict",
}


def _type_to_annotation(col: ColumnIR) -> str:
    """Convert ColumnIR to Mapped[] annotation string."""
    # Handle Enum types: use the enum class name as the annotation type
    if col.type.startswith("Enum(") and col.type.endswith(")"):
        enum_class = col.type[5:-1]  # Extract class name from "Enum(ClassName)"
        if col.nullable:
            return f"Mapped[{enum_class} | None]"
        return f"Mapped[{enum_class}]"

    # Extract base type name (e.g. "String(50)" -> "String")
    base = col.type.split("(")[0] if col.type else "str"
    py_type = _TYPE_MAP.get(base, "str")

    if col.primary_key:
        return f"Mapped[{py_type}]"
    if col.nullable:
        return f"Mapped[{py_type} | None]"
    return f"Mapped[{py_type}]"


# ---------------------------------------------------------------------------
# Source builders (for new classes/columns/relationships)
# ---------------------------------------------------------------------------

def _build_enum_class(enum_name: str, values: list[str]) -> str:
    """Generate a Python Enum class from enum member values.

    Example output:
        class TicketPriority(enum.Enum):
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
    """
    lines = [f"class {enum_name}(enum.Enum):"]
    for val in values:
        member = val.strip().upper().replace(" ", "_").replace("-", "_")
        lines.append(f'    {member} = "{val.strip()}"')
    return "\n".join(lines)


def _resolve_enum_column(col: ColumnIR, class_name: str) -> tuple[str, str | None]:
    """Resolve an Enum column: return (type_string, enum_class_name).

    If the column is an Enum type with enum_values, derives the enum class name
    and returns the Enum(ClassName) type string. Otherwise returns (col.type, None).
    """
    if col.type == "Enum" and col.enum_values:
        # Derive enum class name: {ClassName}{ColumnNameCapitalized}
        col_capitalized = col.name.replace("_", " ").title().replace(" ", "")
        enum_class = f"{class_name}{col_capitalized}"
        return f"Enum({enum_class})", enum_class
    return col.type, None


def _build_column_source(col: ColumnIR, indent: str = "    ") -> str:
    """Generate a single column line like: name: Mapped[str] = mapped_column(String(50), ...)"""
    annotation = _type_to_annotation(col)
    args: list[str] = []

    # First positional: type
    if col.type:
        args.append(col.type)

    # ForeignKey
    if col.foreign_key:
        args.append(f'ForeignKey("{col.foreign_key}")')

    # Keyword args
    if col.primary_key:
        args.append("primary_key=True")
    if not col.nullable and not col.primary_key:
        args.append("nullable=False")
    if col.unique:
        args.append("unique=True")
    if col.index:
        args.append("index=True")
    if col.default is not None:
        args.append(f"default={col.default}")
    if col.server_default is not None:
        args.append(f'server_default=text("{col.server_default}")')

    args_str = ", ".join(args)
    return f"{indent}{col.name}: {annotation} = mapped_column({args_str})"


def _build_relationship_source(rel: RelationshipIR, indent: str = "    ") -> str:
    """Generate a single relationship line."""
    if rel.uselist:
        annotation = f'Mapped[list["{rel.target}"]]'
    else:
        annotation = f'Mapped["{rel.target}"]'

    args: list[str] = []
    if rel.back_populates:
        args.append(f'back_populates="{rel.back_populates}"')
    if rel.cascade:
        args.append(f'cascade="{rel.cascade}"')
    if rel.lazy:
        args.append(f'lazy="{rel.lazy}"')
    if not rel.uselist:
        args.append("uselist=False")
    if rel.order_by:
        args.append(f'order_by="{rel.order_by}"')

    args_str = ", ".join(args)
    return f"{indent}{rel.name}: {annotation} = relationship({args_str})"


def _build_class_source(table: TableIR) -> str:
    """Generate a complete class source string for a new table.

    If any columns are Enum type with enum_values, generates
    the Enum class definitions before the table class.
    """
    enum_blocks: list[str] = []
    resolved_types: dict[str, str] = {}  # col.name -> resolved type

    # Resolve Enum columns first
    for col in table.columns:
        resolved_type, enum_class = _resolve_enum_column(col, table.class_name)
        if enum_class:
            enum_blocks.append(_build_enum_class(enum_class, col.enum_values))
            resolved_types[col.name] = resolved_type

    parts: list[str] = []

    # Enum class definitions (before the table class)
    for block in enum_blocks:
        parts.append(block)
        parts.append("")
        parts.append("")

    # Table class
    lines: list[str] = []
    lines.append(f"class {table.class_name}(Base):")
    lines.append(f'    __tablename__ = "{table.table_name}"')
    if table.schema:
        lines.append(f'    __table_args__ = {{"schema": "{table.schema}"}}')

    # Blank line between table args and columns
    if table.columns or table.relationships:
        lines.append("")

    for col in table.columns:
        if col.name in resolved_types:
            # Use resolved Enum type
            original_type = col.type
            col.type = resolved_types[col.name]
            lines.append(_build_column_source(col))
            col.type = original_type  # Restore
        else:
            lines.append(_build_column_source(col))

    if table.columns and table.relationships:
        lines.append("")

    for rel in table.relationships:
        lines.append(_build_relationship_source(rel))

    parts.append("\n".join(lines))
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CST Transformer
# ---------------------------------------------------------------------------

class ModelWriter(cst.CSTTransformer):
    """CSTTransformer that applies IR changes to model.py source."""

    def __init__(
        self,
        tables: list[TableIR],
        deleted_classes: set[str],
        original_tables: list[TableIR],
    ) -> None:
        super().__init__()
        self.tables_by_class: dict[str, TableIR] = {t.class_name: t for t in tables}
        self.original_by_class: dict[str, TableIR] = {
            t.class_name: t for t in original_tables
        }
        self.deleted_classes = deleted_classes
        self._current_class: str | None = None
        self._current_table: TableIR | None = None
        self._current_original: TableIR | None = None
        self._original_class_names: set[str] = set()
        # Track which original class name maps to which new class name (for renames)
        self._rename_map: dict[str, str] = {}  # original_name -> new_name
        # Track Enum class definitions to insert (from new Enum columns on existing tables)
        self._pending_enum_classes: list[tuple[str, str]] = []  # (before_class, enum_source)
        self._build_rename_map(tables, original_tables)

    def _build_rename_map(
        self, tables: list[TableIR], original_tables: list[TableIR]
    ) -> None:
        """Detect renamed classes by comparing original and new table lists.

        A renamed class is one where the original class_name no longer exists
        in the new tables, but there's a new class_name with the same set of
        column names (fuzzy match).
        """
        new_names = {t.class_name for t in tables}
        orig_names = {t.class_name for t in original_tables}

        # For tables that exist in both by name, check if table_name changed
        for orig in original_tables:
            if orig.class_name in new_names:
                new_t = self.tables_by_class[orig.class_name]
                # Same class name, possibly different table_name -- handled in leave_ClassDef
                continue

        # For tables that disappeared from original, see if there's a match
        # by column names in the new set -- but this is complex. For now,
        # rely on the simpler approach: if original class_name is NOT in new
        # tables and NOT in deleted_classes, it might be renamed. But we
        # need the user to pass renamed tables with the ORIGINAL class_name
        # in the tables list but a changed class_name field.
        # Actually the plan says: rename = change class_name on existing TableIR.
        # That means the TableIR passed still corresponds to the original
        # position in the list. We need to match by position or by
        # table_name or by column overlap.
        #
        # Simplest approach: match original tables to new tables by index
        # if they share at least some columns.
        pass

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        name = node.name.value
        self._original_class_names.add(name)

        # Check if this class is in our tables (either directly or via rename)
        if name in self.tables_by_class:
            self._current_class = name
            self._current_table = self.tables_by_class[name]
            self._current_original = self.original_by_class.get(name)
        elif name in self.deleted_classes:
            self._current_class = name
            self._current_table = None
            self._current_original = self.original_by_class.get(name)
        else:
            # Check if this is an original ORM class that was renamed
            # (its name is in original_by_class but not in tables_by_class)
            if name in self.original_by_class and name not in self.tables_by_class:
                # Find the renamed version by matching original tables
                self._current_class = name
                self._current_table = self._find_renamed_table(name)
                self._current_original = self.original_by_class[name]
            else:
                self._current_class = None
                self._current_table = None
                self._current_original = None
        return None

    def _find_renamed_table(self, original_name: str) -> Optional[TableIR]:
        """Find a table in tables_by_class that is a rename of original_name."""
        # Look for a table whose class_name is new (not in original) and
        # not already claimed
        orig = self.original_by_class[original_name]
        orig_col_names = {c.name for c in orig.columns}

        for t in self.tables_by_class.values():
            if t.class_name not in self.original_by_class:
                # This is a "new" class -- could be a rename
                new_col_names = {c.name for c in t.columns}
                # Check overlap
                if orig_col_names and new_col_names:
                    overlap = orig_col_names & new_col_names
                    if len(overlap) >= len(orig_col_names) * 0.5:
                        return t
        return None

    def leave_ClassDef(
        self,
        original_node: cst.ClassDef,
        updated_node: cst.ClassDef,
    ) -> Union[cst.ClassDef, cst.RemovalSentinel]:
        name = original_node.name.value

        if name in self.deleted_classes:
            self._current_class = None
            self._current_table = None
            self._current_original = None
            return cst.RemoveFromParent()

        table = self._current_table
        original = self._current_original

        self._current_class = None
        self._current_table = None
        self._current_original = None

        if table is None or original is None:
            return updated_node

        # --- Class-level changes ---
        result = updated_node

        # Rename class
        if table.class_name != name:
            result = result.with_changes(
                name=cst.Name(table.class_name)
            )

        # --- Body-level changes ---
        # Rebuild body: handle tablename change, column/relationship add/modify/delete
        new_body = self._rebuild_class_body(
            updated_node.body, table, original
        )
        if new_body is not None:
            result = result.with_changes(body=new_body)

        return result

    def _rebuild_class_body(
        self,
        body: cst.BaseSuite,
        table: TableIR,
        original: TableIR,
    ) -> Optional[cst.BaseSuite]:
        """Rebuild a class body to reflect IR changes."""
        if not isinstance(body, cst.IndentedBlock):
            return None

        new_col_names = {c.name for c in table.columns}
        orig_col_names = {c.name for c in original.columns}
        new_rel_names = {r.name for r in table.relationships}
        orig_rel_names = {r.name for r in original.relationships}

        # Build lookup maps
        new_cols = {c.name: c for c in table.columns}
        orig_cols = {c.name: c for c in original.columns}
        new_rels = {r.name: r for r in table.relationships}
        orig_rels = {r.name: r for r in original.relationships}

        new_stmts: list[cst.BaseStatement] = []
        changed = False

        for stmt in body.body:
            keep, replacement = self._process_class_stmt(
                stmt, table, original, new_cols, orig_cols,
                new_rels, orig_rels, new_col_names, orig_col_names,
                new_rel_names, orig_rel_names,
            )
            if not keep:
                changed = True
                continue
            if replacement is not None:
                new_stmts.append(replacement)
                if replacement is not stmt:
                    changed = True
            else:
                new_stmts.append(stmt)

        # Add new columns (in new but not in original)
        added_cols = new_col_names - orig_col_names
        for col_name in added_cols:
            col = new_cols[col_name]
            # Resolve Enum columns: generate Enum class and update type
            resolved_type, enum_class = _resolve_enum_column(col, table.class_name)
            if enum_class:
                enum_src = _build_enum_class(enum_class, col.enum_values)
                self._pending_enum_classes.append((table.class_name, enum_src))
                original_type = col.type
                col.type = resolved_type
                col_src = _build_column_source(col, indent="")
                col.type = original_type  # Restore
            else:
                col_src = _build_column_source(col, indent="")
            col_stmt = cst.parse_statement(col_src + "\n")
            new_stmts.append(col_stmt)
            changed = True

        # Add new relationships (in new but not in original)
        added_rels = new_rel_names - orig_rel_names
        for rel_name in added_rels:
            rel = new_rels[rel_name]
            rel_src = _build_relationship_source(rel, indent="")
            rel_stmt = cst.parse_statement(rel_src + "\n")
            new_stmts.append(rel_stmt)
            changed = True

        if not changed:
            return None

        return body.with_changes(body=new_stmts)

    def _process_class_stmt(
        self,
        stmt: cst.BaseStatement,
        table: TableIR,
        original: TableIR,
        new_cols: dict[str, ColumnIR],
        orig_cols: dict[str, ColumnIR],
        new_rels: dict[str, RelationshipIR],
        orig_rels: dict[str, RelationshipIR],
        new_col_names: set[str],
        orig_col_names: set[str],
        new_rel_names: set[str],
        orig_rel_names: set[str],
    ) -> tuple[bool, Optional[cst.BaseStatement]]:
        """Process a single statement in a class body.

        Returns (keep, replacement):
        - (False, None) -> remove the statement
        - (True, None) -> keep unchanged
        - (True, new_stmt) -> replace with new_stmt
        """
        if not isinstance(stmt, cst.SimpleStatementLine):
            return (True, None)

        for sub_stmt in stmt.body:
            # Handle __tablename__ changes
            if isinstance(sub_stmt, cst.Assign):
                for target in sub_stmt.targets:
                    if (
                        isinstance(target.target, cst.Name)
                        and target.target.value == "__tablename__"
                    ):
                        # Check if table_name changed
                        if table.table_name != original.table_name:
                            new_value = cst.SimpleString(f'"{table.table_name}"')
                            new_assign = sub_stmt.with_changes(
                                value=new_value
                            )
                            new_stmt = stmt.with_changes(body=[new_assign])
                            return (True, new_stmt)
                        return (True, None)

            # Handle columns and relationships (AnnAssign)
            if isinstance(sub_stmt, cst.AnnAssign):
                if not isinstance(sub_stmt.target, cst.Name):
                    return (True, None)

                attr_name = sub_stmt.target.value
                value = sub_stmt.value

                if value is None:
                    return (True, None)

                # Detect call type
                call_name = self._get_call_name(value)

                if call_name == "mapped_column":
                    # Column statement
                    if attr_name in orig_col_names and attr_name not in new_col_names:
                        # Deleted column
                        return (False, None)
                    if attr_name in new_cols and attr_name in orig_cols:
                        # Possibly modified column
                        new_col = new_cols[attr_name]
                        orig_col = orig_cols[attr_name]
                        if self._column_changed(new_col, orig_col):
                            col_src = _build_column_source(new_col, indent="")
                            replacement = cst.parse_statement(col_src + "\n")
                            return (True, replacement)
                    return (True, None)

                if call_name == "relationship":
                    # Relationship statement
                    if attr_name in orig_rel_names and attr_name not in new_rel_names:
                        # Deleted relationship
                        return (False, None)
                    if attr_name in new_rels and attr_name in orig_rels:
                        # Possibly modified relationship
                        new_rel = new_rels[attr_name]
                        orig_rel = orig_rels[attr_name]
                        if self._relationship_changed(new_rel, orig_rel):
                            rel_src = _build_relationship_source(new_rel, indent="")
                            replacement = cst.parse_statement(rel_src + "\n")
                            return (True, replacement)
                    return (True, None)

        return (True, None)

    def _column_changed(self, new: ColumnIR, orig: ColumnIR) -> bool:
        return (
            new.name != orig.name
            or new.type != orig.type
            or new.nullable != orig.nullable
            or new.primary_key != orig.primary_key
            or new.foreign_key != orig.foreign_key
            or new.unique != orig.unique
            or new.index != orig.index
            or new.default != orig.default
            or new.server_default != orig.server_default
            or new.enum_values != orig.enum_values
        )

    def _relationship_changed(self, new: RelationshipIR, orig: RelationshipIR) -> bool:
        return (
            new.name != orig.name
            or new.target != orig.target
            or new.back_populates != orig.back_populates
            or new.cascade != orig.cascade
            or new.lazy != orig.lazy
            or new.uselist != orig.uselist
            or new.order_by != orig.order_by
        )

    def _get_call_name(self, node: cst.BaseExpression) -> Optional[str]:
        if not isinstance(node, cst.Call):
            return None
        if isinstance(node.func, cst.Name):
            return node.func.value
        if isinstance(node.func, cst.Attribute):
            return node.func.attr.value
        return None

    def leave_Module(
        self,
        original_node: cst.Module,
        updated_node: cst.Module,
    ) -> cst.Module:
        """Append new classes that don't exist in original."""
        new_classes = []
        for class_name, table in self.tables_by_class.items():
            if (
                class_name not in self._original_class_names
                and class_name not in self.deleted_classes
            ):
                # Check this isn't a rename target (already handled)
                # A rename target has a class_name that doesn't appear in original
                # but the original class was already transformed
                is_rename_target = False
                for orig_name in self.original_by_class:
                    if orig_name not in self.tables_by_class:
                        # This original class was removed/renamed
                        renamed = self._find_renamed_table_static(orig_name, table)
                        if renamed:
                            is_rename_target = True
                            break
                if is_rename_target:
                    continue
                new_classes.append(table)

        if not new_classes and not self._pending_enum_classes:
            return updated_node

        new_body = list(updated_node.body)

        # Insert pending Enum class definitions (from Enum columns added to existing tables)
        # Insert them before the class that uses them
        for before_class, enum_src in self._pending_enum_classes:
            parsed = cst.parse_module(enum_src + "\n")
            for stmt in parsed.body:
                stmt_with_lines = stmt.with_changes(
                    leading_lines=[cst.EmptyLine(), cst.EmptyLine()]
                )
                # Find the index of the class that uses this Enum and insert before it
                insert_idx = len(new_body)
                for i, existing in enumerate(new_body):
                    if isinstance(existing, cst.ClassDef) and existing.name.value == before_class:
                        insert_idx = i
                        break
                new_body.insert(insert_idx, stmt_with_lines)

        for table in new_classes:
            class_src = _build_class_source(table)
            # Parse as a module to get the class statement
            parsed = cst.parse_module(class_src + "\n")
            for stmt in parsed.body:
                # Add 2 blank lines before the new class (PEP 8)
                stmt_with_lines = stmt.with_changes(
                    leading_lines=[cst.EmptyLine(), cst.EmptyLine()]
                )
                new_body.append(stmt_with_lines)

        return updated_node.with_changes(body=new_body)

    def _find_renamed_table_static(
        self, original_name: str, candidate: TableIR
    ) -> bool:
        """Check if candidate is a rename of original_name."""
        orig = self.original_by_class.get(original_name)
        if orig is None:
            return False
        orig_col_names = {c.name for c in orig.columns}
        candidate_col_names = {c.name for c in candidate.columns}
        if orig_col_names and candidate_col_names:
            overlap = orig_col_names & candidate_col_names
            if len(overlap) >= len(orig_col_names) * 0.5:
                return True
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def apply_changes(
    original_source: str,
    tables: list[TableIR],
    deleted_classes: set[str],
) -> str:
    """Apply IR changes to model.py source, preserving formatting.

    Args:
        original_source: Original Python source code.
        tables: Updated list of TableIR (may include new, modified, renamed).
        deleted_classes: Set of class names to remove.

    Returns:
        Modified Python source code.
    """
    original_tables = extract_model(original_source)
    tree = cst.parse_module(original_source)
    writer = ModelWriter(tables, deleted_classes, original_tables)
    modified = tree.visit(writer)
    return modified.code


def generate_preview(tables: list[TableIR], imports: str = "") -> str:
    """Generate a complete Python source string from IR (string-built, no CST).

    Args:
        tables: List of TableIR to render.
        imports: Optional imports header.

    Returns:
        Valid Python source code.
    """
    # Check if any table has Enum columns requiring import enum
    has_enum = any(
        col.type == "Enum" and col.enum_values
        for table in tables
        for col in table.columns
    )

    lines: list[str] = []

    if imports:
        lines.append(imports)
    else:
        # Default imports
        if has_enum:
            lines.append("import enum")
            lines.append("")
        lines.append("from sqlalchemy import Column, Enum, Integer, String, ForeignKey, Boolean, Text, DateTime, Float")
        lines.append("from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship")
        lines.append("")
        lines.append("")
        lines.append("class Base(DeclarativeBase):")
        lines.append("    pass")

    for table in tables:
        lines.append("")
        lines.append("")
        lines.append(_build_class_source(table))

    lines.append("")
    return "\n".join(lines)
