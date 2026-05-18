#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${AGENT_MEMORY_REPO:-https://github.com/sandeepkarmacharya/agent-memory-framework.git}"
TARGET="${AGENT_MEMORY_TARGET:-${1:-$(pwd)}}"
TARGET="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"
TMP_DIR=""

cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

need_cmd python

if [ -n "${AGENT_MEMORY_SOURCE:-}" ]; then
  SOURCE="$AGENT_MEMORY_SOURCE"
else
  need_cmd git
  TMP_DIR="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP_DIR" >/dev/null 2>&1
  SOURCE="$TMP_DIR"
fi

if [ ! -f "$SOURCE/scripts/agent-memory" ]; then
  echo "Invalid Agent Memory source: $SOURCE" >&2
  exit 1
fi

mkdir -p "$TARGET"

COMMAND="install"
if [ -d "$TARGET/.ai" ] || [ -f "$TARGET/scripts/agent-memory" ]; then
  COMMAND="upgrade"
fi

echo "Running: python scripts/agent-memory $COMMAND --target $TARGET"
python "$SOURCE/scripts/agent-memory" "$COMMAND" --target "$TARGET"

echo
echo "Agent Memory Framework ready in $TARGET"
echo "Next: ask your agent to follow AGENTS.md, or run:"
echo "  python scripts/agent-memory context \"<task>\""
