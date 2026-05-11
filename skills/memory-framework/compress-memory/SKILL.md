---
name: compress-memory
description: Compress bloated project memory without losing important context. Use when .ai files become repetitive, outdated, or too long for agents to read efficiently.
---


# Compress Memory

## Goal

Reduce memory bloat while preserving important context.

## Workflow

1. Read every file in `.ai/`.
2. Remove duplicate information.
3. Preserve:
   - Current state
   - Active decisions
   - Known bugs
   - Active tasks
   - Architecture that is still true
   - Useful graph relationships
   - Current handoff
4. Move old but useful details into an `Archived / Historical Notes` section only if needed.
5. Delete stale details only when clearly superseded.
6. Update `.ai/memory-index.md` if file purpose or read order changed.
7. Make `.ai/agent-handoff.md` short and immediately useful.

## Rules

- Do not delete unresolved bugs.
- Do not delete active decisions.
- Do not hide uncertainty.
- Do not compress so aggressively that the next agent loses context.

## End with

1. What was compressed
2. What was preserved
3. What the next agent should read first

