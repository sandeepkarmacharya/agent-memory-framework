# Agent Memory Framework

Repo-based memory system for AI agents. Zero context loss across sessions, models, tools.

## Problem

AI agents forget everything when session ends. Switching agent = starting over. Chat history is unreliable memory. Token waste repeating same context.

## Solution

Store project memory in `.ai/` folder inside repo. Any agent reads same files, continues same project, respects same decisions. No chat history dependency.

## Why Caveman Style

This framework uses **caveman communication** — compressed, no filler, no pleasantries, full technical accuracy. Benefits:

- **Token savings**: ~75% fewer tokens per conversation
- **Faster reads**: Agents parse memory files quickly
- **Less noise**: Only actionable info survives
- **Consistent memory**: Compressed format = smaller `.ai/` files = faster context loading

All memory files, handoffs, and agent interactions favor brevity over verbosity.

## Quick Start

### 1. Install

Copy these into your repo root:

```
AGENTS.md          -> Agent instructions (required entry point)
skills/            -> Skill definitions (13 slash commands)
```

### 2. Initialize

```
/setup-memory
```

Creates `.ai/` folder with all memory files.

### 3. Build

```
/new               -> Start new project
/continue          -> Resume existing project
/feature           -> Add feature
```

### 4. Maintain

```
/update-memory     -> After meaningful work
/handoff           -> Before switching agents
/status            -> Check current state
```

## Memory Files

All stored in `.ai/` folder:

| File | Purpose | Update when |
|---|---|---|
| `project-brief.md` | Goals, audience, scope, constraints | Project scope changes |
| `current-state.md` | What's built, broken, blocked, next | Any progress happens |
| `decisions.md` | Important product/architecture choices | Choices change |
| `task-board.md` | Tasks: next, in-progress, backlog, done | Tasks change state |
| `architecture.md` | Structure, data flow, APIs, deployment | Architecture changes |
| `coding-standards.md` | Code rules for agents and humans | Standards change |
| `bugs-and-fixes.md` | Bug log: symptoms, causes, fixes, risks | Bugs found or fixed |
| `agent-handoff.md` | Session summary for next agent | Before stopping |
| `graph-memory.md` | Relationship map: features, files, APIs, data | Dependencies change |
| `shared-language.md` | Domain terms and naming conventions | New terms emerge |
| `memory-index.md` | Read priority and update rules | File purposes change |

## Slash Commands

| Command | Action | When to use |
|---|---|---|
| `/setup-memory` | Initialize/repair memory files | First time setup |
| `/new` | Start new project | Blank repo |
| `/continue` | Resume from memory | Returning to project |
| `/handoff` | Prepare for agent switch | Ending session |
| `/update-memory` | Sync memory with code changes | After meaningful work |
| `/compress-memory` | Shrink bloated memory files | Files too long/repetitive |
| `/debug` | Disciplined bug diagnosis | Bug reported |
| `/feature` | Add feature as vertical slice | New feature requested |
| `/review` | Code/architecture review | Quality check needed |
| `/graphify` | Update dependency graph | Relationships unclear |
| `/status` | Current state summary | "Where are we?" |
| `/architecture` | Improve system design | Structure needs work |
| `/sync-decisions` | Align decisions with code | Decisions stale |

## How It Works

```
Agent starts
  -> reads AGENTS.md
  -> reads .ai/ memory files
  -> understands full project context
  -> does work
  -> updates .ai/ files
  -> writes handoff for next agent
```

Next agent (same or different model/tool) picks up exactly where previous left off. Zero chat history needed.

## Operating Principles

1. **Never start from scratch** — read memory first
2. **Smallest useful change** — vertical slices, not rewrites
3. **Test or validate** — mark unverified work as unverified
4. **Update memory** — after every meaningful task
5. **No secrets** — never store credentials in `.ai/`
6. **Caveman communication** — compressed, accurate, no filler

## Folder Structure

```
your-repo/
  AGENTS.md              <- Agent entry point
  .ai/
    agent-handoff.md     <- Session handoff
    current-state.md     <- What's built/broken/next
    decisions.md         <- Important choices
    task-board.md        <- Task tracking
    architecture.md      <- System design
    graph-memory.md      <- Relationship map
    bugs-and-fixes.md    <- Bug log
    coding-standards.md  <- Code rules
    shared-language.md   <- Domain terms
    memory-index.md      <- File guide
    project-brief.md     <- Project goals
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

## Agent Compatibility

Works with any AI coding agent that can:
- Read files from repo
- Follow instructions in `AGENTS.md`
- Execute slash commands or load skill files

Tested with: Claude Code, Cursor, Continue, opencode, and similar tools.

## Task Completion Standard

Task not done until:

1. Work completed or blocker explained
2. Change validated (test or manual check)
3. Memory files updated
4. Handoff written for next agent
