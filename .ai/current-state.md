# Current State

## Current development stage

Building.

## What is built

- CLI: `init`, `validate`, `compress`, `index`, `query`, `search`, `import`, `suggest`.
- CLI: `context "<task>"` builds compact task-specific context pack.
- Context pack always includes handoff/current-state/task-board, then BM25-ranked relevant memory.
- Context pack supports `--top-k` and `--budget` with truncation marker.
- AGENTS first rule is context-first: agents run `agent-memory context "<task>"` before reading memory files.

## What is partially built

- Automatic memory runtime: context-first start done; finish/install/doctor pending.

## What is broken

- None known.

## Current blockers

- None.

## Current focus

- Make framework automatic, low-command, token-saving for coding agents.

## Next recommended task

- Add `finish --summary` command to update handoff/current-state/task-board from git diff and rebuild index.

## Validation status

- Tests run: `python -m pytest -q` -> 4 passed.
- Manual checks: `agent-memory context`, `validate`, `index` passed.
- Known unverified areas: no CI yet; no install packaging yet.

## Last updated

- Date: 2026-05-18
- Agent/tool: Hermes / GPT-5.5 Codex

## 2026-05-18 — Latest Progress

- Latest progress: Added finish command to update core memory after tasks
- Next recommended task: Add install command for drop-in setup
- Last updated: 2026-05-18

## 2026-05-18 — Latest Progress

- Latest progress: added drop-in install command for target projects
- Next recommended task: add automatic background memory optimization hooks
- Last updated: 2026-05-18

## 2026-05-18 — Latest Progress

- Latest progress: added generated agent auto-hook instruction files
- Next recommended task: add optional background memory optimizer/watch command
- Last updated: 2026-05-18

## 2026-05-18 — Latest Progress

- Latest progress: added optimize command for memory bloat and stale index cleanup
- Next recommended task: wire optimize into install/agent hooks as periodic maintenance
- Last updated: 2026-05-18

## 2026-05-18 — Latest Progress

- Latest progress: wired optimize into generated agent hooks and AGENTS maintenance guidance
- Next recommended task: consider auto-updating existing hook files with opt-in upgrade command
- Last updated: 2026-05-18
