# Decisions

Record important decisions here. Do not delete historical decisions unless they are clearly wrong or superseded.

## Active decisions

## 2026-05-18 — Add context command as first automation layer

Status: Accepted

Context:
- Framework goal: reduce token usage and long-term memory friction without user memorizing skill commands.
- Raw `query` helps retrieval but still requires agent/user to know when/how to compose context.

Decision:
- Add `agent-memory context "<task>"` as task-start runtime command.
- Context pack includes continuity files plus BM25-ranked relevant memory.
- Token budget uses approximate char-based truncation; no external tokenizer dependency.

Reason:
- Gives agents one obvious command before work.
- Reduces default need to read every `.ai/` file.
- Keeps framework zero-dependency.

Impact:
- `scripts/agent-memory`
- `README.md`
- `AGENTS.md`
- `skills/README.md`
- `tests/test_context_command.py`

Tradeoffs:
- Token counting approximate.
- AGENTS read-order still needs separate context-first rule update.

Revisit when:
- Adding real tokenizer dependency or model-specific budgeting.
- Adding `finish`/`install` runtime commands.

## Superseded decisions

None yet.
