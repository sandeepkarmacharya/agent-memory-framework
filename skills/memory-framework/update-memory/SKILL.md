---
name: update-memory
description: Update project memory after a meaningful task. Use when the user runs /update-memory or after coding, debugging, reviewing, planning, or changing architecture.
---


# Update Memory

## Goal

Keep repo memory accurate after work is completed.

## Workflow

Review the completed work and update:

1. `.ai/current-state.md`
   - What is now built
   - What is incomplete
   - What is broken
   - What should happen next
2. `.ai/task-board.md`
   - Move completed work to Done
   - Add new tasks discovered
   - Mark blocked tasks
   - Set next recommended task
3. `.ai/agent-handoff.md`
   - Write a concise handoff
   - Include changed files, commands, validation, known issues, and next task
4. `.ai/graph-memory.md`
   - Update feature/file/API/data/bug/decision relationships
5. `.ai/bugs-and-fixes.md`
   - Add bugs found, fixes attempted, fixes completed, or regression risks
6. `.ai/decisions.md`
   - Add important decisions only

## Rules

- Do not rewrite everything.
- Preserve useful history.
- Remove duplicated stale information only when clearly safe.
- Mark unverified work.

