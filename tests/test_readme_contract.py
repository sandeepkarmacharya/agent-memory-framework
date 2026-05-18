from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def readme() -> str:
    return README.read_text(encoding="utf-8")


def test_readme_is_concise_but_complete():
    text = readme()
    lines = text.splitlines()

    assert len(lines) <= 260
    assert "## Quick start" in text
    assert "## Daily workflow" in text
    assert "## Command reference" in text
    assert "## What gets installed" in text
    assert "## Memory files" in text
    assert "## Agent support" in text
    assert "## Troubleshooting" in text
    assert "## Safety notes" in text


def test_readme_guides_novice_users_without_requiring_command_memorization():
    text = readme()

    assert "If you are new, run the one-liner and then ask your agent to read `AGENTS.md`." in text
    assert "You do not need to memorize these commands." in text
    assert "AGENTS.md" in text
    assert "CLAUDE.md" in text
    assert ".cursorrules" in text
    assert ".codex/AGENTS.md" in text
    assert "HERMES.md" in text


def test_readme_keeps_required_setup_and_advanced_commands():
    text = readme()

    required_commands = [
        "curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | bash",
        "AGENT_MEMORY_TARGET=/path/to/your/project",
        "python scripts/agent-memory context \"<task>\"",
        "python scripts/agent-memory finish --summary",
        "python scripts/agent-memory doctor",
        "python scripts/agent-memory optimize --apply",
        "python scripts/agent-memory upgrade --target",
        "python scripts/agent-memory import",
        "python scripts/agent-memory query",
        "python scripts/agent-memory suggest",
    ]
    for command in required_commands:
        assert command in text


def test_readme_removes_old_verbose_sections():
    text = readme()

    assert "## Slash Commands" not in text
    assert "## Caveman Mode" not in text
    assert "### `install`" not in text
    assert "### `query`" not in text
    assert "Why YAML for graph memory?" not in text
