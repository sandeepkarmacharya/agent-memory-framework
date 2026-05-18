import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "agent-memory"


def run_cli(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=30,
    )


def make_memory_repo(tmp_path: Path) -> Path:
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    ai = tmp_path / ".ai"
    ai.mkdir()
    (ai / "agent-handoff.md").write_text("# Agent Handoff\nLast task: build login.\n", encoding="utf-8")
    (ai / "current-state.md").write_text("# Current State\nAuth module in progress.\n", encoding="utf-8")
    (ai / "task-board.md").write_text("# Task Board\nNext: fix auth redirect bug.\n", encoding="utf-8")
    (ai / "decisions.md").write_text("# Decisions\nUse session cookies for auth.\n", encoding="utf-8")
    (ai / "bugs-and-fixes.md").write_text(
        "# Bugs and Fixes\nAuth redirect bug happens after login callback.\n",
        encoding="utf-8",
    )
    (ai / "architecture.md").write_text("# Architecture\nLogin controller handles callback.\n", encoding="utf-8")
    return tmp_path


def test_context_command_outputs_context_pack_with_always_included_and_relevant_memory(tmp_path):
    repo = make_memory_repo(tmp_path)

    result = run_cli(repo, "context", "fix auth redirect bug", "--top-k", "2", "--budget", "1200")

    assert result.returncode == 0, result.stderr
    assert "# Agent Memory Context Pack" in result.stdout
    assert "Task: fix auth redirect bug" in result.stdout
    assert "## Always Included" in result.stdout
    assert ".ai/agent-handoff.md" in result.stdout
    assert ".ai/current-state.md" in result.stdout
    assert ".ai/task-board.md" in result.stdout
    assert "## Relevant Memory" in result.stdout
    assert ".ai/bugs-and-fixes.md" in result.stdout
    assert "## Files To Read Fully" in result.stdout


def test_context_command_respects_budget_by_truncating_large_memory_files(tmp_path):
    repo = make_memory_repo(tmp_path)
    large_text = "# Current State\n" + "auth redirect detail " * 300
    (repo / ".ai" / "current-state.md").write_text(large_text, encoding="utf-8")

    result = run_cli(repo, "context", "auth redirect", "--top-k", "1", "--budget", "500")

    assert result.returncode == 0, result.stderr
    assert "Budget: ~500 tokens" in result.stdout
    assert "[truncated]" in result.stdout
    assert len(result.stdout) < len(large_text)
