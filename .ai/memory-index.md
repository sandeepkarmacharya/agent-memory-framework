# Memory Index

## Read priority

### Always read first

1. `AGENTS.md`
2. `.ai/agent-handoff.md`
3. `.ai/current-state.md`
4. `.ai/task-board.md`
5. `.ai/decisions.md`

### Read when relevant

- `.ai/architecture.md` — before architecture, feature, API, database, or refactor work
- `.ai/coding-standards.md` — before coding or review
- `.ai/bugs-and-fixes.md` — before debugging or touching fragile areas
- `.ai/graph-memory.md` — before tracing dependencies or switching agents
- `.ai/shared-language.md` — before naming concepts or explaining domain logic
- `.ai/prompts.md` — when slash skills are unavailable
- `.ai/session-log.md` — when chronological history is needed

## Update rules

| File | Update when |
|---|---|
| `project-brief.md` | Project goals, audience, scope, or constraints change |
| `current-state.md` | Any meaningful implementation progress happens |
| `decisions.md` | Product, architecture, API, database, pricing, or security choices change |
| `task-board.md` | Tasks are added, started, blocked, or completed |
| `architecture.md` | Structure, data flow, dependencies, APIs, or deployment changes |
| `coding-standards.md` | Team or agent coding rules change |
| `bugs-and-fixes.md` | Bugs are found, investigated, fixed, or deferred |
| `agent-handoff.md` | Before stopping or switching agents |
| `graph-memory.md` | Relationships between features/files/APIs/data/bugs change |
| `shared-language.md` | New domain terms appear |
| `prompts.md` | New reusable prompt is added |
| `session-log.md` | Human-readable chronological note is useful |

## Memory hygiene

- Keep current files current.
- Archive or compress stale details.
- Do not duplicate large sections across files.
- Do not store secrets.
