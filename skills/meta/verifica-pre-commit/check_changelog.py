#!/usr/bin/env python3
"""
Check 2: Changelog aggiornato.
Verifica che le modifiche siano tracciate nel changelog unificato (CHANGELOG.md).

Usage: python3 check_changelog.py file1 [file2 ...]
Exit: 0 = PASS, 1 = FAIL
"""

import sys
import os
import re
from typing import Optional

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Pattern per file che richiedono changelog struttura vs contenuti
STRUTTURA_PREFIXES = ("skills/", "docs/", "projects/_template/", ".tags/index.md")
CONTENUTI_PREFIXES = ("projects/", "patterns/", "knowledge/")
CONTENUTI_EXCLUDE = ("projects/_template/", "projects/_archivio/", "projects/INDEX.md")


def count_entries_in_section(filepath: str, version_header: str, section_header: str = None) -> int:
    """Conta le entry (righe che iniziano con '- ') in una sezione del changelog.

    version_header: es. "[Non rilasciato]" o "[v1.14]"
    Se section_header è specificato (es. "### Struttura"), conta solo dentro quella sotto-sezione.
    """
    if not os.path.isfile(filepath):
        return 0

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Trova la sezione richiesta
    pattern = r'^## ' + re.escape(version_header) + r'\s*(?:—\s*\S+)?\s*\n(.*?)(?=^## \[|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return 0

    section = match.group(1)

    if section_header:
        # Trova la sotto-sezione specifica
        sub_pattern = re.escape(section_header) + r'\s*\n(.*?)(?=^### |\Z)'
        sub_match = re.search(sub_pattern, section, re.MULTILINE | re.DOTALL)
        if not sub_match:
            return 0
        section = sub_match.group(1)

    return len(re.findall(r'^- ', section, re.MULTILINE))


def find_latest_version_header(filepath: str) -> Optional[str]:
    """Trova l'header della prima sezione versionata (es. '[v1.14]')."""
    if not os.path.isfile(filepath):
        return None

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    match = re.search(r'^## (\[v\d+\.\d+\])', content, re.MULTILINE)
    return match.group(1) if match else None


def classify_file(filepath: str) -> Optional[str]:
    """Classifica un file come 'struttura', 'contenuti', o None (meta/ignorabile)."""
    rel = filepath.removeprefix(KB_ROOT + "/").removeprefix("./")

    # Escludi file che non richiedono entry
    if rel.startswith(("CHANGELOG", "IDEAS.md", ".git")):
        return None

    # Struttura
    if any(rel.startswith(p) for p in STRUTTURA_PREFIXES):
        return "struttura"

    # Contenuti (escludi template e archivio)
    if any(rel.startswith(p) for p in CONTENUTI_PREFIXES):
        if not any(rel.startswith(e) for e in CONTENUTI_EXCLUDE):
            return "contenuti"

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: check_changelog.py file1 [file2 ...]")
        sys.exit(2)

    changelog_path = os.path.join(KB_ROOT, "CHANGELOG.md")

    # Controlla prima [Non rilasciato], poi la versione più recente
    struttura_entries = count_entries_in_section(changelog_path, "[Non rilasciato]", "### Struttura")
    contenuti_entries = count_entries_in_section(changelog_path, "[Non rilasciato]", "### Contenuti")

    # Se [Non rilasciato] è vuoto, controlla la versione più recente
    # (le entry possono essere scritte direttamente nella sezione versionata)
    if struttura_entries == 0 or contenuti_entries == 0:
        latest = find_latest_version_header(changelog_path)
        if latest:
            if struttura_entries == 0:
                struttura_entries = count_entries_in_section(changelog_path, latest, "### Struttura")
            if contenuti_entries == 0:
                contenuti_entries = count_entries_in_section(changelog_path, latest, "### Contenuti")

    has_struttura = False
    has_contenuti = False

    for filepath in sys.argv[1:]:
        cat = classify_file(filepath)
        if cat == "struttura":
            has_struttura = True
        elif cat == "contenuti":
            has_contenuti = True

    issues = []

    if has_struttura and struttura_entries == 0:
        issues.append("Modifiche a struttura ma CHANGELOG.md [Non rilasciato] → ### Struttura è vuoto")

    if has_contenuti and contenuti_entries == 0:
        issues.append("Modifiche a contenuti ma CHANGELOG.md [Non rilasciato] → ### Contenuti è vuoto")

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
