"""Git commit and push for publishing new digests."""

import subprocess
import sys
from datetime import datetime, timezone


def git_publish() -> None:
    """Stage content/ changes, commit, and push to origin main.

    Handles the case where there are no changes gracefully.
    """
    repo_root = _find_repo_root()
    if not repo_root:
        print("  Warning: Not in a git repository, skipping git publish")
        return

    now = datetime.now(timezone.utc)
    week_number = now.isocalendar()[1]
    year = now.year

    try:
        # Stage content directory
        _run_git(["git", "add", "content/"], cwd=repo_root)

        # Check if there are staged changes
        result = _run_git(
            ["git", "diff", "--staged", "--quiet"],
            cwd=repo_root,
            check=False,
        )
        if result.returncode == 0:
            print("  No changes to commit")
            return

        # Commit
        commit_msg = f"digest: Week {week_number}, {year}"
        _run_git(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_root,
        )
        print(f"  Committed: {commit_msg}")

        # Push
        _run_git(["git", "push", "origin", "main"], cwd=repo_root)
        print("  Pushed to origin/main")

    except subprocess.CalledProcessError as e:
        print(f"  Git error: {e}", file=sys.stderr)
        raise


def _run_git(
    cmd: list[str], cwd: str, check: bool = True
) -> subprocess.CompletedProcess:
    """Run a git command and return the result."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def _find_repo_root() -> str | None:
    """Find the git repository root directory."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
