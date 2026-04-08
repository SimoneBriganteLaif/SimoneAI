#!/usr/bin/env python3
"""
Sincronizza i repository LAIF: clone se non esistono, pull se esistono.

Uso:
    python3 sync_repos.py --config ../repos.yaml [--dry-run]
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def sync_repo(name: str, url: str, branch: str, workspace: Path, dry_run: bool) -> str:
    """Clona o aggiorna un singolo repo. Ritorna stato: cloned/pulled/failed/skipped."""
    repo_dir = workspace / name

    if repo_dir.exists():
        if dry_run:
            return "would_pull"
        try:
            subprocess.run(
                ["git", "-C", str(repo_dir), "fetch", "origin"],
                capture_output=True, check=True, timeout=60
            )
            subprocess.run(
                ["git", "-C", str(repo_dir), "checkout", branch],
                capture_output=True, check=True, timeout=30
            )
            subprocess.run(
                ["git", "-C", str(repo_dir), "pull", "origin", branch],
                capture_output=True, check=True, timeout=120
            )
            return "pulled"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"  ERRORE pull {name}: {e}", file=sys.stderr)
            return "failed"
    else:
        if dry_run:
            return "would_clone"
        try:
            subprocess.run(
                ["git", "clone", "--branch", branch, "--single-branch", url, str(repo_dir)],
                capture_output=True, check=True, timeout=300
            )
            return "cloned"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"  ERRORE clone {name}: {e}", file=sys.stderr)
            return "failed"


def main():
    parser = argparse.ArgumentParser(description="Sincronizza repository LAIF")
    parser.add_argument("--config", required=True, help="Path a repos.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Mostra cosa farebbe senza eseguire")
    args = parser.parse_args()

    config = load_config(args.config)
    workspace = Path(config["workspace"]).expanduser()
    default_branch = config.get("default_branch", "master")
    github_org = config.get("github_org", "laif-group")

    if not args.dry_run:
        workspace.mkdir(parents=True, exist_ok=True)

    results = {"cloned": 0, "pulled": 0, "failed": 0, "skipped": 0,
               "would_clone": 0, "would_pull": 0}

    for repo in config["repos"]:
        name = repo["name"]
        if repo.get("skip", False):
            results["skipped"] += 1
            continue

        branch = repo.get("branch", default_branch)
        url = repo.get("url", f"git@github.com:{github_org}/{name}.git")

        print(f"{'[DRY] ' if args.dry_run else ''}{name} ({branch})...", end=" ")
        status = sync_repo(name, url, branch, workspace, args.dry_run)
        results[status] += 1
        print(status)

    print(f"\n--- Risultati ---")
    for k, v in results.items():
        if v > 0:
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
