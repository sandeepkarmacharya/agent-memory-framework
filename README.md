# Agent Memory Framework

Repo memory for AI coding agents. It keeps project context in `.ai/` files so Claude Code, Cursor, Codex, Hermes, opencode, Continue, and other agents can resume work without reading old chats.

Main goal: reduce token use while preserving long term project memory.

## Why use it

Agents lose context between sessions. This framework gives them a small, shared memory layer inside the repo:

- Start with `context "<task>"` instead of reading every file.
- Retrieve only relevant memory with a local BM25 index.
- Record handoff, state, decisions, tasks, bugs, tests, dependencies, security notes, and API contracts.
- Auto-update the retrieval index through `finish`, `index`, and the pre-commit hook.
- Keep agent instructions in repo files, so users do not need to remember command sequences.

If you are new, run the one-liner and then ask your agent to read `AGENTS.md`.

## Quick start

### One-line setup

Run this from the root of any app/project repo:

```bash
curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | bash
```

Installs into the current project by default. For another folder:

```bash
curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | AGENT_MEMORY_TARGET=/path/to/your/project bash
```

What the installer does:

- Uses `install` for new projects.
- Uses `upgrade` when `.ai/` or `scripts/agent-memory` already exists.
- Preserves existing project files and custom agent instructions.
- Enables `.githooks/pre-commit` when the target is a Git repo.

Manual install from a local clone:

```bash
python scripts/agent-memory install --target /path/to/your/project
python scripts/agent-memory install --target .
```

## Daily workflow

You do not need to memorize these commands. The generated `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.codex/AGENTS.md`, and `HERMES.md` tell agents when to run them.

If you are driving manually:

```bash
# 1. Before work: get compact task context
python scripts/agent-memory context "<task>"

# 2. Do the work with your agent

# 3. After meaningful work: update handoff/state/tasks and rebuild index
python scripts/agent-memory finish --summary "<what changed>" --next "<next task>"
```

When something feels stale or broken:

```bash
python scripts/agent-memory doctor
python scripts/agent-memory optimize --apply
```

## How it works

```text
Agent reads repo instructions
  -> runs context "<task>"
  -> reads compact context pack and selected memory files
  -> works on code/docs/tests
  -> runs finish --summary ... --next ...
  -> updates .ai/ memory and retrieval index
Next agent starts from the same repo memory
```

The important design choice: agents query memory first, then read full files only when the context pack says they are relevant. That is where the token savings come from.

## Command reference

| Command | Use it when | Example |
|---|---|---|
| `install` | Add framework to another project | `python scripts/agent-memory install --target ../app` |
| `upgrade` | Refresh CLI/hooks without overwriting custom instructions | `python scripts/agent-memory upgrade --target ../app` |
| `init` | Create missing `.ai/` templates in current repo | `python scripts/agent-memory init` |
| `context` | Build compact context for a task | `python scripts/agent-memory context "fix auth bug" --budget 4000` |
| `finish` | Save task result and next step | `python scripts/agent-memory finish --summary "fixed auth" --next "add tests"` |
| `query` | Search memory by relevance | `python scripts/agent-memory query "auth middleware errors" -k 3` |
| `search` | Find files containing a term | `python scripts/agent-memory search "migration"` |
| `index` | Rebuild retrieval index | `python scripts/agent-memory index` |
| `validate` | Check setup and required files | `python scripts/agent-memory validate` |
| `doctor` | Diagnose setup, memory, index, hooks | `python scripts/agent-memory doctor` |
| `optimize` | Detect or fix stale/bloated memory | `python scripts/agent-memory optimize --apply` |
| `compress` | Remove repeated lines/blank bloat | `python scripts/agent-memory compress` |
| `import` | Seed memory from an existing repo | `python scripts/agent-memory import ../old-project` |
| `suggest` | Propose memory updates from Git diff | `python scripts/agent-memory suggest` |

Advanced notes:

