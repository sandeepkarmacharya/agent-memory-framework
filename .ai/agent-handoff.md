# Agent Handoff

This is the primary file for switching agents. Keep it concise and current.

## Latest session summary

Added first automation step: `agent-memory context "<task>"`.

## What was completed

- Added compact context pack CLI command.
- Added budget-aware truncation.
- Added always-included continuity files.
- Added BM25-ranked relevant memory section.
- Added tests.
- Updated README, AGENTS command table, skills README.

## Files changed

- `scripts/agent-memory`
- `tests/test_context_command.py`
- `README.md`
- `AGENTS.md`
- `skills/README.md`
- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`
- `.ai/test-results.md`
- `.ai/decisions.md`

## Decisions made

- Use `context` as first runtime abstraction above raw `query`/manual slash commands.

## Bugs found or fixed

- None.

## Current task status

- Step 1 complete.

## Next recommended task

- Add `finish --summary` command to update memory from task summary/git diff and rebuild index.

## Commands run

```bash
python -m pytest tests/test_context_command.py -q
python -m pytest -q
python scripts/agent-memory context "fix auth redirect bug" --top-k 2 --budget 1200
python scripts/agent-memory validate
python scripts/agent-memory index
```

## Validation status

- Tests run: 2 passed.
- Manual checks: context output, validate, index passed.
- Not verified: packaging/CI absent.

## Warnings for next agent

- `validate` still warns about unchanged template files: graph-memory, test-results, dependencies, security, api-contracts.
- AGENTS first-rule still asks agents to read many files; next step should switch that to context-first.

## Do not redo

- Do not re-add context command; extend it only if needed.

## Suggested next prompt

```txt
Continue one step: implement agent-memory finish --summary with tests first.
```

## Last updated

- Date: 2026-05-18
- Agent/tool: Hermes / GPT-5.5 Codex
