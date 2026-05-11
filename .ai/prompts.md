# Reusable Prompts

Use these prompts when your agent does not support slash commands or skill loading.

## Continue project

```txt
Read AGENTS.md and all relevant files in .ai/, especially agent-handoff, current-state, task-board, decisions, architecture, graph-memory, and bugs-and-fixes. Summarize the current state, identify the next best task, complete the smallest safe step, validate it, and update memory before stopping. Do not start from scratch.
```

## Prepare handoff

```txt
Prepare this project for another AI agent. Update .ai/agent-handoff.md with session summary, completed work, changed files, decisions, bugs, current status, next task, commands run, validation status, warnings, and things not to redo. Also update current-state, task-board, graph-memory, bugs-and-fixes, and decisions as needed.
```

## Update memory

```txt
Review the work completed in this session and update .ai/current-state.md, .ai/task-board.md, .ai/agent-handoff.md, .ai/graph-memory.md, .ai/bugs-and-fixes.md, and .ai/decisions.md where relevant. Preserve useful existing information and only update what changed.
```

## Debug

```txt
Debug this project using the memory framework. Read AGENTS.md, current-state, bugs-and-fixes, architecture, graph-memory, and agent-handoff. Reproduce or characterize the issue, identify likely root cause, make the smallest safe fix, validate it, and update bug memory plus handoff.
```
