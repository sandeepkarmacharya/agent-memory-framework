# Agent Handoff

This is the primary file for switching agents. Keep it concise and current.

## Latest session summary

Completed step 2: AGENTS now tells agents to run `agent-memory context "<task>"` before reading memory files.

## What was completed

- Replaced broad minimum-read list in AGENTS first rule.
- Added context-first instruction with fallback-only manual read list.
- Updated retrieval section to prefer context packs before raw query.
- Added tests for AGENTS context-first behavior.

## Files changed

- `AGENTS.md`
- `tests/test_agent_instructions.py`
- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`
- `.ai/test-results.md`
- `.ai/decisions.md`
- `.ai/.memory_index/index.json`

## Decisions made

- Context pack is now the default task-start path for agents.
- Raw query/manual file reads are fallback or deeper follow-up only.

## Bugs found or fixed

- None.

## Current task status

- Step 2 complete.

## Next recommended task

- Add `finish --summary` command to update memory from task summary/git diff and rebuild index.

## Commands run

```bash
python -m pytest tests/test_agent_instructions.py -q
python -m pytest -q
python scripts/agent-memory context "update AGENTS first rule to context first" --top-k 2 --budget 1200
python scripts/agent-memory validate
python scripts/agent-memory index
```

## Validation status

- Tests run: 4 passed.
- Manual checks: context output, validate, index passed.
- Not verified: packaging/CI absent.

## Warnings for next agent

- `validate` still warns about unchanged template files: graph-memory, dependencies, security, api-contracts.

## Do not redo

- Do not re-add context-first AGENTS rule; extend only if needed.

## Suggested next prompt

```txt
Continue one step: implement agent-memory finish --summary with tests first.
```

## Last updated

- Date: 2026-05-18
- Agent/tool: Hermes / GPT-5.5 Codex

## 2026-05-18 — Finish

- Summary: Added finish command to update core memory after tasks
- Next: Add install command for drop-in setup
- Changed files:
- `AGENTS.md`
- `README.md`
- `scripts/agent-memory`
- `skills/README.md`
- `tests/test_finish_command.py`

## 2026-05-18 — Finish

- Summary: added drop-in install command for target projects
- Next: add automatic background memory optimization hooks
- Changed files:
- `AGENTS.md`
- `README.md`
- `scripts/agent-memory`
- `tests/test_install_command.py`
