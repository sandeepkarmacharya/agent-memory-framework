---
name: graphify
description: Update graph-style project memory that maps relationships between features, files, APIs, data, bugs, and decisions. Use when dependencies are unclear or after significant code changes.
---


# Graphify

## Goal

Create or refresh a useful relationship map for future agents.

## Read first

1. `.ai/architecture.md`
2. `.ai/current-state.md`
3. `.ai/decisions.md`
4. `.ai/bugs-and-fixes.md`
5. Existing `.ai/graph-memory.md`

## Workflow

Update `.ai/graph-memory.md` with these sections:

1. Feature graph
2. File graph
3. API graph
4. Data graph
5. Bug graph
6. Decision graph

For each item, include only useful relationships:

- Depends on
- Used by
- Related files
- Related APIs
- Related data
- Related decisions
- Known risks

## Rules

- Do not invent relationships.
- Do not list every file if it does not help.
- Keep it readable.
- Remove relationships that are clearly outdated.

## Required updates

- `.ai/graph-memory.md`
- `.ai/agent-handoff.md`

