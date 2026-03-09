#!/usr/bin/env python3
"""
Check 1: Coerenza referenze cross-file.
Verifica che i link markdown nei file puntino a file/directory esistenti.

Usage: python3 check_refs.py file1.md [file2.md ...]
Exit: 0 = PASS, 1 = FAIL
"""

import sys
import re
import os
from typing import List

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Pattern per link markdown: [testo](target)
LINK_RE = re.compile(r'\]\(([^)]+)\)')
# URL da ignorare
SKIP_RE = re.compile(r'^(https?://|#|mailto:)')


def check_file(filepath: str) -> List[str]:
    """Controlla i link markdown in un file. Ritorna lista di issue."""
    issues = []
    abs_path = filepath if os.path.isabs(filepath) else os.path.join(KB_ROOT, filepath)

    if not os.path.isfile(abs_path) or not abs_path.endswith(".md"):
        return []

    file_dir = os.path.dirname(abs_path)

    with open(abs_path, encoding="utf-8") as f:
        in_code_block = False
        for line_num, line in enumerate(f, 1):
            # Ignora blocchi di codice (```)
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Rimuovi inline code (`...`) prima di cercare i link
            clean_line = re.sub(r'`[^`]+`', '', line)

            for match in LINK_RE.finditer(clean_line):
                target = match.group(1)

                # Ignora URL esterni e ancore
                if SKIP_RE.match(target):
                    continue

                # Rimuovi eventuale ancora (#sezione)
                target = target.split("#")[0]
                if not target:
                    continue

                # Risolvi percorso relativo
                resolved = os.path.normpath(os.path.join(file_dir, target))

                if not os.path.exists(resolved):
                    rel_file = os.path.relpath(abs_path, KB_ROOT)
                    issues.append(f"{rel_file}:{line_num} → {target} (non esiste)")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: check_refs.py file1.md [file2.md ...]")
        sys.exit(2)

    all_issues = []
    for f in sys.argv[1:]:
        all_issues.extend(check_file(f))

    if not all_issues:
        print("Check 1 — Referenze: ✓ PASS")
        sys.exit(0)
    else:
        print(f"Check 1 — Referenze: ✗ FAIL ({len(all_issues)} issue)")
        for issue in all_issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
