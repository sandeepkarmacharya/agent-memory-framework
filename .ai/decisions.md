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
- Agents rely on CLI availability for optimal path; manual read list remains fallback.

Revisit when:
- Adding real tokenizer dependency or model-specific budgeting.
- Adding `finish`/`install` runtime commands.
- Context command becomes unavailable in target agent environments.

## 2026-05-18 — Add finish command as task-end automation

Status: Accepted

Context:
- Framework needs automatic task-end memory updates so users/agents do not memorize handoff/current-state/task-board update rules.
- Context command handles task start; task end still needed a symmetric runtime command.

Decision:
- Add `agent-memory finish --summary "<done>" --next "<next>"`.
- Command appends to handoff/current-state/task-board, records Git changed/untracked files, rebuilds BM25 index.

Reason:
- Gives agents one obvious command after work.
- Keeps memory fresh with less manual instruction-following.
- Preserves existing memory by appending instead of rewriting.

Impact:
- `scripts/agent-memory`
- `README.md`
- `AGENTS.md`
- `skills/README.md`
- `tests/test_finish_command.py`

Tradeoffs:
- Appends simple sections; does not yet intelligently rewrite stale sections.
- Git changed-file list is file-level only, not semantic.

Revisit when:
- Adding smart memory rewrite/compression.
- Adding LLM-assisted summarization.

## Superseded decisions

None yet.
