#!/usr/bin/env python3
"""
Check 5: Struttura vs documentazione (bidirezionale).
- Diretto: directory reali devono essere documentate
- Inverso: directory documentate devono esistere

Usage: python3 check_struttura.py
Exit: 0 = PASS, 1 = FAIL
"""

import sys
import os
import re

KB_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
STRUTTURA = os.path.join(KB_ROOT, "docs", "struttura.md")
INDEX = os.path.join(KB_ROOT, "projects", "INDEX.md")

# Placeholder nel tree che non sono directory reali
PLACEHOLDERS = {"[nome-progetto]", "nome-progetto"}


def read_file(path):
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def list_subdirs(parent):
    """Lista le subdirectory immediate di una cartella."""
    if not os.path.isdir(parent):
        return []
    return [
        d for d in os.listdir(parent)
        if os.path.isdir(os.path.join(parent, d)) and not d.startswith(".")
    ]


def parse_tree_paths(struttura_content):
    """
    Parsa il blocco code con il tree in docs/struttura.md.
    Ritorna una lista di percorsi directory relativi (es. 'skills/presales/init-project/').
    """
    # Estrai il blocco di codice con il tree
    match = re.search(r'```\n(.*?)```', struttura_content, re.DOTALL)
    if not match:
        return []

    tree = match.group(1)
    paths = []
    stack = []  # [(depth, name)]

    for line in tree.splitlines():
        # Rimuovi commenti descrittivi (tutto dopo ←)
        line_clean = line.split("←")[0].rstrip()

        # Cerca entry directory: ├── name/ o └── name/
        m = re.search(r'[├└]── (.+?)/', line_clean)
        if not m:
            continue

        name = m.group(1).strip()

        # Ignora placeholder
        if name in PLACEHOLDERS or name.startswith("["):
            continue

        # Calcola profondità basata sulla posizione del ├ o └
        pos = line.index('├') if '├' in line else line.index('└')
        depth = pos // 4

        # Aggiorna lo stack: rimuovi tutto ciò che è >= depth corrente
        stack = [(d, n) for d, n in stack if d < depth]
        stack.append((depth, name))

        # Costruisci il percorso completo
        full_path = "/".join(n for _, n in stack) + "/"
        paths.append(full_path)

    return paths


def main():
    struttura_content = read_file(STRUTTURA)
    index_content = read_file(INDEX)
    issues = []

    # ===== CHECK DIRETTO: directory reali → documentazione =====

    # 1. Skill directories
    skills_dir = os.path.join(KB_ROOT, "skills")
    for phase in list_subdirs(skills_dir):
        phase_dir = os.path.join(skills_dir, phase)
        for skill in list_subdirs(phase_dir):
            if skill + "/" not in struttura_content:
                issues.append(f"skills/{phase}/{skill}/ esiste ma non è in docs/struttura.md")

    # 2. Progetti reali (non _prefixed) in INDEX.md
    projects_dir = os.path.join(KB_ROOT, "projects")
    for proj in list_subdirs(projects_dir):
        if proj.startswith("_"):
            continue
        if proj.lower() not in index_content.lower():
            issues.append(f"projects/{proj}/ esiste ma non è in projects/INDEX.md")

    # 3. Subdirectory di knowledge/
    knowledge_dir = os.path.join(KB_ROOT, "knowledge")
    for sub in list_subdirs(knowledge_dir):
        if sub + "/" not in struttura_content:
            issues.append(f"knowledge/{sub}/ esiste ma non è in docs/struttura.md")

    # 4. Subdirectory di core/
    core_dir = os.path.join(KB_ROOT, "core")
    for sub in list_subdirs(core_dir):
        if sub + "/" not in struttura_content:
            issues.append(f"core/{sub}/ esiste ma non è in docs/struttura.md")

    # ===== CHECK INVERSO: documentazione → directory reali =====

    documented_paths = parse_tree_paths(struttura_content)

    for doc_path in documented_paths:
        # Ignora percorsi sotto _template/ (sono descrittivi, non reali)
        if "/_template/" in doc_path or doc_path.startswith("_template/"):
            continue
        real_path = os.path.join(KB_ROOT, doc_path)
        if not os.path.isdir(real_path):
            issues.append(f"{doc_path} documentata in docs/struttura.md ma non esiste")

    # ===== OUTPUT =====

    if not issues:
        print("Check 5 — Struttura: ✓ PASS")
        sys.exit(0)
    else:
        print(f"Check 5 — Struttura: ✗ FAIL ({len(issues)} issue)")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
