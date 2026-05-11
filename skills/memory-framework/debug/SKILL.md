---
name: debug
description: Debug a project using a disciplined memory-aware diagnosis loop. Use when the user reports a bug, failing test, regression, performance issue, or unexpected behavior.
---


# Debug

## Goal

Fix bugs without random changes or context loss.

## Read first

1. `AGENTS.md`
2. `.ai/current-state.md`
3. `.ai/bugs-and-fixes.md`
4. `.ai/architecture.md`
5. `.ai/graph-memory.md`
6. `.ai/agent-handoff.md`

## Workflow

1. Reproduce or characterize the issue.
2. Identify affected feature, files, APIs, and data using `.ai/graph-memory.md`.
3. Form a specific hypothesis.
4. Inspect the smallest relevant area.
5. Apply the smallest safe fix.
6. Validate with a test or manual check.
7. Record the root cause and fix.

## Rules

- Do not apply random fixes.
- Do not rewrite unrelated code.
- Do not claim success without validation.
- If validation is impossible, say what remains unverified.

## Required updates

- `.ai/bugs-and-fixes.md`
- `.ai/current-state.md`
- `.ai/agent-handoff.md`
- `.ai/graph-memory.md`
- `.ai/task-board.md` if new work is discovered

