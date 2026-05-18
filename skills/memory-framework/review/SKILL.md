---
name: review
description: Review a codebase using memory-aware engineering checks. Use when the user asks for code review, architecture review, security review, quality review, or readiness check.
---


# Review

## Goal

Find meaningful issues without rewriting the project.

## Read first

1. `AGENTS.md`
2. `.ai/project-brief.md`
3. `.ai/architecture.md`
4. `.ai/coding-standards.md`
5. `.ai/decisions.md`
6. `.ai/current-state.md`
7. `.ai/graph-memory.yaml`

## Review checklist

Look for:

1. Security and privacy issues
2. Broken architecture boundaries
3. Over-engineering
4. Missing error handling
5. Bad state management
6. Duplicated logic
7. Performance risks
8. Testing gaps
9. Accessibility issues
10. Files or modules that are too large
11. Inconsistency with recorded decisions

## Output

Return:

1. Critical issues
2. Important issues
3. Nice-to-have improvements
4. Recommended next fixes in priority order

## Required updates

- `.ai/bugs-and-fixes.md` for confirmed bugs
- `.ai/task-board.md` for recommended fixes
- `.ai/agent-handoff.md` with review summary
- `.ai/graph-memory.yaml` if relationships are discovered

