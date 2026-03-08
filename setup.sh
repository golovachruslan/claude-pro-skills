#!/usr/bin/env bash
#
# setup.sh - Set up the full Claude Pro Skills plugin ecosystem
#
# Usage:
#   bash setup.sh            # Install everything
#   bash setup.sh --dry-run  # Preview commands without executing
#

set -euo pipefail

# --- Configuration ---

MARKETPLACES=(
  "davila7/claude-code-templates"
  "anthropics/skills"
  "https://github.com/anthropics/claude-code.git --sparse .claude-plugin plugins"
  "anthropics/claude-plugins-official"
  "golovachruslan/claude-pro-skills"
  "kepano/obsidian-skills"
)

PLUGINS=(
  # claude-code-templates
  "security-pro@claude-code-templates"
  "git-workflow@claude-code-templates"

  # claude-code-plugins (anthropics/claude-code repo)
  "plugin-dev@claude-code-plugins"
  "security-guidance@claude-code-plugins"
  "feature-dev@claude-code-plugins"
  "frontend-design@claude-code-plugins"

  # claude-plugins-official
  "playwright@claude-plugins-official"
  "plugin-dev@claude-plugins-official"
  "commit-commands@claude-plugins-official"
  "hookify@claude-plugins-official"
  "skill-creator@claude-plugins-official"
  "playground@claude-plugins-official"
  "frontend-design@claude-plugins-official"
  "code-simplifier@claude-plugins-official"
  "claude-md-management@claude-plugins-official"

  # claude-pro-skills (this repo)
  "obsidian@claude-pro-skills"
  "skills-improver@claude-pro-skills"
  "project-context@claude-pro-skills"
  "agent-context@claude-pro-skills"
  "mermaid@claude-pro-skills"

  # obsidian-skills
  "obsidian@obsidian-skills"
)

# --- Colors & helpers ---

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

DRY_RUN=false
PASS=0
FAIL=0
SKIP=0

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo -e "${YELLOW}${BOLD}DRY RUN MODE${NC} — commands will be printed but not executed\n"
fi

run_cmd() {
  if $DRY_RUN; then
    echo -e "  ${BLUE}[dry-run]${NC} $*"
    return 0
  fi

  if "$@" 2>&1; then
    return 0
  else
    return 1
  fi
}

# --- Prerequisites ---

echo -e "${BOLD}Checking prerequisites...${NC}"
if ! command -v claude &>/dev/null; then
  echo -e "${RED}Error: 'claude' CLI not found. Install it first:${NC}"
  echo "  npm install -g @anthropic-ai/claude-code"
  exit 1
fi
echo -e "${GREEN}  claude CLI found${NC}\n"

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

TOTAL=$((PASS + FAIL + SKIP))
echo -e "${BOLD}Done!${NC}"
echo -e "  ${GREEN}Passed: ${PASS}${NC}"
if [[ $FAIL -gt 0 ]]; then
  echo -e "  ${RED}Failed: ${FAIL}${NC}"
fi
echo ""

if $DRY_RUN; then
  echo -e "Run ${BOLD}bash setup.sh${NC} (without --dry-run) to execute."
else
  echo -e "Verify with:"
  echo "  claude plugin marketplace list"
  echo "  claude plugin list"
fi
