---
name: new
description: Start a new project using the Agent Memory Framework. Use when the user runs /new or asks to begin a new build with durable multi-agent memory.
---


# New Project

## Goal

Start a new project without creating messy context debt.

## Before coding

1. Read `AGENTS.md`.
2. Read all `.ai/` files.
3. Ask only for missing information that blocks a safe first step.
4. If enough context exists, proceed without unnecessary questions.

## Workflow

1. Summarize the project goal.
2. Fill or update `.ai/project-brief.md`.
3. Create an initial architecture outline in `.ai/architecture.md`.
4. Record initial decisions in `.ai/decisions.md`.
5. Create a small task plan in `.ai/task-board.md`.
6. Pick the safest first vertical slice.
7. Implement only that first slice.
8. Validate the change.
9. Update memory.

## Rules

- Do not build the whole app in one pass.
- Do not create unnecessary abstractions.
- Prefer a working thin slice over broad scaffolding.
- Mark anything unverified.

## Required updates before stopping

- `.ai/project-brief.md`
- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/architecture.md`
- `.ai/decisions.md` if decisions were made
- `.ai/graph-memory.md`
- `.ai/agent-handoff.md`

