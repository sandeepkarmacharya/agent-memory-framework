from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


def test_ci_workflow_runs_project_quality_gates():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "python -m pytest -q" in text
    assert "python scripts/agent-memory validate" in text
    assert "python scripts/agent-memory doctor" in text
    assert "python scripts/agent-memory optimize" in text
    assert "python scripts/agent-memory index" in text


def test_ci_workflow_runs_on_pushes_and_pull_requests():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "push:" in text
    assert "pull_request:" in text
    assert "branches: [main]" in text


def test_ci_workflow_uses_multiple_supported_python_versions():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "python-version: ['3.11', '3.12']" in text
    assert "actions/checkout@v6" in text
    assert "actions/setup-python@v6" in text
    assert "python -m pip install pytest" in text
    assert "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true" in text
