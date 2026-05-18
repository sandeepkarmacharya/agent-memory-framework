from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


def test_agents_first_rule_is_context_first_not_read_everything_first():
    text = AGENTS.read_text(encoding="utf-8")
    first_rule = text.split("## CLI tool", 1)[0]

    assert 'python scripts/agent-memory context "<task>"' in first_rule
    assert "Do not read all `.ai/` files by default" in first_rule
    assert "Fallback only" in first_rule
    assert "At minimum, read:" not in first_rule


def test_agents_retrieval_section_points_to_context_before_raw_query():
    text = AGENTS.read_text(encoding="utf-8")
    retrieval = text.split("## Retrieval layer", 1)[1].split("## Import", 1)[0]

    context_pos = retrieval.index('python scripts/agent-memory context "<task>"')
    query_pos = retrieval.index('python scripts/agent-memory query')
    assert context_pos < query_pos


def test_agents_required_updates_include_periodic_optimize_maintenance():
    text = AGENTS.read_text(encoding="utf-8")
    required = text.split("## Required memory updates", 1)[1].split("## Slash command mapping", 1)[0]

    assert "python scripts/agent-memory optimize" in required
    assert "periodic maintenance" in required
    assert "when context feels stale" in required
