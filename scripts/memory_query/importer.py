"""Repo importer: scan an existing project and bootstrap .ai/ memory files.

Usage:
    from memory_query.importer import import_repo
    import_repo("/path/to/repo")

CLI:
    python scripts/agent-memory import /path/to/repo
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


# ── Detection Patterns ─────────────────────────────────────────────────────

_LANG_EXTS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "React", ".tsx": "React TypeScript", ".java": "Java",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
    ".swift": "Swift", ".kt": "Kotlin", ".cpp": "C++", ".c": "C",
    ".h": "C/C++ Header", ".cs": "C#", ".scala": "Scala",
    ".r": "R", ".m": "Objective-C", ".dart": "Dart",
    ".lua": "Lua", ".elixir": "Elixir", ".ex": "Elixir",
    ".exs": "Elixir Script", ".clj": "Clojure",
    ".hs": "Haskell", ".svelte": "Svelte", ".vue": "Vue",
    ".eex": "Elixir Template", ".heex": "Elixir HEEx",
}

_FRAMEWORK_INDICATORS = {
    "requirements.txt": "Python",
    "setup.py": "Python",
    "pyproject.toml": "Python (PEP 621)",
    "Cargo.toml": "Rust",
    "package.json": "Node.js",
    "go.mod": "Go",
    "Gemfile": "Ruby",
    "build.gradle": "Java/Gradle",
    "pom.xml": "Java/Maven",
    "composer.json": "PHP",
    "Mix.exs": "Elixir",
}


def _run(cmd: List[str], cwd: Path) -> str:
    """Run a shell command and return stdout."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=cwd)
        return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def _detect_languages(root: Path) -> Dict[str, int]:
    """Count source files by language extension."""
    counts = {}
    for fpath in root.rglob("*"):
        if fpath.is_dir() or fpath.name.startswith("."):
            continue
        ext = fpath.suffix.lower()
        if ext in _LANG_EXTS:
            lang = _LANG_EXTS[ext]
            counts[lang] = counts.get(lang, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def _detect_framework(root: Path) -> Optional[str]:
    """Detect project framework from config files."""
    for fname, framework in _FRAMEWORK_INDICATORS.items():
        if (root / fname).exists():
            return framework

    # Check in subdirectories too
    for f in root.rglob("*"):
        if f.name in _FRAMEWORK_INDICATORS:
            return _FRAMEWORK_INDICATORS[f.name]
    return None


def _detect_package_name(root: Path) -> str:
    """Try to determine project name from various config files."""
    # package.json
    pj = root / "package.json"
    if pj.exists():
        try:
            return json.loads(pj.read_text()).get("name", "")
        except (json.JSONDecodeError, Exception):
            pass

    # pyproject.toml
    ppt = root / "pyproject.toml"
    if ppt.exists():
        for line in ppt.read_text().splitlines():
            m = re.match(r'^name\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1)

    # Cargo.toml
    ct = root / "Cargo.toml"
    if ct.exists():
        for line in ct.read_text().splitlines():
            m = re.match(r'^name\s*=\s*"([^"]+)"', line)
            if m:
                return m.group(1)

    # Fallback: directory name
    return root.name


def _detect_build_tools(root: Path) -> List[str]:
    """Detect CI/CD and build systems."""
    tools = []
    checks = [
        ("Makefile", "Make"),
        ("Dockerfile", "Docker"),
        ("docker-compose.yml", "Docker Compose"),
        (".github/workflows", "GitHub Actions"),
        (".gitlab-ci.yml", "GitLab CI"),
        ("Jenkinsfile", "Jenkins"),
        ("Justfile", "Just"),
        ("Taskfile.yml", "Taskfile"),
        ("tox.ini", "Tox"),
        ("noxfile.py", "Nox"),
    ]
    for fname, tool in checks:
        if (root / fname).exists():
            tools.append(tool)
    return tools


def _detect_tests(root: Path) -> Dict[str, int]:
    """Count test files."""
    patterns = [
        "test_*.py", "*_test.py", "*.test.js", "*.spec.js",
        "*_test.go", "*_spec.rb", "test_*.rb",
    ]
    counts = {}
    total = 0
    for fpath in root.rglob("*"):
        if not fpath.is_file():
            continue
        name = fpath.name
        if name.startswith("test_") or name.endswith("_test.py") or name.endswith("_spec.rb"):
            ext = fpath.suffix.lower()
            lang = _LANG_EXTS.get(ext, "unknown")
            counts[lang] = counts.get(lang, 0) + 1
            total += 1
    counts["total"] = total
    return counts


def _detect_structure(root: Path, max_depth: int = 3) -> str:
    """List project directory structure (text form)."""
    lines = []
    prefix = ""
    root_str = str(root)

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs, node_modules, venv, __pycache__
        dirnames[:] = [d for d in dirnames if not d.startswith(".")
                      and d not in ("node_modules", "venv", ".venv",
                                    "__pycache__", ".git", ".ai",
                                    "target", "dist", "build")]

        rel = Path(dirpath).relative_to(root)
        depth = len(rel.parts)
        if depth > max_depth:
            continue

        indent = "  " * depth
        if depth == 0:
            lines.append(f"{root.name}/")
            continue

        lines.append(f"{indent}{rel.name}/")

        # Show first few files in each directory
        for fname in sorted(filenames)[:6]:
            if not fname.startswith("."):
                lines.append(f"{indent}  {fname}")

    return "\n".join(lines)


def _detect_deps(root: Path) -> List[str]:
    """Extract dependency info from common config files."""
    deps = []

    # Python requirements.txt
    req = root / "requirements.txt"
    if req.exists():
        for line in req.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-"):
                deps.append(line)

    # package.json dependencies
    pj = root / "package.json"
    if pj.exists():
        try:
            data = json.loads(pj.read_text())
            for key in ("dependencies", "devDependencies"):
                if key in data:
                    for pkg, ver in data[key].items():
                        deps.append(f"{pkg}@{ver}")
        except (json.JSONDecodeError, Exception):
            pass

    return deps


def _readme_summary(root: Path) -> str:
    """Extract first meaningful paragraph from README."""
    for fname in ("README.md", "README.rst", "README.txt", "README"):
        fp = root / fname
        if fp.exists():
            text = fp.read_text(encoding="utf-8", errors="replace")
            # Skip headings, find first paragraph
            for line in text.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and len(line) > 30:
                    return line[:200]
    return ""


# ── Bootstrap Templates ────────────────────────────────────────────────────

def _make_project_brief(root: Path) -> str:
    name = _detect_package_name(root)
    readme = _readme_summary(root)
    lang_counts = _detect_languages(root)
    primary_langs = ", ".join(lang for lang in list(lang_counts.keys())[:3]) if lang_counts else "TBD"
    framework = _detect_framework(root) or "TBD"

    return f"""# Project Brief

## Goal
{readme or f'Project: {name}. (Auto-detected from repo structure — update this.)'}

## Languages
{primary_langs}

## Framework
{framework}

## Build & CI
{', '.join(_detect_build_tools(root)) or 'TBD'}

## Constraints
<!-- Add known constraints here -->
"""


def _make_architecture(root: Path) -> str:
    structure = _detect_structure(root)
    return f"""# Architecture

## Overview
Auto-detected from project structure. Update with actual architecture decisions.

## Project Structure
```
{structure}
```

## Technologies
<!-- Primary technologies used -->
"""


def _make_dependencies(root: Path) -> str:
    deps = _detect_deps(root)
    if not deps:
        return """# Dependencies
<!-- None auto-detected. Populate manually. -->
"""

    # Categorize
    runtimes = [d for d in deps if not d.startswith("pytest") and not d.startswith("mypy")]
    dev = [d for d in deps if d.startswith("pytest") or d.startswith("mypy") or d.startswith("flake") or d.startswith("black") or d.startswith("ruff")]

    lines = ["# Dependencies\n"]
    if runtimes:
        lines.append("## Runtime")
        for d in runtimes[:20]:
            lines.append(f"- {d}")
        lines.append("")
    if dev:
        lines.append("## Dev")
        for d in dev[:10]:
            lines.append(f"- {d}")

    return "\n".join(lines)


def _make_task_board(root: Path) -> str:
    tests = _detect_tests(root)
    total_tests = tests.pop("total", 0)
    return f"""# Task Board

## Next
<!-- Auto-imported project. Review and fill initial tasks. -->

## Backlog
- Review auto-generated memory and fill in project details
- Set up CI/CD if not already configured
- Run existing tests and document results
- Create initial development plan

## Done
<!-- Project imported by agent-memory import -->
"""


def _make_current_state(root: Path) -> str:
    lang_counts = _detect_languages(root)
    total_files = sum(lang_counts.values())
    tests = _detect_tests(root)
    total_tests = tests.pop("total", 0)
    framework = _detect_framework(root) or "Unknown"

    return f"""# Current State
<!-- Auto-imported from project analysis -->

Project scanned: {total_files} source files in {len(lang_counts)} languages
Primary: {framework}
Tests: {total_tests} test files detected

## What's Built
<!-- Source files detected. No feature analysis performed. -->

## What's Missing
- [ ] Review and fill auto-generated memory files
- [ ] Document architecture decisions
- [ ] Define project scope and goals
"""


# ── Main ───────────────────────────────────────────────────────────────────

def import_repo(root_path: str, ai_dir: str = ".ai") -> Dict[str, str]:
    """Scan an existing project and bootstrap .ai/ memory files.

    Returns dict of {filename: status} for created/skipped files.
    """
    root = Path(root_path).resolve()
    ai = root / ai_dir

    if not root.exists():
        return {"error": f"Path does not exist: {root}"}

    # Check it's a git repo or has source files
    is_git = (root / ".git").exists()
    sources = _detect_languages(root)
    if not is_git and not sources:
        return {"error": "Not a git repository and no source files found."}

    ai.mkdir(parents=True, exist_ok=True)

    files_created = {}
    generators = {
        "project-brief.md": _make_project_brief,
        "current-state.md": _make_current_state,
        "architecture.md": _make_architecture,
        "dependencies.md": _make_dependencies,
        "task-board.md": _make_task_board,
    }

    for fname, gen_fn in generators.items():
        fpath = ai / fname
        if fpath.exists():
            files_created[fname] = "skipped (exists)"
        else:
            content = gen_fn(root)
            fpath.write_text(content.strip() + "\n", encoding="utf-8")
            files_created[fname] = "created"

    return files_created


def import_cli(args) -> int:
    """CLI handler for 'agent-memory import'."""
    target = args.path or "."
    result = import_repo(target)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    print(f"Imported project: {Path(target).resolve()}")
    print()
    for fname, status in result.items():
        icon = "✓" if status == "created" else "○"
        print(f"  {icon} {fname} — {status}")

    print()
    print("Review the generated files and fill in TBD placeholders.")
    print("Run: agent-memory init  (to create remaining memory files)")
    print("     agent-memory validate  (to check integrity)")
    return 0
