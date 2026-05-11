# AGENTS.md

This repository uses the Agent Memory Framework. All AI agents must follow these instructions before making changes.

## First rule

Do not start from scratch unless the user explicitly asks for a reset.

Before doing any work, read the relevant memory files in `.ai/`. At minimum, read:

1. `.ai/agent-handoff.md`
2. `.ai/current-state.md`
3. `.ai/task-board.md`
4. `.ai/decisions.md`
5. `.ai/architecture.md`
6. `.ai/graph-memory.md`
7. `.ai/bugs-and-fixes.md`

For brand-new setup, also read:

1. `.ai/project-brief.md`
2. `.ai/coding-standards.md`
3. `.ai/shared-language.md`
4. `.ai/memory-index.md`

## Operating principles

- Preserve existing decisions unless there is a clear, documented reason to change them.
- Make the smallest useful change.
- Prefer vertical slices over large rewrites.
- Test or validate changes when possible.
- Mark unverified work as unverified.
- Do not store secrets, tokens, credentials, private keys, or personal sensitive data in `.ai/` files.
- Keep memory files useful, concise, and current.

## Caveman mode (always on)

All agent communication and memory files use caveman style:

- Drop filler words, articles, pleasantries
- Keep full technical accuracy
- Compress to ~25% of normal token usage
- Prefer short factual statements over paragraphs
- No "I think", "it seems", "please note" — just state facts
- Memory files: bullet points, tables, terse prose
- Agent responses: answer directly, no preamble, no summary unless asked

This applies to: `.ai/` file content, agent-handoff.md, agent responses, code comments (only when comments are needed), task descriptions, decision records.

Caveman does NOT apply to: user-facing docs the human controls, public README sections explaining the framework to new users.

## Required memory updates

After every meaningful task, update:

- `.ai/current-state.md`
- `.ai/task-board.md`
- `.ai/agent-handoff.md`
- `.ai/graph-memory.md` if relationships changed
- `.ai/bugs-and-fixes.md` if bugs were found, fixed, or investigated
- `.ai/decisions.md` if an important product or architecture decision was made

## Slash command mapping

If the user invokes a slash command, load the matching skill:

- `/setup-memory` -> `skills/memory-framework/setup-memory/SKILL.md`
- `/new` -> `skills/memory-framework/new/SKILL.md`
- `/continue` -> `skills/memory-framework/continue/SKILL.md`
- `/handoff` -> `skills/memory-framework/handoff/SKILL.md`
- `/update-memory` -> `skills/memory-framework/update-memory/SKILL.md`
- `/compress-memory` -> `skills/memory-framework/compress-memory/SKILL.md`
- `/debug` -> `skills/memory-framework/debug/SKILL.md`
- `/feature` -> `skills/memory-framework/feature/SKILL.md`
- `/review` -> `skills/memory-framework/review/SKILL.md`
- `/graphify` -> `skills/memory-framework/graphify/SKILL.md`
- `/status` -> `skills/memory-framework/status/SKILL.md`
- `/architecture` -> `skills/memory-framework/architecture/SKILL.md`
- `/sync-decisions` -> `skills/memory-framework/sync-decisions/SKILL.md`

## Completion standard

A task is not complete until:

1. The requested work is done or the blocker is clearly explained.
2. The change has been validated where possible.
3. The affected memory files are updated.
4. `.ai/agent-handoff.md` tells the next agent exactly what to do.
