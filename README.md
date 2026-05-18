# Agent Memory Framework

**Repo-based persistent memory for AI agents.** Zero context loss across sessions, models, and tools.

AI agents forget everything when the session ends. Switching agents means starting over. This framework stores project memory in `.ai/` files inside your repo — any agent reads the same files, continues the same project, respects the same decisions. No chat history dependency.

## Features

- **13 memory file types** — state, decisions, tasks, architecture, bugs, deps, test results, security, API contracts, shared language, more
- **Structured YAML graph memory** — machine-readable relationship maps between features, files, APIs, data, bugs
- **Context pack generator** — `context "<task>"` returns continuity files + ranked relevant memory within an approximate token budget
- **BM25 retrieval layer** — ranked full-text search across memory files; agents query specific context instead of reading everything (saves ~50-80% token overhead)
- **Repo importer** — bootstrap `.ai/` from any existing project by scanning source code, dependencies, and structure
- **CLI tool** — `install`, `init`, `validate`, `optimize`, `compress`, `context`, `finish`, `index`, `query`, `search`, `import`, `suggest`
- **13 slash-command skills** — `/new`, `/continue`, `/handoff`, `/debug`, `/feature`, `/review`, etc.
- **Pre-commit hook** — automatic memory validation + index rebuild before every `git commit`
- **Git-aware suggestions** — `suggest` command analyzes recent changes and proposes memory updates
- **Caveman mode** — terse communication saves ~75% token usage
- **IDE integration** — `CLAUDE.md`, `.cursorrules`, `.codex/AGENTS.md`, and `HERMES.md` generated for zero-config agent onboarding
- **Agent-agnostic** — works with Claude Code, Cursor, Continue, opencode, Hermes Agent, and any tool that reads repo files

## Quick Start

### 1. Install the framework in your repo

#### One-line setup

Run this from the root of any app/project repo:

```bash
curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | bash
```

Installs into the current project by default. The bootstrapper clones the framework to a temporary directory, runs `install` for new projects, and automatically runs `upgrade` when `.ai/` or `scripts/agent-memory` already exists.

Optional target directory:

```bash
curl -fsSL https://raw.githubusercontent.com/sandeepkarmacharya/agent-memory-framework/main/install.sh | AGENT_MEMORY_TARGET=/path/to/your/project bash
```

Manual install from a local clone still works:

```bash
python scripts/agent-memory install --target /path/to/your/project
python scripts/agent-memory install --target .
```

This copies `AGENTS.md`, agent hook files (`CLAUDE.md`, `.cursorrules`, `.codex/AGENTS.md`, `HERMES.md`), `scripts/agent-memory`, the retrieval package, `.ai/` templates, and `.githooks/pre-commit` into the target project. Existing project files are preserved. If the target is a Git repo, the installer enables `core.hooksPath = .githooks` automatically.

### 2. Start working with your agent

```bash
python scripts/agent-memory context "<task>"
```

Agents should use the context pack first, then read only the files listed under `Files To Read Fully`.

### 3. Finish work and update memory

```bash
python scripts/agent-memory finish --summary "fixed auth bug" --next "add regression tests"
```

This updates handoff/current-state/task-board and rebuilds the retrieval index. The user does not need to memorize slash commands; repo-level `AGENTS.md` and generated agent hook files tell agents to run `context`, `finish`, and periodic `optimize --apply` maintenance automatically.

## Memory Files

All stored in `.ai/`. The CLI creates templates with real-world examples for every file.

| File | Purpose | Update When |
|---|---|---|
| `project-brief.md` | Goals, audience, scope, constraints | Project scope changes |
| `current-state.md` | What's built, broken, blocked, next | Any progress happens |
| `decisions.md` | Important product/architecture choices | Choices change |
| `task-board.md` | Tasks: next, in-progress, backlog, done | Tasks change state |
| `architecture.md` | Structure, data flow, APIs, deployment | Architecture changes |
| `coding-standards.md` | Code rules for agents and humans | Standards change |
| `bugs-and-fixes.md` | Bug log with root causes and fixes | Bugs found or fixed |
| `agent-handoff.md` | Session summary for next agent | Before stopping/switch |
| `graph-memory.yaml` | **Structured** relationship map | Dependencies change |
| `shared-language.md` | Domain terms and naming conventions | New terms emerge |
| `memory-index.md` | Read priority and update rules | — (stable reference) |
| `test-results.md` | Test suite results and coverage | Tests pass or fail |
| `dependencies.md` | Runtime, dev, and system dependencies | Deps added or changed |
| `security.md` | Threat model, audits, vulnerabilities | Security changes |
| `api-contracts.md` | API routes, schemas, auth requirements | API surface changes |
| `performance.md` | Benchmarks and profiles | Benchmarks run |
| `data-migrations.md` | Migration history and rollback plans | Migrations occur |
| `prompts.md` | Reusable prompts for agents without slash commands | New prompts created |
| `session-log.md` | Human-readable chronological notes | Useful to document |

