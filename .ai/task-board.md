# Task Board

Keep this simple and current. Prefer small vertical slices.

## Next recommended task

- Add `finish --summary` command.

## In progress

- Automatic memory runtime, one step at time.

## Backlog

- Add `install` command for drop-in project setup.
- Add `doctor` command for memory/index/hook/staleness health.
- Add CI workflow.
- Add package metadata for pipx/uv install.

## Blocked

- None.

## Done

- Updated AGENTS first-rule to prefer `agent-memory context "<task>"` over reading all `.ai/` files.
- Added tests that enforce context-first AGENTS instructions.
- Added `agent-memory context "<task>"` command.
- Added tests for context pack output and budget truncation.
- Documented context command in README, AGENTS command table, skills README.

## Parking lot

Ideas useful but not urgent:

- Memory quality score: freshness/coverage/bloat/staleness risk.
- Smart compression with archive for old completed tasks.

## 2026-05-18 — Task Update

### Done
- Added finish command to update core memory after tasks

### Next
- Add install command for drop-in setup
