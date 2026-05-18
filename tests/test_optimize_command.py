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
    (ai / "current-state.md").write_text("# Current State\n\nActive work.\n", encoding="utf-8")
    (ai / "agent-handoff.md").write_text("# Agent Handoff\n\n" + ("duplicate line that should compress\n\n" * 80), encoding="utf-8")
    (ai / "task-board.md").write_text("# Task Board\n\n## Next\n- Optimize memory\n", encoding="utf-8")
    return tmp_path


def test_optimize_reports_bloat_and_stale_index_without_applying(tmp_path):
    repo = make_memory_repo(tmp_path)

    result = run_cli(repo, "optimize", "--max-bytes", "500")

    assert result.returncode == 0, result.stderr
    assert "Memory optimization report" in result.stdout
    assert "Bloated files" in result.stdout
    assert ".ai/agent-handoff.md" in result.stdout
    assert "Index status: stale or missing" in result.stdout
    assert "Run with --apply" in result.stdout
    assert not (repo / ".ai" / ".memory_index" / "index.json").exists()


def test_optimize_apply_compresses_and_rebuilds_index(tmp_path):
    repo = make_memory_repo(tmp_path)
    handoff = repo / ".ai" / "agent-handoff.md"
    before = len(handoff.read_text(encoding="utf-8"))

    result = run_cli(repo, "optimize", "--max-bytes", "500", "--apply")

    assert result.returncode == 0, result.stderr
    after = len(handoff.read_text(encoding="utf-8"))
    assert after < before
    assert "Applied safe compression" in result.stdout
    assert "Rebuilt memory index" in result.stdout
    assert (repo / ".ai" / ".memory_index" / "index.json").exists()