### Why YAML for graph memory?

The old `graph-memory.md` was plain text — agents parsed it inconsistently and couldn't query relationships reliably. The new `graph-memory.yaml` is machine-readable:
- JSON-friendly (YAML is a superset)
- Agents can query specific relationships without regex
- Diff-compatible (git sees exact field changes)
- Can be used programmatically by other tools

## CLI Reference

```bash
python scripts/agent-memory install --target ../my-project  # Drop-in setup for another project
python scripts/agent-memory upgrade --target ../my-project  # Refresh managed hooks/CLI safely
python scripts/agent-memory init        # Initialize .ai/ files (safe to re-run)
python scripts/agent-memory validate    # Check all files exist and have content
python scripts/agent-memory doctor      # One-command setup/memory/index/hook health check
python scripts/agent-memory optimize    # Report bloat/stale index; add --apply to fix safe issues
python scripts/agent-memory compress    # Compress bloated memory files
python scripts/agent-memory context "fix auth bug" --budget 4000  # Compact context pack for a task
python scripts/agent-memory finish --summary "fixed auth bug" --next "add regression tests"  # Update memory after work
python scripts/agent-memory index       # Build BM25 search index for retrieval
python scripts/agent-memory query "..." # Ranked full-text search across memory
python scripts/agent-memory search ...  # Find which files contain a term
python scripts/agent-memory import ...  # Bootstrap .ai/ from existing project
python scripts/agent-memory suggest     # Propose memory updates from git diff
```

### `install`

Installs the framework into another project in one command:

```bash
python scripts/agent-memory install --target ../my-project
```

Behavior:
- Creates the target directory if needed
- Copies `AGENTS.md` only when missing; never overwrites existing project instructions
- Creates agent hook files for Claude, Cursor, Codex, and Hermes so agents auto-run `context`, `finish`, and periodic `optimize --apply` maintenance
- Creates `.ai/` memory templates
- Copies `scripts/agent-memory` and `scripts/memory_query/`
- Creates `.githooks/pre-commit`
- Enables `git config core.hooksPath .githooks` when the target is a Git repo

Use this for existing app projects. Use `init` only inside a repo that already has this CLI and `AGENTS.md`.

### `upgrade`

Refreshes managed framework files in an already-installed project without overwriting custom instructions:

```bash
python scripts/agent-memory upgrade --target ../my-project
```

Behavior:
- Adds missing `.ai/` templates but preserves existing memory files
- Refreshes `scripts/agent-memory` and `scripts/memory_query/`
- Creates missing agent hook files
- Appends or replaces only the marked Agent Memory managed block in `CLAUDE.md`, `.cursorrules`, `.codex/AGENTS.md`, and `HERMES.md`
- Preserves custom content outside `<!-- agent-memory:managed:start -->` / `<!-- agent-memory:managed:end -->`
- Creates missing pre-commit hook and enables `core.hooksPath` when possible

Use this after pulling a newer framework version into projects that already have custom agent instructions.

### `init`

Creates any missing `.ai/` files from templates. Safe to run on existing projects — existing files are never overwritten.
- Creates all 14+ memory files with example content
- Creates `.githooks/pre-commit` hook script
- Also creates optional recommended files (performance, data-migrations, prompts, session-log)

### `validate`

Checks required and recommended files:
- Verifies `AGENTS.md` exists and is non-empty
- Checks all required `.ai/` files exist and have been filled in (warns on unchanged templates)
- Reports missing recommended files
- Checks skill directory completeness
- Reports pre-commit hook status

### `doctor`

Runs one health check for setup, memory, retrieval, hooks, and optimization state:

```bash
python scripts/agent-memory doctor
python scripts/agent-memory doctor --max-bytes 8000
```

Behavior:
- Checks `AGENTS.md`, installed CLI, required `.ai/` files, and template placeholders
- Reports stale/missing BM25 index
- Reports memory files above bloat threshold
- Reports pre-commit hook presence and Git hook enablement
- Prints actionable next commands such as `init`, `index`, `optimize --apply`, or hook setup

