#!/usr/bin/env python3
"""
Contesto proattivo — match.py

Dato un nome progetto, trova i file rilevanti nella KB in base ai tag del progetto.
Cerca match in: patterns/, knowledge/problemi-tecnici/, knowledge/industrie/

Usage: python3 match.py <nome-progetto>
Exit: 0 = match trovati, 1 = nessun match, 2 = progetto non trovato
"""

from __future__ import annotations

import sys
import os
import re
import glob

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def extract_tags_from_file(filepath: str) -> set[str]:
    """Estrae tag dal frontmatter YAML di un file markdown."""
    tags = set()
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return tags

    # Trova frontmatter YAML (tra ---)
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return tags

    frontmatter = match.group(1)

    # Estrai tutti i tag (formato: - "#tag:valore" o - #tag:valore)
    for tag_match in re.finditer(r'["\']?(#\w+:\S+?)["\']?\s*$', frontmatter, re.MULTILINE):
        tags.add(tag_match.group(1).strip('"\''))

    return tags


def extract_stack_tags(tags: set[str]) -> set[str]:
    """Filtra solo i tag #stack: e #industria: da un set di tag."""
    return {t for t in tags if t.startswith("#stack:") or t.startswith("#industria:")}


def find_project_readme(project_name: str) -> str | None:
    """Trova il README.md del progetto."""
    readme = os.path.join(KB_ROOT, "projects", project_name, "README.md")
    return readme if os.path.isfile(readme) else None


def scan_directory_for_matches(directory: str, project_tags: set[str]) -> list[tuple[str, set[str]]]:
    """Scansiona una directory per file con tag matchanti."""
    matches = []
    pattern = os.path.join(KB_ROOT, directory, "**", "*.md")

    for filepath in glob.glob(pattern, recursive=True):
        if os.path.basename(filepath).startswith("_"):
            continue  # Salta template

        file_tags = extract_tags_from_file(filepath)
        matching = project_tags & file_tags

        if matching:
            rel_path = os.path.relpath(filepath, KB_ROOT)
            matches.append((rel_path, matching))

    return matches


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 match.py <nome-progetto>")
        sys.exit(2)

    project_name = sys.argv[1]
    readme = find_project_readme(project_name)

    if not readme:
        print(f"Progetto '{project_name}' non trovato in projects/")
        sys.exit(2)

    # Estrai tag del progetto
    project_tags = extract_tags_from_file(readme)
    search_tags = extract_stack_tags(project_tags)

    if not search_tags:
        print(f"Nessun tag #stack: o #industria: trovato in projects/{project_name}/README.md")
        sys.exit(1)

    print(f"Progetto: {project_name}")
    print(f"Tag di ricerca: {', '.join(sorted(search_tags))}")
    print()

    # Cerca in patterns/, knowledge/problemi-tecnici/, knowledge/industrie/
    all_matches = []

    for directory in ["patterns", "knowledge/problemi-tecnici", "knowledge/industrie"]:
        matches = scan_directory_for_matches(directory, search_tags)
        if matches:
            all_matches.extend(matches)

    if not all_matches:
        print("Nessun file rilevante trovato.")
        sys.exit(1)

    # Output ordinato per directory
    print("File rilevanti da consultare:")
    print()

    for rel_path, matching_tags in sorted(all_matches):
        tags_str = ", ".join(sorted(matching_tags))
        print(f"  {rel_path}")
        print(f"    match: {tags_str}")

    print()
    print(f"Totale: {len(all_matches)} file")
    sys.exit(0)


if __name__ == "__main__":
    main()
