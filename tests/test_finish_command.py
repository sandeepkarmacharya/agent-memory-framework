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


def make_repo(tmp_path: Path) -> Path:
    (tmp_path / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
    ai = tmp_path / ".ai"
    ai.mkdir()
    (ai / "agent-handoff.md").write_text("# Agent Handoff\n\nOld handoff.\n", encoding="utf-8")
    (ai / "current-state.md").write_text("# Current State\n\nOld state.\n", encoding="utf-8")
    (ai / "task-board.md").write_text("# Task Board\n\n## Done\n- Old task\n", encoding="utf-8")
    (ai / "decisions.md").write_text("# Decisions\n", encoding="utf-8")
    (ai / "bugs-and-fixes.md").write_text("# Bugs\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=tmp_path, check=True)
    (tmp_path / "app.py").write_text("print('changed')\n", encoding="utf-8")
    return tmp_path


def test_finish_summary_updates_core_memory_and_rebuilds_index(tmp_path):
    repo = make_repo(tmp_path)

    result = run_cli(repo, "finish", "--summary", "Added context-first finish automation", "--next", "Add install command")

    assert result.returncode == 0, result.stderr
    assert "Updated .ai/agent-handoff.md" in result.stdout
    assert "Updated .ai/current-state.md" in result.stdout
    assert "Updated .ai/task-board.md" in result.stdout
    assert "Rebuilt memory index" in result.stdout

    handoff = (repo / ".ai" / "agent-handoff.md").read_text(encoding="utf-8")
    current_state = (repo / ".ai" / "current-state.md").read_text(encoding="utf-8")
    task_board = (repo / ".ai" / "task-board.md").read_text(encoding="utf-8")

    assert "Added context-first finish automation" in handoff
    assert "app.py" in handoff
    assert "Add install command" in handoff
    assert "Added context-first finish automation" in current_state
    assert "Add install command" in current_state
    assert "Added context-first finish automation" in task_board
    assert "Add install command" in task_board
    assert (repo / ".ai" / ".memory_index" / "index.json").exists()


def test_finish_requires_summary(tmp_path):
    repo = make_repo(tmp_path)

    result = run_cli(repo, "finish")

    assert result.returncode != 0
    assert "required" in result.stderr.lower()