Use this as the default support command when a project feels stale or misconfigured.

### `optimize`

Reports memory bloat and stale/missing retrieval index without changing files:

```bash
python scripts/agent-memory optimize
```

Apply safe cleanup:

```bash
python scripts/agent-memory optimize --apply
```

Behavior:
- Scans `.ai/*.md` and `.ai/*.yaml`
- Flags files above `--max-bytes` threshold
- Detects stale or missing `.ai/.memory_index/index.json`
- With `--apply`, deduplicates repeated long lines, collapses extra blank lines, and rebuilds the BM25 index

### `compress`

Reduces bloat in memory files without losing important context:
- Collapses repeated empty lines
- Deduplicates exact repeated lines (longer than 20 chars)
- Skips files that are already compact (under 50 bytes)

For deeper compression, use the `/compress-memory` skill which intelligently preserves decisions, active tasks, and unresolved bugs.

### `context`

Builds a compact context pack for a specific task so agents do not need to read every `.ai/` file:

```bash
python scripts/agent-memory context "fix auth redirect bug"
python scripts/agent-memory context "add billing webhook" --top-k 2 --budget 2000
```

The context pack includes:
- Always-useful continuity files: `agent-handoff.md`, `current-state.md`, `task-board.md`
- Ranked relevant memory from the BM25 index
- A `Files To Read Fully` list for deeper follow-up
- Approximate token-budget truncation for large memory files

### `finish`

Updates core memory at the end of a task:

```bash
python scripts/agent-memory finish --summary "fixed auth redirect bug" --next "add regression tests"
```

This command:
- Appends a finish section to `.ai/agent-handoff.md`
- Appends latest progress to `.ai/current-state.md`
- Appends done/next task entries to `.ai/task-board.md`
- Records changed and untracked files from Git
- Rebuilds the BM25 memory index

### `index`

Builds a BM25 search index over all `.ai/` files for fast retrieval:

```
python scripts/agent-memory index
```

The index is cached at `.ai/.memory_index/index.json` and auto-rebuilds on:
- `git commit` (via pre-commit hook)
- First `query` call after files change

Zero external dependencies — BM25 is implemented in pure Python.

### `query`

**Ranked full-text search** across all indexed memory files. This is the retrieval layer:

```
python scripts/agent-memory query "database schema config"
python scripts/agent-memory query "error handling auth middleware" -k 3
```

Returns ranked results with relevance scores and context snippets. Use this to:
- Find relevant context without reading every `.ai/` file
- Quickly onboard onto a project: `query "architecture goals decisions"`
- Debug: `query "bug error caching timeout"` → finds bugs-and-fixes.md matches

### `search`

Grep-like search that returns files containing a term, sorted by match count:

```
python scripts/agent-memory search "migration"
```

Useful for finding which specific files to read on a topic.

### `import`

Bootstrap `.ai/` memory files from an existing project that doesn't use the framework yet:

```
python scripts/agent-memory import ../other-project
```

Auto-detects:
- Languages and frameworks (Python, JS/TS, Go, Rust, etc.)
- Build/CI tools (Docker, GitHub Actions, Make, etc.)
- Dependencies (from requirements.txt, package.json, etc.)
- Project structure (directory tree up to 3 levels deep)
- Test files and configurations

Generates: `project-brief.md`, `current-state.md`, `architecture.md`, `dependencies.md`, `task-board.md`

After import, run `agent-memory init` and `agent-memory validate` to complete setup with remaining memory files.

### `suggest`

Analyzes recent git changes and proposes memory updates:

```
python scripts/agent-memory suggest
```

If you modified source files, it suggests updating `current-state.md`, `task-board.md`, and `agent-handoff.md`. If you modified config files, it flags `dependencies.md` for review. If it detects potential credential exposure in changed files, it issues a **CRITICAL** alert for `security.md`.

## Slash Commands

| Command | Action | When to Use |
|---|---|---|
| `/setup-memory` | Initialize/repair memory files | First time setup |
| `/new` | Start new project with full memory | Blank repo |
| `/continue` | Resume from memory | Returning to project |
| `/handoff` | Prepare for agent switch | Ending session |
| `/update-memory` | Sync memory with code changes | After meaningful work |
| `/compress-memory` | Shrink bloated memory files | Files too long |
| `/debug` | Disciplined bug diagnosis | Bug reported |
| `/feature` | Add feature as vertical slice | New feature |
| `/review` | Code/architecture review | Quality check |
| `/graphify` | Update dependency relationships | Relationships unclear |
| `/status` | Current state summary | "Where are we?" |
| `/architecture` | Improve system design | Structure needs work |
| `/sync-decisions` | Align decisions with code | Decisions stale |

