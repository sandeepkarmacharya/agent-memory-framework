---
name: sync-decisions
description: Synchronize project decisions with the actual current code and memory. Use when decisions may be stale, contradictory, or missing after architecture/product changes.
---


# Sync Decisions

## Goal

Make the decision log trustworthy again.

## Read first

1. `.ai/decisions.md`
2. `.ai/current-state.md`
3. `.ai/architecture.md`
4. `.ai/task-board.md`
5. `.ai/graph-memory.yaml`
6. Relevant source files

## Workflow

1. List active decisions.
2. Compare them with current code and architecture.
3. Mark outdated decisions as `Superseded` instead of deleting them.
4. Add missing decisions that are clearly reflected in the code.
5. Add revisit conditions where needed.
6. Update graph-memory decision relationships.

## Rules

- Do not invent reasons.
- Do not rewrite history.
- Preserve superseded decisions for traceability.
- Mark uncertainty when code and docs conflict.

## Required updates

- `.ai/decisions.md`
- `.ai/graph-memory.yaml`
- `.ai/agent-handoff.md`

