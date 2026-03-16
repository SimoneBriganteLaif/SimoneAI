#!/usr/bin/env python3
"""
Check 4: Tag frontmatter.
- Verifica che i file .md abbiano tag validi e registrati in .tags/index.md
- Verifica consistenza tag all'interno di ogni progetto

Usage: python3 check_tags.py file1.md [file2.md ...]
Exit: 0 = PASS, 1 = FAIL
"""

import sys
import os
import re
import glob as glob_module
from typing import List, Optional
from collections import defaultdict

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TAGS_INDEX = os.path.join(KB_ROOT, ".tags", "index.md")

# File da escludere dal check (basename)
SYSTEM_FILES = {
    "CLAUDE.md", "System.md", "IDEAS.md", "README.md", "INDEX.md", "SKILL.md", ".gitkeep",
}
SYSTEM_PREFIXES = ("CHANGELOG", "_template")

# Directory i cui file non richiedono tag
SYSTEM_DIRS = ("docs/", ".tags/", "core/", ".claude/", "issues/", "CLI/")

# Pattern per i tag nel frontmatter YAML
TAG_RE = re.compile(r'"(#[a-z]+:[a-zA-Z0-9_-]+)"')


def is_system_file(filepath, basename):
    if basename in SYSTEM_FILES:
        return True
    if any(basename.startswith(p) for p in SYSTEM_PREFIXES):
        return True
    rel = os.path.relpath(filepath, KB_ROOT) if os.path.isabs(filepath) else filepath
    return any(rel.startswith(d) for d in SYSTEM_DIRS)


def load_known_tags(index_path):
    """Legge tutti i tag dichiarati in .tags/index.md."""
    if not os.path.isfile(index_path):
        return set()
    with open(index_path, encoding="utf-8") as f:
        content = f.read()
    return set(re.findall(r'`(#[a-z]+:[a-zA-Z0-9_-]+)`', content))


def extract_frontmatter_tags(filepath):
    # type: (str) -> Optional[List[str]]
    """Estrae i tag dal frontmatter YAML. None se no frontmatter, [] se no tag."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        return None

    frontmatter_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter_lines.append(line)

    frontmatter = "\n".join(frontmatter_lines)
    return TAG_RE.findall(frontmatter)


def get_project_name(filepath):
    """Se il file è dentro projects/[nome]/, ritorna il nome progetto. Altrimenti None."""
    rel = os.path.relpath(filepath, KB_ROOT) if os.path.isabs(filepath) else filepath
    parts = rel.split(os.sep)
    if len(parts) >= 2 and parts[0] == "projects" and not parts[1].startswith("_"):
        return parts[1]
    return None


def check_project_consistency(issues):
    """
    Per ogni progetto in projects/, verifica che tutti i file .md (non di sistema)
    usino gli stessi tag #progetto: e #industria:.
    """
    projects_dir = os.path.join(KB_ROOT, "projects")
    if not os.path.isdir(projects_dir):
        return

    for proj_name in os.listdir(projects_dir):
        proj_dir = os.path.join(projects_dir, proj_name)
        if not os.path.isdir(proj_dir) or proj_name.startswith("_"):
            continue

        # Raccogli tag da tutti i .md del progetto (ricorsivo)
        project_tags = defaultdict(set)  # {category: set of values}
        files_with_tags = {}  # {filepath: tags}

        for md_file in glob_module.glob(os.path.join(proj_dir, "**", "*.md"), recursive=True):
            # Salta repo/ e file di sistema
            rel = os.path.relpath(md_file, proj_dir)
            if rel.startswith("repo"):
                continue
            basename = os.path.basename(md_file)
            if basename in SYSTEM_FILES:
                continue

            tags = extract_frontmatter_tags(md_file)
            if tags is None or not tags:
                continue

            files_with_tags[md_file] = tags
            for tag in tags:
                # tag è tipo "#progetto:jubatus"
                if ":" in tag:
                    cat = tag.split(":")[0]  # "#progetto"
                    project_tags[cat].add(tag)

        # Verifica consistenza: #progetto: e #industria: devono essere uguali in tutti i file
        for category in ["#progetto", "#industria"]:
            values = project_tags.get(category, set())
            if len(values) > 1:
                values_str = ", ".join(sorted(values))
                issues.append(
                    f"projects/{proj_name}/: tag {category} inconsistente — "
                    f"valori diversi trovati: {values_str}"
                )

        # Verifica che tutti i file del progetto abbiano #progetto:[nome]
        expected_progetto = "#progetto:" + proj_name
        for md_file, tags in files_with_tags.items():
            if expected_progetto not in tags:
                rel = os.path.relpath(md_file, KB_ROOT)
                issues.append(f"{rel}: manca tag {expected_progetto}")


def main():
    if len(sys.argv) < 2:
        print("Usage: check_tags.py file1.md [file2.md ...]")
        sys.exit(2)

    known_tags = load_known_tags(TAGS_INDEX)
    issues = []

    # --- Check base: tag presenti e registrati ---
    for filepath in sys.argv[1:]:
        abs_path = filepath if os.path.isabs(filepath) else os.path.join(KB_ROOT, filepath)

        if not os.path.isfile(abs_path) or not abs_path.endswith(".md"):
            continue

        basename = os.path.basename(abs_path)
        if is_system_file(abs_path, basename):
            continue

        rel = os.path.relpath(abs_path, KB_ROOT)
        tags = extract_frontmatter_tags(abs_path)

        if tags is None:
            issues.append(f"{rel}: nessun frontmatter")
            continue

        if not tags:
            issues.append(f"{rel}: nessun tag nel frontmatter")
            continue

        for tag in tags:
            if tag not in known_tags:
                issues.append(f"{rel}: tag {tag} non registrato in .tags/index.md")

    # --- Check consistenza tag per progetto ---
    # Verifica tutti i progetti (non solo i file modificati)
    check_project_consistency(issues)

    if not issues:
        print("Check 4 — Tag: ✓ PASS")
        sys.exit(0)
    else:
        print(f"Check 4 — Tag: ✗ FAIL ({len(issues)} issue)")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
