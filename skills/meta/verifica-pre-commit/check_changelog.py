#!/usr/bin/env python3
"""
Check 2: Changelog aggiornato.
Verifica che le modifiche siano tracciate nel changelog corretto.

Usage: python3 check_changelog.py file1 [file2 ...]
Exit: 0 = PASS, 1 = FAIL
"""

import sys
import os
import re
from typing import Optional

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Pattern per file che richiedono changelog framework vs contenuti
FRAMEWORK_PREFIXES = ("skills/", "docs/", "projects/_template/", ".tags/index.md")
CONTENUTI_PREFIXES = ("projects/", "patterns/", "knowledge/")
CONTENUTI_EXCLUDE = ("projects/_template/", "projects/_archivio/", "projects/INDEX.md")


def count_entries_in_non_rilasciato(filepath: str) -> int:
    """Conta le entry (righe che iniziano con '- ') nella sezione [Non rilasciato]."""
    if not os.path.isfile(filepath):
        return 0

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Trova la sezione [Non rilasciato]
    match = re.search(r'^## \[Non rilasciato\]\s*\n(.*?)(?=^## \[|\Z)', content, re.MULTILINE | re.DOTALL)
    if not match:
        return 0

    section = match.group(1)
    return len(re.findall(r'^- ', section, re.MULTILINE))


def classify_file(filepath: str) -> Optional[str]:
    """Classifica un file come 'framework', 'contenuti', o None (meta/ignorabile)."""
    rel = filepath.removeprefix(KB_ROOT + "/").removeprefix("./")

    # Escludi file che non richiedono entry
    if rel.startswith(("CHANGELOG", "IDEAS.md", ".git")):
        return None

    # Framework
    if any(rel.startswith(p) for p in FRAMEWORK_PREFIXES):
        return "framework"

    # Contenuti (escludi template e archivio)
    if any(rel.startswith(p) for p in CONTENUTI_PREFIXES):
        if not any(rel.startswith(e) for e in CONTENUTI_EXCLUDE):
            return "contenuti"

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: check_changelog.py file1 [file2 ...]")
        sys.exit(2)

    fw_path = os.path.join(KB_ROOT, "CHANGELOG-framework.md")
    ct_path = os.path.join(KB_ROOT, "CHANGELOG-contenuti.md")

    fw_entries = count_entries_in_non_rilasciato(fw_path)
    ct_entries = count_entries_in_non_rilasciato(ct_path)

    has_framework = False
    has_contenuti = False

    for filepath in sys.argv[1:]:
        cat = classify_file(filepath)
        if cat == "framework":
            has_framework = True
        elif cat == "contenuti":
            has_contenuti = True

    issues = []

    if has_framework and fw_entries == 0:
        issues.append("Modifiche a framework ma CHANGELOG-framework.md [Non rilasciato] è vuoto")

    if has_contenuti and ct_entries == 0:
        issues.append("Modifiche a contenuti ma CHANGELOG-contenuti.md [Non rilasciato] è vuoto")

    if not issues:
        print("Check 2 — Changelog: ✓ PASS")
        sys.exit(0)
    else:
        print(f"Check 2 — Changelog: ✗ FAIL ({len(issues)} issue)")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
