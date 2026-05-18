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


def test_doctor_reports_ready_project_health(tmp_path):
    project = tmp_path / "healthy"
    project.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    install = run_cli(ROOT, "install", "--target", str(project))
    assert install.returncode == 0, install.stderr
    index = subprocess.run(
        [sys.executable, str(project / "scripts" / "agent-memory"), "index"],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert index.returncode == 0, index.stderr

    result = subprocess.run(
        [sys.executable, str(project / "scripts" / "agent-memory"), "doctor"],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    assert "Agent Memory Doctor" in result.stdout
    assert "Setup health" in result.stdout
    assert "Memory files" in result.stdout
    assert "Retrieval index" in result.stdout
    assert "Optimization" in result.stdout
    assert "RESULT: READY" in result.stdout


def test_doctor_fails_with_actionable_fix_for_missing_required_files(tmp_path):
    project = tmp_path / "broken"
    project.mkdir()

    result = run_cli(project, "doctor")

    assert result.returncode == 1
    assert "Agent Memory Doctor" in result.stdout
    assert "Missing required: AGENTS.md" in result.stdout
    assert "Missing required: .ai/project-brief.md" in result.stdout
    assert "Next actions" in result.stdout
    assert "python scripts/agent-memory install --target ." in result.stdout
