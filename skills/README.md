# Memory Framework Skills

Each folder contains one reusable skill for an AI agent. In tools that support slash commands or skills, use the slash-style name. In tools that do not, paste the matching `SKILL.md` content into the agent's instructions.

## Skills

| Slash | Folder | Use when |
|---|---|---|
| `/setup-memory` | `setup-memory` | Installing or initializing the framework |
| `/new` | `new` | Starting a brand-new project |
| `/continue` | `continue` | Continuing an existing project |
| `/handoff` | `handoff` | Switching agents or ending a session |
| `/update-memory` | `update-memory` | After meaningful work |
| `/compress-memory` | `compress-memory` | Memory files are too long or duplicated |
| `/debug` | `debug` | Investigating bugs or regressions |
| `/feature` | `feature` | Adding a feature |
| `/review` | `review` | Reviewing quality and architecture |
| `/graphify` | `graphify` | Updating relationship memory |
| `/status` | `status` | Getting a current state summary |
| `/architecture` | `architecture` | Improving system design |
| `/sync-decisions` | `sync-decisions` | Aligning decisions with current code |

## CLI

The `scripts/agent-memory` Python CLI provides three commands that complement these skills:

- `python scripts/agent-memory init` — automated `.ai/` file creation (instead of `/setup-memory`)
- `python scripts/agent-memory validate` — integrity check
- `python scripts/agent-memory compress` — basic file compression (pre-step before `/compress-memory`)

## Rule

Every skill should leave the repository easier for the next agent to understand.
