"""H. Git stats: contributor, ultimo commit."""

from __future__ import annotations

import subprocess
from pathlib import Path

# Branch upstream da provare in ordine (locali e remoti)
UPSTREAM_REFS = [
    "upstream/main",
    "upstream/master",
    "upstream/develop",
    "remotes/upstream/main",
    "remotes/upstream/master",
    "remotes/upstream/develop",
]


def run(repo_path: str, baseline: dict) -> dict:
    repo = Path(repo_path)

    if not (repo / ".git").exists():
        return {"contributors": [], "last_commit": None}

    contributors = _get_contributors(repo)
    last_commit = _get_last_commit(repo)

    return {
        "contributors": contributors,
        "contributor_count": len(contributors),
        "last_commit": last_commit,
    }


def _find_upstream_ref(repo: Path) -> str | None:
    """Trova il ref upstream da usare per escludere commit template."""
    for ref in UPSTREAM_REFS:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", ref],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return ref
    return None


def _get_contributors(repo: Path) -> list:
    """Lista contributor con conteggio commit, esclusi commit template."""
    upstream_ref = _find_upstream_ref(repo)

    try:
        cmd = ["git", "-C", str(repo), "shortlog", "-sn", "--no-merges"]
        if upstream_ref:
            cmd.extend(["HEAD", "--not", upstream_ref])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        # Se il filtro upstream non ha dato risultati, prova senza filtro
        if result.returncode != 0 or not result.stdout.strip():
            result = subprocess.run(
                ["git", "-C", str(repo), "shortlog", "-sn", "--no-merges", "HEAD"],
                capture_output=True, text=True, timeout=30
            )
    except subprocess.TimeoutExpired:
        return []

    contributors = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            count = int(parts[0].strip())
            name = parts[1].strip()
            contributors.append({"name": name, "commits": count})

    return contributors


def _get_last_commit(repo: Path) -> dict | None:
    """Data e info dell'ultimo commit."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%H|%ai|%an|%s"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return None
    except subprocess.TimeoutExpired:
        return None

    parts = result.stdout.strip().split("|", 3)
    if len(parts) == 4:
        return {
            "hash": parts[0],
            "date": parts[1],
            "author": parts[2],
            "message": parts[3],
        }
    return None
