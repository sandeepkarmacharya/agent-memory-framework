import os
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


def test_install_bootstraps_target_project_without_existing_agents_file(tmp_path):
    project = tmp_path / "app"
    project.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)

    result = run_cli(ROOT, "install", "--target", str(project))

    assert result.returncode == 0, result.stderr
    assert "Installed Agent Memory Framework" in result.stdout
    assert (project / "AGENTS.md").exists()
    assert (project / ".ai" / "current-state.md").exists()
    assert (project / ".ai" / "agent-handoff.md").exists()
    assert (project / "scripts" / "agent-memory").exists()
    assert os.access(project / "scripts" / "agent-memory", os.X_OK)
    assert (project / "scripts" / "memory_query" / "indexer.py").exists()
    assert (project / ".githooks" / "pre-commit").exists()
    assert os.access(project / ".githooks" / "pre-commit", os.X_OK)

    for rel in ["CLAUDE.md", ".cursorrules", ".codex/AGENTS.md", "HERMES.md"]:
        text = (project / rel).read_text(encoding="utf-8")
        assert 'python scripts/agent-memory context "<task>"' in text
        assert 'python scripts/agent-memory finish --summary "<what changed>" --next "<next task>"' in text

    hooks_path = subprocess.run(
        ["git", "config", "core.hooksPath"],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=5,
        check=True,
    ).stdout.strip()
    assert hooks_path == ".githooks"

    validate = subprocess.run(
        [sys.executable, str(project / "scripts" / "agent-memory"), "validate"],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert validate.returncode == 0, validate.stderr


def test_install_preserves_existing_agents_file(tmp_path):
    project = tmp_path / "existing"
    project.mkdir()
    (project / "AGENTS.md").write_text("# Existing project instructions\n", encoding="utf-8")

    result = run_cli(ROOT, "install", "--target", str(project))

    assert result.returncode == 0, result.stderr
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "# Existing project instructions\n"
    assert "AGENTS.md already exists" in result.stdout
    assert (project / ".ai" / "task-board.md").exists()


def test_install_preserves_existing_agent_hook_files(tmp_path):
    project = tmp_path / "custom-hooks"
    project.mkdir()
    (project / "CLAUDE.md").write_text("# Custom Claude instructions\n", encoding="utf-8")

    result = run_cli(ROOT, "install", "--target", str(project))

    assert result.returncode == 0, result.stderr
    assert (project / "CLAUDE.md").read_text(encoding="utf-8") == "# Custom Claude instructions\n"
    assert "CLAUDE.md already exists" in result.stdout
    assert 'python scripts/agent-memory context "<task>"' in (project / ".cursorrules").read_text(encoding="utf-8")