- `context` uses `agent-handoff.md`, `current-state.md`, `task-board.md`, and ranked BM25 results.
- `query` and `context` auto-refresh the index when memory files change.
- `finish` records changed/untracked Git files and rebuilds the index.
- `upgrade` only replaces content inside the managed agent-memory block in hook files.

## What gets installed

```text
your-repo/
  AGENTS.md                  general agent entry point
  CLAUDE.md                  Claude Code instructions
  .cursorrules               Cursor instructions
  .codex/AGENTS.md           Codex instructions
  HERMES.md                  Hermes instructions
  .githooks/pre-commit       validates memory and rebuilds index
  scripts/agent-memory       CLI
  scripts/memory_query/      local BM25 retrieval
  .ai/                       project memory
```

Existing `AGENTS.md` and custom hook files are preserved. On upgrade, managed blocks are appended or refreshed without deleting your own instructions.

## Memory files

All memory lives in `.ai/`.

| File | Purpose |
|---|---|
| `project-brief.md` | Goals, users, scope, constraints |
| `current-state.md` | Built, broken, in progress, next |
| `decisions.md` | Architecture/product decisions and rationale |
| `task-board.md` | Next, in progress, backlog, done |
| `architecture.md` | Structure, data flow, deployment |
| `coding-standards.md` | Rules agents should follow |
| `bugs-and-fixes.md` | Bugs, root causes, fixes, regression risk |
| `agent-handoff.md` | Session summary for the next agent |
| `graph-memory.yaml` | Machine-readable relationships between features, files, APIs, data, and bugs |
| `shared-language.md` | Domain terms and naming conventions |
| `memory-index.md` | Guide to what to read and when |
| `test-results.md` | Test runs, coverage, known gaps |
| `dependencies.md` | Runtime, dev, system dependencies |
| `security.md` | Threat model, audits, sensitive areas |
| `api-contracts.md` | Routes, schemas, auth rules |
| `performance.md` | Benchmarks and profiling notes |
| `data-migrations.md` | Migration history and rollback notes |
| `prompts.md` | Reusable prompts for agents without skill support |
| `session-log.md` | Optional chronological notes |

Required files are created during install. Recommended optional files are created by `init` and filled as the project grows.

## Agent support

Works with any agent that can read repo files.

| Agent/tool | File it reads |
|---|---|
| General agents, opencode, Continue | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Codex | `.codex/AGENTS.md` |
| Hermes Agent | `HERMES.md` and `AGENTS.md` |

The generated instructions tell agents to:

1. Run `python scripts/agent-memory context "<task>"` before work.
2. Read only the files listed in the context pack unless more detail is needed.
3. Run tests or validation when possible.
4. Run `python scripts/agent-memory finish --summary ... --next ...` after meaningful work.
5. Run `doctor` or `optimize --apply` when memory/index health looks stale.

## Troubleshooting

Run:

```bash
python scripts/agent-memory doctor
```

Common fixes:

| Problem | Fix |
|---|---|
| Missing `.ai/` files | `python scripts/agent-memory init` |
| Stale or missing index | `python scripts/agent-memory index` |
| Memory files too large | `python scripts/agent-memory optimize --apply` |
| Existing install needs latest hooks/CLI | `python scripts/agent-memory upgrade --target .` |
| Agent reads too much context | Start with `context "<task>"`, then read only listed files |
| Unsure what memory to update | `python scripts/agent-memory suggest` |

## Safety notes

- Do not store secrets, API keys, tokens, passwords, private certs, or customer data in `.ai/`.
- Keep memory factual and compact. Store durable project facts, not chat transcripts.
- Treat `security.md` as a pointer to sensitive areas and audit notes, not a place for raw credentials.
- Review `.ai/` changes like code. They affect future agent behavior.
- The one-line installer runs a shell script from GitHub. If you prefer to inspect first, open `install.sh`, then run it locally.

## Development

This repo uses GitHub Actions and local tests.

```bash
python -m pytest -q
python scripts/agent-memory validate
python scripts/agent-memory doctor
python scripts/agent-memory optimize
python scripts/agent-memory index
```

CI runs these checks on Python 3.11 and 3.12 for pushes and pull requests.

## License

MIT
