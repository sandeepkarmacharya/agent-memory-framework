---
name: handoff
description: Prepare a project for another AI agent by updating the latest handoff and related memory files. Use before switching agents, models, tools, or ending a session.
---


# Handoff

## Goal

Make the next agent productive without reading the full chat.

## Workflow

Update `.ai/agent-handoff.md` with:

1. Session summary
2. What was completed
3. Files created or changed
4. Decisions made
5. Bugs found
6. Bugs fixed
7. What remains incomplete
8. Current task status
9. Next recommended task
10. Commands run
11. Tests or checks performed
12. Tests still needed
13. Warnings for the next agent
14. Things the next agent should not redo
15. Suggested next prompt

Also update related memory files.

## Rules

- Be concise but complete.
- Do not hide uncertainty.
- Mark unverified work as unverified.
- Do not claim tests passed unless they actually ran.
- Use caveman style: terse, factual, no filler, no hedging.
- Bullet points over paragraphs. Short sentences.

## Required updates

- `.ai/agent-handoff.md`
- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/graph-memory.md` if relationships changed
- `.ai/bugs-and-fixes.md` if bugs were involved
- `.ai/decisions.md` if decisions changed

