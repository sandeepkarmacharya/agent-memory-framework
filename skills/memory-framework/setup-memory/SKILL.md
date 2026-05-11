---
name: setup-memory
description: Initialize the Agent Memory Framework in a repository and make sure all memory files are usable. Use when the user asks to set up repo memory, install the framework, or prepare a project for multi-agent work.
---


# Setup Memory

## Goal

Initialize or repair the repo-based memory framework so future agents can continue the project without relying on chat history.

## Workflow

1. Read `README.md` and `AGENTS.md`.
2. Check that these exist:
   - `.ai/project-brief.md`
   - `.ai/current-state.md`
   - `.ai/decisions.md`
   - `.ai/task-board.md`
   - `.ai/architecture.md`
   - `.ai/coding-standards.md`
   - `.ai/bugs-and-fixes.md`
   - `.ai/agent-handoff.md`
   - `.ai/memory-index.md`
   - `.ai/graph-memory.md`
   - `.ai/shared-language.md`
   - `.ai/prompts.md`
3. If any are missing, create them using the framework structure.
4. Inspect the project and fill obvious project-specific details.
5. Do not invent facts. Mark unknowns as `TBD`.
6. Run `python scripts/check-memory.py` if available.
7. End by summarizing:
   - Files checked or created
   - Missing details the human should provide
   - Recommended first command

## Required updates

- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`

