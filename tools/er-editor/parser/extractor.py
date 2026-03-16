"""SQLAlchemy 2.0 model extractor using libcst.

Walks a model.py CST and produces a list of TableIR dataclasses representing
all ORM tables found. ORM detection is based on __tablename__ presence,
not base class name.
"""
from __future__ import annotations

from typing import Optional, Sequence

import libcst as cst

from .ir import ColumnIR, RelationshipIR, TableIR


class ModelExtractor(cst.CSTVisitor):
    """CSTVisitor that extracts SQLAlchemy ORM tables into TableIR."""

    def __init__(self) -> None:
        self.tables: list[TableIR] = []
        self._current_class: Optional[TableIR] = None
        self._found_tablename: bool = False
        self._class_depth: int = 0

    # ------------------------------------------------------------------
    # Class enter / leave
    # ------------------------------------------------------------------

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self._class_depth += 1
        if self._class_depth == 1:
            # Start tracking a potential ORM class
            self._current_class = TableIR(
                class_name=node.name.value, table_name=""
            )
            self._found_tablename = False
        return None  # visit children

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        if self._class_depth == 1:
            if self._current_class and self._found_tablename:
                self.tables.append(self._current_class)
            self._current_class = None
            self._found_tablename = False
        self._class_depth -= 1

    # ------------------------------------------------------------------
    # Statement visitors
    # ------------------------------------------------------------------

    def visit_SimpleStatementLine(
        self, node: cst.SimpleStatementLine
    ) -> Optional[bool]:
        if self._class_depth != 1 or self._current_class is None:
            return None

        for stmt in node.body:
            # __tablename__ = "..."
            if isinstance(stmt, cst.Assign):
                self._handle_assign(stmt)
            # Annotated: Mapped[...] = mapped_column(...) / relationship(...)
            elif isinstance(stmt, cst.AnnAssign):
                self._handle_ann_assign(stmt)

        return False  # don't descend further

    # ------------------------------------------------------------------
    # Assign handlers
    # ------------------------------------------------------------------

    def _handle_assign(self, node: cst.Assign) -> None:
        """Handle plain Assign: __tablename__, __table_args__."""
        for target in node.targets:
            target_node = target.target
            if not isinstance(target_node, cst.Name):
                continue
            name = target_node.value

            if name == "__tablename__":
                val = self._extract_string(node.value)
                if val is not None:
                    assert self._current_class is not None
                    self._current_class.table_name = val
                    self._found_tablename = True

            elif name == "__table_args__":
                self._parse_table_args(node.value)

    def _handle_ann_assign(self, node: cst.AnnAssign) -> None:
        """Handle AnnAssign: Mapped[...] = mapped_column(...) / relationship(...)."""
        if not isinstance(node.target, cst.Name):
            return
        attr_name = node.target.value
        value = node.value
        if value is None:
            return

        # Detect what kind of call it is
        call_name = self._get_call_name(value)

        if call_name == "mapped_column":
            self._extract_column(attr_name, node.annotation, value)
        elif call_name == "relationship":
            self._extract_relationship(attr_name, node.annotation, value)

    # ------------------------------------------------------------------
    # Column extraction
    # ------------------------------------------------------------------

    def _extract_column(
        self,
        name: str,
        annotation: Optional[cst.Annotation],
        value: cst.BaseExpression,
    ) -> None:
        assert self._current_class is not None
        assert isinstance(value, cst.Call)

        # Determine nullable from annotation (Mapped[X | None] -> True)
        annotation_nullable = False
        if annotation:
            annotation_nullable = self._annotation_is_nullable(
                annotation.annotation
            )

        # Extract type from first positional arg of mapped_column()
        col_type = self._extract_column_type(value)
        if not col_type and annotation:
            col_type = self._extract_type_from_mapped(annotation.annotation)

        # Extract keyword args
        pk = self._get_keyword_bool(value, "primary_key") or False
        nullable_explicit = self._get_keyword_bool(value, "nullable")
        unique = self._get_keyword_bool(value, "unique") or False
        index = self._get_keyword_bool(value, "index") or False
        default = self._get_keyword_value_str(value, "default")
        server_default = self._extract_server_default(value)
        foreign_key = self._extract_foreign_key(value)

        # Nullable logic:
        # - PK -> always False
        # - explicit nullable= in mapped_column() overrides annotation
        # - otherwise use annotation (Mapped[X | None] -> True, Mapped[X] -> False)
        if pk:
            nullable = False
        elif nullable_explicit is not None:
            nullable = nullable_explicit
        else:
            nullable = annotation_nullable

        col = ColumnIR(
            name=name,
            type=col_type or "Unknown",
            nullable=nullable,
            primary_key=pk,
            foreign_key=foreign_key,
            unique=unique,
            index=index,
            default=default,
            server_default=server_default,
        )
        self._current_class.columns.append(col)

    def _extract_column_type(self, call: cst.Call) -> Optional[str]:
        """Extract type from first positional arg of mapped_column().

        E.g. mapped_column(Integer, ...) -> "Integer"
             mapped_column(String(255), ...) -> "String(255)"
             mapped_column(DateTime(timezone=True), ...) -> "DateTime(timezone=True)"
        """
        for arg in call.args:
            if arg.keyword is not None:
                continue
            # First positional arg
            return self._reconstruct_type(arg.value)
        return None

    def _reconstruct_type(self, node: cst.BaseExpression) -> str:
        """Turn a CST expression into a display string like 'String(50)' or 'Integer'."""
        if isinstance(node, cst.Name):
            return node.value
        elif isinstance(node, cst.Call):
            func_name = self._reconstruct_type(node.func)
            args_parts = []
            for arg in node.args:
                if arg.keyword is not None:
                    kw_val = self._node_to_source(arg.value)
                    args_parts.append(f"{arg.keyword.value}={kw_val}")
                else:
                    args_parts.append(self._node_to_source(arg.value))
            return f"{func_name}({', '.join(args_parts)})"
        elif isinstance(node, cst.Attribute):
            return f"{self._reconstruct_type(node.value)}.{node.attr.value}"
        else:
            return self._node_to_source(node)

    def _extract_foreign_key(self, call: cst.Call) -> Optional[str]:
        """Look for ForeignKey('...') among positional args of mapped_column()."""
        for arg in call.args:
            if arg.keyword is not None:
                continue
            if isinstance(arg.value, cst.Call):
                fn = self._get_call_name(arg.value)
                if fn == "ForeignKey":
                    # First positional arg of ForeignKey() is the FK string
                    for fk_arg in arg.value.args:
                        if fk_arg.keyword is None:
                            return self._extract_string(fk_arg.value)
        return None

    def _extract_server_default(self, call: cst.Call) -> Optional[str]:
        """Extract server_default value. Handles text('now()') -> 'now()'."""
        val_node = self._get_keyword_node(call, "server_default")
        if val_node is None:
            return None
        # Check if it's text("...")
        if isinstance(val_node, cst.Call):
            fn = self._get_call_name(val_node)
            if fn == "text":
                for arg in val_node.args:
                    if arg.keyword is None:
                        return self._extract_string(arg.value)
        return self._node_to_source(val_node)

    # ------------------------------------------------------------------
    # Relationship extraction
    # ------------------------------------------------------------------

    def _extract_relationship(
        self,
        name: str,
        annotation: Optional[cst.Annotation],
        value: cst.BaseExpression,
    ) -> None:
        assert self._current_class is not None
        assert isinstance(value, cst.Call)

        # Target: first positional string arg, or from annotation
        target = None
        for arg in value.args:
            if arg.keyword is None:
                target = self._extract_string(arg.value)
                break

        if target is None and annotation:
            target = self._extract_relationship_target(annotation.annotation)

        # uselist: from annotation (list[X] -> True, X -> False), explicit overrides
        uselist_from_annotation = self._annotation_is_list(annotation.annotation) if annotation else True
        uselist_explicit = self._get_keyword_bool(value, "uselist")
        uselist = uselist_explicit if uselist_explicit is not None else uselist_from_annotation

        back_populates = self._get_keyword_str(value, "back_populates")
        cascade = self._get_keyword_str(value, "cascade")
        lazy = self._get_keyword_str(value, "lazy")
        order_by = self._get_keyword_str(value, "order_by")

        rel = RelationshipIR(
            name=name,
            target=target or "Unknown",
            back_populates=back_populates,
            cascade=cascade,
            lazy=lazy,
            uselist=uselist,
            order_by=order_by,
        )
        self._current_class.relationships.append(rel)

    def _extract_relationship_target(
        self, annotation: cst.BaseExpression
    ) -> Optional[str]:
        """Extract target class from Mapped['Target'] or Mapped[list['Target']]."""
        # Get the inner type from Mapped[...]
        inner = self._get_subscript_inner(annotation)
        if inner is None:
            return None

        # list["Target"] -> extract "Target"
        if isinstance(inner, cst.Subscript) and self._get_subscript_name(inner) == "list":
            inner = self._get_subscript_inner(inner)
            if inner is None:
                return None

        # "Target" (string annotation)
        if isinstance(inner, (cst.SimpleString, cst.ConcatenatedString, cst.FormattedString)):
            return self._extract_string(inner)
        if isinstance(inner, cst.Name):
            return inner.value
        return None

    # ------------------------------------------------------------------
    # __table_args__ parsing
    # ------------------------------------------------------------------

    def _parse_table_args(self, value: cst.BaseExpression) -> None:
        """Parse __table_args__ for schema key."""
        assert self._current_class is not None

        if isinstance(value, cst.Dict):
            self._extract_schema_from_dict(value)
        elif isinstance(value, cst.Tuple):
            # Tuple: last element may be a dict with schema
            for el in value.elements:
                if isinstance(el, cst.Element) and isinstance(el.value, cst.Dict):
                    self._extract_schema_from_dict(el.value)

    def _extract_schema_from_dict(self, dict_node: cst.Dict) -> None:
        assert self._current_class is not None
        for el in dict_node.elements:
            if isinstance(el, cst.DictElement):
                key = self._extract_string(el.key)
                if key == "schema":
                    val = self._extract_string(el.value)
                    if val:
                        self._current_class.schema = val

    # ------------------------------------------------------------------
    # Annotation helpers
    # ------------------------------------------------------------------

    def _annotation_is_nullable(self, annotation: cst.BaseExpression) -> bool:
        """Check if annotation is Mapped[X | None] -> True."""
        inner = self._get_subscript_inner(annotation)
        if inner is None:
            return False
        return self._contains_none_union(inner)

    def _contains_none_union(self, node: cst.BaseExpression) -> bool:
        """Check if node is X | None (BinaryOperation with | and None)."""
        if isinstance(node, cst.BinaryOperation):
            if isinstance(node.operator, cst.BitOr):
                if self._is_none(node.left) or self._is_none(node.right):
                    return True
                return self._contains_none_union(
                    node.left
                ) or self._contains_none_union(node.right)
        return False

    def _is_none(self, node: cst.BaseExpression) -> bool:
        return isinstance(node, cst.Name) and node.value == "None"

    def _annotation_is_list(self, annotation: cst.BaseExpression) -> bool:
        """Check if annotation is Mapped[list[...]]."""
        inner = self._get_subscript_inner(annotation)
        if inner is None:
            return False
        if isinstance(inner, cst.Subscript):
            return self._get_subscript_name(inner) == "list"
        if isinstance(inner, cst.Name):
            return inner.value == "list"
        return False

    def _get_subscript_inner(
        self, node: cst.BaseExpression
    ) -> Optional[cst.BaseExpression]:
        """Get inner type from Subscript: Mapped[X] -> X."""
        if not isinstance(node, cst.Subscript):
            return None
        if len(node.slice) == 1:
            sl = node.slice[0]
            if isinstance(sl, cst.SubscriptElement):
                if isinstance(sl.slice, cst.Index):
                    return sl.slice.value
        return None

    def _get_subscript_name(self, node: cst.Subscript) -> Optional[str]:
        if isinstance(node.value, cst.Name):
            return node.value.value
        return None

    def _extract_type_from_mapped(
        self, annotation: cst.BaseExpression
    ) -> Optional[str]:
        """Fallback: extract type string from Mapped[X] annotation."""
        inner = self._get_subscript_inner(annotation)
        if inner is None:
            return None
        if isinstance(inner, cst.BinaryOperation):
            # X | None -> return X part
            if self._is_none(inner.right):
                return self._node_to_source(inner.left)
            if self._is_none(inner.left):
                return self._node_to_source(inner.right)
        return self._node_to_source(inner)

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    def _get_call_name(self, node: cst.BaseExpression) -> Optional[str]:
        """Get function name from a Call node."""
        if not isinstance(node, cst.Call):
            return None
        if isinstance(node.func, cst.Name):
            return node.func.value
        if isinstance(node.func, cst.Attribute):
            return node.func.attr.value
        return None

    def _get_keyword_node(
        self, call: cst.Call, keyword: str
    ) -> Optional[cst.BaseExpression]:
        """Find keyword arg value node in a Call."""
        for arg in call.args:
            if arg.keyword and arg.keyword.value == keyword:
                return arg.value
        return None

    def _get_keyword_bool(
        self, call: cst.Call, keyword: str
    ) -> Optional[bool]:
        """Extract boolean from keyword arg."""
        node = self._get_keyword_node(call, keyword)
        if node is None:
            return None
        if isinstance(node, cst.Name):
            if node.value == "True":
                return True
            if node.value == "False":
                return False
        return None

    def _get_keyword_str(
        self, call: cst.Call, keyword: str
    ) -> Optional[str]:
        """Extract string from keyword arg."""
        node = self._get_keyword_node(call, keyword)
        if node is None:
            return None
        return self._extract_string(node)

    def _get_keyword_value_str(
        self, call: cst.Call, keyword: str
    ) -> Optional[str]:
        """Extract keyword arg value as display string (for default=True -> 'True')."""
        node = self._get_keyword_node(call, keyword)
        if node is None:
            return None
        if isinstance(node, cst.Name):
            return node.value  # True, False, None, etc.
        if isinstance(node, cst.Integer):
            return node.value
        if isinstance(node, cst.Float):
            return node.value
        return self._extract_string(node) or self._node_to_source(node)

    def _extract_string(
        self, node: cst.BaseExpression
    ) -> Optional[str]:
        """Extract raw string value from a string literal node."""
        if isinstance(node, cst.SimpleString):
            # Remove quotes: "value" or 'value'
            raw = node.value
            # Handle triple quotes
            for q in ('"""', "'''", '"', "'"):
                if raw.startswith(q) and raw.endswith(q):
                    return raw[len(q) : -len(q)]
            return raw
        if isinstance(node, cst.ConcatenatedString):
            # Try to get first part
            parts = []
            for part in node.left, node.right:
                s = self._extract_string(part)
                if s:
                    parts.append(s)
            return "".join(parts) if parts else None
        return None

    def _node_to_source(self, node: cst.BaseExpression) -> str:
        """Convert a CST node back to source string."""
        module = cst.Module(body=[cst.SimpleStatementLine(body=[cst.Expr(value=node)])])
        code = module.code.strip()
        return code


def extract_model(source: str) -> list[TableIR]:
    """Parse SQLAlchemy model source and return list of TableIR.

    Args:
        source: Python source code string of a model.py file.

    Returns:
        List of TableIR dataclasses for each ORM table found.
    """
    tree = cst.parse_module(source)
    extractor = ModelExtractor()
    wrapper = cst.metadata.MetadataWrapper(tree)
    wrapper.visit(extractor)
    return extractor.tables
