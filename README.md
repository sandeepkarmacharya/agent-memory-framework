# Agent Memory Framework

**Repo-based persistent memory for AI agents.** Zero context loss across sessions, models, and tools.

AI agents forget everything when the session ends. Switching agents means starting over. This framework stores project memory in `.ai/` files inside your repo — any agent reads the same files, continues the same project, respects the same decisions. No chat history dependency.

## Features

- **13 memory file types** — state, decisions, tasks, architecture, bugs, deps, test results, security, API contracts, shared language, more
- **Structured YAML graph memory** — machine-readable relationship maps between features, files, APIs, data, bugs
- **BM25 retrieval layer** — ranked full-text search across memory files; agents query specific context instead of reading everything (saves ~50-80% token overhead)
- **Repo importer** — bootstrap `.ai/` from any existing project by scanning source code, dependencies, and structure
- **CLI tool** — `init`, `validate`, `compress`, `index`, `query`, `search`, `import`, `suggest`
- **13 slash-command skills** — `/new`, `/continue`, `/handoff`, `/debug`, `/feature`, `/review`, etc.
- **Pre-commit hook** — automatic memory validation + index rebuild before every `git commit`
- **Git-aware suggestions** — `suggest` command analyzes recent changes and proposes memory updates
- **Caveman mode** — terse communication saves ~75% token usage
- **IDE integration** — `claude.md` and `.cursorrules` included for zero-config agent onboarding
- **Agent-agnostic** — works with Claude Code, Cursor, Continue, opencode, Hermes Agent, and any tool that reads repo files

## Quick Start

### 1. Install the framework in your repo

```bash
# Copy these files to your repo root:
#   AGENTS.md            -> Agent instructions (required entry point)
#   scripts/agent-memory -> CLI tool
#   skills/              -> Skill definitions (13 slash commands)
#   claude.md            -> Claude Code integration
#   .cursorrules         -> Cursor integration
#   .githooks/           -> Pre-commit hook

# Or clone the template repo:
git clone https://github.com/sandeepkarmacharya/agent-memory-framework.git my-project
```

### 2. Initialize memory

```bash
python scripts/agent-memory init
```

This creates a full `.ai/` directory with all 14+ memory files, each containing templates with examples to guide you.

### 3. Enable the pre-commit hook

```bash
git config core.hooksPath .githooks
```

Now every commit runs `agent-memory validate` automatically. Commits with missing or empty memory files are blocked.

### 4. Start working with your agent

```
/new               -> Start a new project with memory
/continue          -> Resume an existing project
/feature           -> Add a new feature
/debug             -> Diagnose and fix a bug
```

If your agent doesn't support slash commands, paste the content of the matching skill file from `skills/memory-framework/`.

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
python scripts/agent-memory init        # Initialize .ai/ files (safe to re-run)
python scripts/agent-memory validate    # Check all files exist and have content
python scripts/agent-memory compress    # Deduplicate and compress bloated files
python scripts/agent-memory index       # Build BM25 search index for retrieval
python scripts/agent-memory query "..." # Ranked full-text search across memory
python scripts/agent-memory search ...  # Find which files contain a term
python scripts/agent-memory import ...  # Bootstrap .ai/ from existing project
python scripts/agent-memory suggest     # Propose memory updates from git diff
```

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

### `compress`

Reduces bloat in memory files without losing important context:
- Collapses repeated empty lines
- Deduplicates exact repeated lines (longer than 20 chars)
- Skips files that are already compact (under 50 bytes)

For deeper compression, use the `/compress-memory` skill which intelligently preserves decisions, active tasks, and unresolved bugs.

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
`claude.md` is provided in the repo root. Claude Code reads it automatically and follows the memory framework.

### Cursor
`.cursorrules` is provided in the repo root. Cursor loads it automatically when you open the project.

### Other Agents (Continue, opencode, Hermes Agent, etc.)
The agent reads `AGENTS.md` → loads `.ai/` memory files → executes slash commands via skills folder. The `prompts.md` file contains reusable prompts for agents that don't support skill loading.

## How It Works

```
Agent starts
  -> reads AGENTS.md
  -> reads .ai/ memory files (in priority order)
  -> understands full project context
  -> does work
  -> updates .ai/ files (current-state, task-board, handoff, etc.)
  -> writes handoff for next agent
```

Next agent — same or different model/tool — picks up exactly where the previous one left off. **Zero chat history needed.**

## File structure in any project

```
your-repo/
  AGENTS.md               <- Agent entry point (required)
  claude.md                <- Claude Code integration
  .cursorrules             <- Cursor integration
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