## Agent Compatibility

Works with **any** AI coding agent that can read repo files and follow instructions.

### Claude Code
`CLAUDE.md` is generated in the repo root. Claude Code reads it automatically and runs `context` before work plus `finish` after meaningful work.

### Cursor
`.cursorrules` is generated in the repo root. Cursor loads it automatically when you open the project and follows the same memory workflow.

### Codex
`.codex/AGENTS.md` is generated with the same auto-hook workflow for Codex-specific project instructions.

### Hermes Agent
`HERMES.md` is generated with the same auto-hook workflow. `AGENTS.md` remains the general entry point.

### Other Agents (Continue, opencode, etc.)
The agent reads `AGENTS.md` → runs `context` → reads only selected `.ai/` memory files → does work → runs `finish`. The `prompts.md` file contains reusable prompts for agents that don't support skill loading.

## How It Works

```
Agent starts
  -> reads agent hook file (AGENTS.md / CLAUDE.md / .cursorrules / .codex/AGENTS.md / HERMES.md)
  -> runs: python scripts/agent-memory context "<task>"
  -> reads only context pack + listed files
  -> does work
  -> runs: python scripts/agent-memory finish --summary "<done>" --next "<next>"
  -> updates core .ai/ files and retrieval index
```

Next agent — same or different model/tool — picks up exactly where the previous one left off. **Zero chat history needed.**

## File structure in any project

```
your-repo/
  AGENTS.md               <- General agent entry point
  CLAUDE.md               <- Claude Code auto-hooks
  .cursorrules            <- Cursor auto-hooks
  HERMES.md               <- Hermes Agent auto-hooks
  .codex/
    AGENTS.md             <- Codex auto-hooks
  .githooks/
    pre-commit             <- Validation hook
  .ai/
    agent-handoff.md       <- Session handoff
    current-state.md       <- What's built/broken/next
    decisions.md           <- Important choices
    task-board.md          <- Task tracking
    architecture.md        <- System design
    graph-memory.yaml      <- Relationship map (structured)
    bugs-and-fixes.md      <- Bug log
    test-results.md        <- Test suite status
    dependencies.md        <- Dependency inventory
    security.md            <- Threat model & audits
    api-contracts.md       <- API surface
    coding-standards.md    <- Code rules
    shared-language.md     <- Domain terms
    project-brief.md       <- Project goals
    memory-index.md        <- File guide
    performance.md         <- Benchmarks (optional)
    data-migrations.md     <- Migration history (optional)
    prompts.md             <- Reusable prompts (optional)
    session-log.md         <- Chronological notes (optional)
  scripts/
    agent-memory           <- CLI tool
  skills/
    memory-framework/
      setup-memory/SKILL.md
      new/SKILL.md
      continue/SKILL.md
      handoff/SKILL.md
      update-memory/SKILL.md
      compress-memory/SKILL.md
      debug/SKILL.md
      feature/SKILL.md
      review/SKILL.md
      graphify/SKILL.md
      status/SKILL.md
      architecture/SKILL.md
      sync-decisions/SKILL.md
```

## Operating Principles

1. **Never start from scratch** — read memory first
2. **Smallest useful change** — vertical slices, not rewrites
3. **Test or validate** — mark unverified work explicitly
4. **Update memory** — after every meaningful task
5. **No secrets** — never store credentials in `.ai/`
6. **Caveman communication** — compressed, accurate, no filler

## Caveman Mode

All agent communication and memory files use a compressed, factual style:

- Drop filler words, articles, pleasantries
- Keep full technical accuracy
- Compress to ~25% of normal token usage
- Bullet points over paragraphs
- No "I think", "it seems", "please note" — just state facts
- Agent responses: answer directly, no preamble, no summary unless asked

Applies to: `.ai/` files, agent responses, code comments, task descriptions, decision records.

Does **not** apply to: user-facing docs, public README sections explaining the framework.

## Task Completion Standard

A task is not done until:

1. Work completed or blocker explained
2. Change validated (test or manual check)
3. Memory files updated
4. Handoff written for next agent

## License

MIT
