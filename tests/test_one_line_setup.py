import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.sh"
README = ROOT / "README.md"
ONE_LINER = "curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | bash"


def test_readme_exposes_copy_paste_one_line_setup():
    text = README.read_text(encoding="utf-8")

    assert "One-line setup" in text
    assert ONE_LINER in text
    assert "Installs into the current project by default" in text


def test_bootstrap_installer_installs_into_current_directory_from_local_source(tmp_path):
    project = tmp_path / "app"
    project.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    env = os.environ.copy()
    env["AGENT_MEMORY_SOURCE"] = str(ROOT)

    result = subprocess.run(
        ["bash", str(INSTALLER)],
        cwd=project,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert "Agent Memory Framework ready" in result.stdout
    assert (project / "AGENTS.md").exists()
    assert (project / "scripts" / "agent-memory").exists()
    assert os.access(project / "scripts" / "agent-memory", os.X_OK)
    assert (project / ".ai" / "current-state.md").exists()
    assert (project / ".githooks" / "pre-commit").exists()

    validate = subprocess.run(
        ["python", "scripts/agent-memory", "validate"],
        cwd=project,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert validate.returncode == 0, validate.stderr


def test_bootstrap_installer_upgrades_existing_installation_without_overwriting_custom_hook(tmp_path):
    project = tmp_path / "existing"
    project.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    (project / "CLAUDE.md").write_text("# Custom Claude rules\n", encoding="utf-8")
    (project / ".ai").mkdir()
    env = os.environ.copy()
    env["AGENT_MEMORY_SOURCE"] = str(ROOT)

    result = subprocess.run(
        ["bash", str(INSTALLER)],
        cwd=project,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    text = (project / "CLAUDE.md").read_text(encoding="utf-8")
    assert "# Custom Claude rules" in text
    assert "<!-- agent-memory:managed:start -->" in text
    assert "python scripts/agent-memory upgrade --target" in result.stdout
