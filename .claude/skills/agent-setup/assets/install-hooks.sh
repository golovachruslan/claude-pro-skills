#!/usr/bin/env bash
#
# install-hooks.sh - Copy git hooks from .githooks/ to .git/hooks/
#
# Safe: skips hooks that already exist (won't overwrite).
#

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO_DIR/.githooks"
DEST="$REPO_DIR/.git/hooks"

if [[ ! -d "$SRC" ]]; then
  echo "No .githooks/ directory found."
  exit 1
fi

if [[ ! -d "$DEST" ]]; then
  mkdir -p "$DEST"
fi

installed=0
skipped=0

for hook in "$SRC"/*; do
  name="$(basename "$hook")"
  target="$DEST/$name"

  if [[ -f "$target" ]]; then
    echo "  skip: $name (already exists in .git/hooks/)"
    ((skipped++))
  else
    cp "$hook" "$target"
    chmod +x "$target"
    echo "  installed: $name"
    ((installed++))
  fi
done

echo ""
echo "Done. Installed: $installed, Skipped: $skipped"
