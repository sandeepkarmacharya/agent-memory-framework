#!/usr/bin/env python3
"""Validate the Agent Memory Framework files.

Run from the repository root:

    python scripts/check-memory.py
"""
from pathlib import Path
import sys

REQUIRED = [
    "AGENTS.md",
    ".ai/project-brief.md",
    ".ai/current-state.md",
    ".ai/decisions.md",
    ".ai/task-board.md",
    ".ai/architecture.md",
    ".ai/coding-standards.md",
    ".ai/bugs-and-fixes.md",
    ".ai/agent-handoff.md",
    ".ai/memory-index.md",
    ".ai/graph-memory.md",
    ".ai/shared-language.md",
    ".ai/prompts.md",
]

SKILLS = [
    "setup-memory",
    "new",
    "continue",
    "handoff",
    "update-memory",
    "compress-memory",
    "debug",
    "feature",
    "review",
    "graphify",
    "status",
    "architecture",
    "sync-decisions",
]


def main() -> int:
    root = Path.cwd()
    errors = []
    warnings = []

    for rel in REQUIRED:
        path = root / rel
        if not path.exists():
            errors.append(f"Missing required file: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            errors.append(f"Empty required file: {rel}")

    for skill in SKILLS:
        path = root / "skills" / "memory-framework" / skill / "SKILL.md"
        if not path.exists():
            errors.append(f"Missing skill: {skill}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "name:" not in text[:300] or "description:" not in text[:500]:
            warnings.append(f"Skill may be missing frontmatter name/description: {skill}")

    if errors:
        print("Memory framework validation failed:\n")
        for err in errors:
            print(f"ERROR: {err}")
    else:
        print("Memory framework validation passed.")

    if warnings:
        print("\nWarnings:\n")
        for warn in warnings:
            print(f"WARN: {warn}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
