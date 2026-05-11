---
name: feature
description: Add a new feature safely using the memory framework. Use when the user asks to build, add, implement, extend, or integrate a feature.
---


# Feature

## Goal

Add a feature as a small, safe vertical slice that fits the existing architecture.

## Read first

1. `AGENTS.md`
2. `.ai/project-brief.md`
3. `.ai/current-state.md`
4. `.ai/task-board.md`
5. `.ai/architecture.md`
6. `.ai/decisions.md`
7. `.ai/graph-memory.md`
8. `.ai/coding-standards.md`

## Workflow

1. Restate the feature.
2. Explain how it fits the architecture.
3. Identify affected files, components, APIs, data, and UI.
4. Check for conflicts with decisions.
5. Break the work into small slices.
6. Implement the smallest useful slice.
7. Validate it.
8. Update memory.

## Rules

- Do not build unrelated features.
- Do not over-engineer.
- Prefer a thin working slice.
- If the feature needs a decision, record it.

## Required updates

- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/graph-memory.md`
- `.ai/agent-handoff.md`
- `.ai/decisions.md` if relevant
- `.ai/bugs-and-fixes.md` if relevant

