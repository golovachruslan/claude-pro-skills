#!/usr/bin/env bash
#
# setup.sh - Set up the full Claude Pro Skills plugin ecosystem
#
# Reads marketplaces and plugins from setup.yaml
#
# Usage:
#   bash setup.sh            # Install everything
#   bash setup.sh --dry-run  # Preview commands without executing
#   bash setup.sh --force    # Re-run even if already completed
#
# Idempotency: creates .setup-done marker on success; skips if marker exists.
# Use --force to bypass the marker check.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/setup.yaml"
MARKER="$SCRIPT_DIR/.setup-done"

# --- Colors & helpers ---

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

DRY_RUN=false
FORCE=false
PASS=0
FAIL=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --force)   FORCE=true ;;
  esac
done

if $DRY_RUN; then
  echo -e "${YELLOW}${BOLD}DRY RUN MODE${NC} — commands will be printed but not executed\n"
fi

# --- Idempotency check ---

if [[ -f "$MARKER" ]] && ! $FORCE && ! $DRY_RUN; then
  echo -e "${GREEN}Setup already completed${NC} (marker: $MARKER)"
  echo -e "Use ${BOLD}--force${NC} to re-run."
  exit 0
fi

run_cmd() {
  if $DRY_RUN; then
    echo -e "  ${BLUE}[dry-run]${NC} $*"
    return 0
  fi
  "$@" 2>&1
}

# Parse YAML list items (lines matching "  - value") under a given key
parse_yaml_list() {
  local key="$1"
  local file="$2"
  sed -n "/^${key}:/,/^[^ #-]/p" "$file" \
    | grep '^[[:space:]]*-' \
    | sed 's/^[[:space:]]*-[[:space:]]*//' \
    | sed 's/[[:space:]]*#.*//'
}

# --- Prerequisites ---

echo -e "${BOLD}Checking prerequisites...${NC}"

if [[ ! -f "$CONFIG" ]]; then
  echo -e "${RED}Error: setup.yaml not found at ${CONFIG}${NC}"
  exit 1
fi

if ! command -v claude &>/dev/null; then
  echo -e "${RED}Error: 'claude' CLI not found. Install it first:${NC}"
  echo "  npm install -g @anthropic-ai/claude-code"
  exit 1
fi

echo -e "${GREEN}  claude CLI found${NC}"
echo -e "${GREEN}  config: ${CONFIG}${NC}\n"

# --- Read config ---

MARKETPLACES=()
while IFS= read -r line; do
  MARKETPLACES+=("$line")
done < <(parse_yaml_list "marketplaces" "$CONFIG")

PLUGINS=()
while IFS= read -r line; do
  PLUGINS+=("$line")
done < <(parse_yaml_list "plugins" "$CONFIG")

# --- Add marketplaces ---

echo -e "${BOLD}Adding ${#MARKETPLACES[@]} marketplaces...${NC}"
for i in "${!MARKETPLACES[@]}"; do
  src="${MARKETPLACES[$i]}"
  step="[$((i + 1))/${#MARKETPLACES[@]}]"
  echo -ne "  ${step} ${src}... "

  set +e
  # shellcheck disable=SC2086
  run_cmd claude plugin marketplace add $src
  rc=$?
  set -e

  if [[ $rc -eq 0 ]]; then
    echo -e "${GREEN}ok${NC}"
    ((PASS++))
  else
    echo -e "${RED}failed${NC}"
    ((FAIL++))
  fi
done

echo ""

# --- Install & enable plugins ---

echo -e "${BOLD}Installing & enabling ${#PLUGINS[@]} plugins...${NC}"
for i in "${!PLUGINS[@]}"; do
  plugin="${PLUGINS[$i]}"
  name="${plugin%%@*}"
  step="[$((i + 1))/${#PLUGINS[@]}]"
  echo -ne "  ${step} ${plugin}... "

  set +e
  run_cmd claude plugin install "$plugin"
  rc_install=$?
  set -e

  if [[ $rc_install -ne 0 ]]; then
    echo -e "${RED}install failed${NC}"
    ((FAIL++))
    continue
  fi

  set +e
  run_cmd claude plugin enable "$name"
  rc_enable=$?
  set -e

  if [[ $rc_enable -eq 0 ]]; then
    echo -e "${GREEN}ok${NC}"
    ((PASS++))
  else
    echo -e "${YELLOW}installed but enable failed${NC}"
    ((FAIL++))
  fi
done

echo ""

# --- Summary ---

echo -e "${BOLD}Done!${NC}"
echo -e "  ${GREEN}Passed: ${PASS}${NC}"
if [[ $FAIL -gt 0 ]]; then
  echo -e "  ${RED}Failed: ${FAIL}${NC}"
fi
echo ""

# --- Create marker on success (skip in dry-run) ---

if ! $DRY_RUN && [[ $FAIL -eq 0 ]]; then
  date -u '+%Y-%m-%dT%H:%M:%SZ' > "$MARKER"
  echo -e "Marker created: ${MARKER}"
fi

if $DRY_RUN; then
  echo -e "Run ${BOLD}bash setup.sh${NC} (without --dry-run) to execute."
else
  echo -e "Verify with:"
  echo "  claude plugin marketplace list"
  echo "  claude plugin list"
fi
