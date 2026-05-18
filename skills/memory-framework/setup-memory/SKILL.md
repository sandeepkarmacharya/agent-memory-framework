---
name: setup-memory
description: Initialize the Agent Memory Framework in a repository and make sure all memory files are usable. Use when the user asks to set up repo memory, install the framework, or prepare a project for multi-agent work.
---


# Setup Memory

## Goal

Initialize or repair the repo-based memory framework so future agents can continue the project without relying on chat history.

## CLI

The `scripts/agent-memory` CLI handles initialization. Use it when possible.

```
python scripts/agent-memory init    # Create missing .ai/ files
python scripts/agent-memory validate  # Verify integrity
```

## Workflow

1. Read `README.md` and `AGENTS.md`.
2. Run `python scripts/agent-memory init` to create or repair all memory files.
3. Run `python scripts/agent-memory validate` to confirm everything is in place.
4. Inspect the project and fill obvious project-specific details.
5. Do not invent facts. Mark unknowns as `TBD`.
6. End by summarizing:
   - Files checked or created
   - Missing details the human should provide
   - `git config core.hooksPath .githooks` if not yet enabled
   - Recommended first command

## Required updates

- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`

