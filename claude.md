# Claude.md — Agent Memory Framework

This project uses the Agent Memory Framework for persistent context.

## Required Setup

1. This repo has `.ai/` folder with structured memory files.
2. Run `python scripts/agent-memory init` if `.ai/` files are missing.
3. Read memory before every task.

## Read Order

Before any work, read in this order:
1. `.ai/agent-handoff.md`
2. `.ai/current-state.md`
3. `.ai/task-board.md`
4. `.ai/decisions.md`
5. `.ai/architecture.md`
6. `.ai/graph-memory.yaml`
7. `.ai/bugs-and-fixes.md`

## Update Rules

After every meaningful task:
- `.ai/current-state.md` — what changed
- `.ai/task-board.md` — task status
- `.ai/agent-handoff.md` — summary for next agent
- `.ai/graph-memory.yaml` — if relationships changed
- `.ai/bugs-and-fixes.md` — if bugs involved

## Caveman Mode

All agent communication and memory files use caveman style:
- Drop filler words, pleasantries, articles
- Preserve full technical accuracy
- Prefer bullet points over paragraphs
- No "I think", "it seems" — just state facts
- Compress to ~25% of normal tokens
- User-facing docs and README are exempt

## Commands

- `python scripts/agent-memory validate` — check memory integrity
- `python scripts/agent-memory init` — create missing files
- `python scripts/agent-memory compress` — reduce bloat
