#!/usr/bin/env python3
"""
Verifica pre-commit — runner principale.
Esegue tutti i check automatici e riporta il risultato.

Usage: python3 run_all.py [file1 file2 ...]
       Se nessun file specificato, usa git per ricavarli.
Exit: 0 = PASS, >0 = numero di check FAIL
"""

import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))


def get_modified_files() -> list[str]:
    """Ricava i file modificati da git (staged + unstaged)."""
    try:
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            cwd=KB_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        staged = []

    try:
        unstaged = subprocess.check_output(
            ["git", "diff", "--name-only"],
            cwd=KB_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        unstaged = []

    try:
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=KB_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        untracked = []

    return sorted(set(staged + unstaged + untracked))


def run_check(script: str, args: list[str] = None) -> bool:
    """Esegue uno script Python e ritorna True se PASS."""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script)]
    if args:
        cmd.extend(args)

    result = subprocess.run(cmd, cwd=KB_ROOT)
    return result.returncode == 0


def main():
    # Ricava file modificati
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = get_modified_files()

    if not files:
        print("Nessun file modificato — niente da verificare.")
        sys.exit(0)

    md_files = [f for f in files if f.endswith(".md")]

    print("═══════════════════════════════════════")
    print("VERIFICA PRE-COMMIT")
    print(f"File da verificare: {len(files)}")
    print("═══════════════════════════════════════")
    print()

    total_fail = 0

    # Check 1: Referenze
    if md_files:
        if not run_check("check_refs.py", md_files):
            total_fail += 1
    else:
        print("Check 1 — Referenze: ✓ PASS (nessun .md)")
    print()

    # Check 2: Changelog
    if not run_check("check_changelog.py", files):
        total_fail += 1
    print()

    # Check 3: IDEAS (manuale)
    print("Check 3 — IDEAS: ⚠ manuale (il parent agent verifica semanticamente)")
    print()

    # Check 4: Tag
    if md_files:
        if not run_check("check_tags.py", md_files):
            total_fail += 1
    else:
        print("Check 4 — Tag: ✓ PASS (nessun .md)")
    print()

    # Check 5: Struttura
    if not run_check("check_struttura.py"):
        total_fail += 1

    print()
    print("═══════════════════════════════════════")
    if total_fail == 0:
        print("RISULTATO: PASS (check 3 da verificare manualmente)")
    else:
        print(f"RISULTATO: FAIL ({total_fail} check falliti)")
    print("═══════════════════════════════════════")

    sys.exit(total_fail)


if __name__ == "__main__":
    main()
