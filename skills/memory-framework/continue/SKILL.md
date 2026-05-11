---
name: continue
description: Continue an existing project from repository memory. Use when the user runs /continue or asks to resume work without losing context.
---


# Continue Project

## Goal

Resume from the repository memory instead of chat memory.

## Read first

1. `AGENTS.md`
2. `.ai/agent-handoff.md`
3. `.ai/current-state.md`
4. `.ai/task-board.md`
5. `.ai/decisions.md`
6. `.ai/architecture.md`
7. `.ai/graph-memory.md`
8. `.ai/bugs-and-fixes.md`

## Workflow

1. Summarize:
   - What the project is
   - What is built
   - What is in progress
   - What decisions must be preserved
   - What the next best task is
2. Continue from the next best task.
3. Make the smallest useful change.
4. Test or validate the change.
5. Update memory before stopping.

## Rules

- Do not restart planning from scratch.
- Do not ignore existing decisions.
- Do not make unrelated changes.
- If memory conflicts with code, inspect code and record the correction.

## Required updates

- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`
- `.ai/graph-memory.md`
- `.ai/bugs-and-fixes.md` if relevant
- `.ai/decisions.md` if relevant

