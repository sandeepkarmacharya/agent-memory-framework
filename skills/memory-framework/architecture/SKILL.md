---
name: architecture
description: Review or improve project architecture using repo memory. Use when the user asks about architecture, structure, refactoring, system design, scalability, or maintainability.
---


# Architecture

## Goal

Improve system design without creating a ball of mud.

## Read first

1. `AGENTS.md`
2. `.ai/project-brief.md`
3. `.ai/architecture.md`
4. `.ai/decisions.md`
5. `.ai/graph-memory.md`
6. `.ai/coding-standards.md`
7. `.ai/current-state.md`

## Workflow

1. Summarize the current architecture.
2. Identify boundaries and responsibilities.
3. Identify coupling, duplication, fragile areas, and missing interfaces.
4. Recommend minimal architecture improvements.
5. If implementing, make one small refactor at a time.
6. Validate behavior remains unchanged.
7. Record decisions and graph changes.

## Rules

- Do not rewrite the whole app.
- Do not change behavior during pure refactor unless explicitly requested.
- Prefer deep modules with small external interfaces.
- Keep terminology aligned with `.ai/shared-language.md`.

## Required updates

- `.ai/architecture.md`
- `.ai/decisions.md` if decisions are made
- `.ai/graph-memory.md`
- `.ai/current-state.md`
- `.ai/agent-handoff.md`

