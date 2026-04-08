"""B. Data model: tabelle custom, materialized views, bozza ER."""

import re
from pathlib import Path


TABLE_PATTERN = re.compile(r'__tablename__\s*=\s*["\'](\w+)["\']')
FK_PATTERN = re.compile(r'ForeignKey\(["\']([^"\']+)["\']')
RELATIONSHIP_PATTERN = re.compile(r'relationship\(["\'](\w+)["\']')
CLASS_PATTERN = re.compile(r'^class\s+(\w+)\(', re.MULTILINE)


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)

    baseline_tables = set()
    for schema_tables in baseline.get("tables", {}).values():
        baseline_tables.update(schema_tables)

    all_tables = []
    materialized_views = []

    # Cerca in tutti i file .py del backend
    backend_src = repo / "backend" / "src"
    if not backend_src.exists():
        return {"custom_tables": [], "materialized_views": [], "mermaid_er": ""}

    for py_file in backend_src.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        rel_path = str(py_file.relative_to(repo))

        # Controlla se è in template/ — salta per tabelle custom
        is_template = "/template/" in rel_path

        # Trova tabelle
        for match in TABLE_PATTERN.finditer(content):
            table_name = match.group(1)
            # Cerca la classe che contiene questo __tablename__
            class_name = _find_class_for_table(content, match.start())

            # Trova FK per questa tabella
            # Cerca nel blocco della classe
            class_body = _get_class_body(content, match.start())
            fk_targets = FK_PATTERN.findall(class_body)
            relationships = RELATIONSHIP_PATTERN.findall(class_body)

            entry = {
                "table": table_name,
                "class": class_name,
                "file": rel_path,
                "is_template": is_template,
                "foreign_keys": fk_targets,
                "relationships": relationships,
            }

            if table_name not in baseline_tables and not is_template:
                all_tables.append(entry)

        # Materialized views
        if "MaterializedView" in content or "__materialized_view__" in content:
            for cls_match in CLASS_PATTERN.finditer(content):
                cls_name = cls_match.group(1)
                cls_body = _get_class_body(content, cls_match.start())
                tbl_match = TABLE_PATTERN.search(cls_body)
                if tbl_match and "MaterializedView" in cls_body[:200]:
                    materialized_views.append({
                        "name": tbl_match.group(1),
                        "class": cls_name,
                        "file": rel_path,
                    })

    # Genera Mermaid ER
    mermaid = _generate_mermaid_er(all_tables)

    return {
        "custom_tables": all_tables,
        "custom_table_count": len(all_tables),
        "materialized_views": materialized_views,
        "materialized_view_count": len(materialized_views),
        "mermaid_er": mermaid,
    }


def _find_class_for_table(content: str, pos: int) -> str:
    """Trova il nome della classe che contiene la posizione data."""
    # Cerca all'indietro la definizione di classe più vicina
    before = content[:pos]
    matches = list(CLASS_PATTERN.finditer(before))
    return matches[-1].group(1) if matches else "Unknown"


def _get_class_body(content: str, class_start: int) -> str:
    """Estrae il body approssimativo di una classe."""
    # Prende fino alla prossima definizione di classe o fine file
    rest = content[class_start:]
    next_class = CLASS_PATTERN.search(rest[1:])  # skip la classe corrente
    if next_class:
        return rest[:next_class.start() + 1]
    return rest


def _generate_mermaid_er(tables: list) -> str:
    """Genera diagramma Mermaid ER dalle tabelle custom."""
    if not tables:
        return ""

    lines = ["erDiagram"]
    for t in tables:
        entity = t["table"].upper()
        lines.append(f"    {entity} {{")
        lines.append(f"        int id PK")
        for fk in t["foreign_keys"]:
            # fk è tipo "tabella.colonna" o "schema.tabella.colonna"
            parts = fk.split(".")
            fk_table = parts[-2] if len(parts) >= 2 else parts[0]
            lines.append(f"        int id_{fk_table} FK")
        lines.append("    }")

    # Relazioni basate su FK
    for t in tables:
        for fk in t["foreign_keys"]:
            parts = fk.split(".")
            fk_table = parts[-2] if len(parts) >= 2 else parts[0]
            lines.append(f"    {fk_table.upper()} ||--o{{ {t['table'].upper()} : \"\"")

    return "\n".join(lines)
