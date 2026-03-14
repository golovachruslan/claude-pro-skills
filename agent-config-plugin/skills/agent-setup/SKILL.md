---
name: agent-setup
description: >
  Use this skill when a user wants to configure Claude Code plugin setup for a project —
  creating setup.sh, setup.yaml, and a SessionStart hook so teammates can install all plugins
  automatically on session start. Triggers on requests like "set up plugin ecosystem",
  "add setup script", "configure marketplaces and plugins for this project".
allowed-tools:
  - Read
  - Write
  - Bash
---

# Agent Setup Skill

Set up a reusable Claude Code plugin ecosystem for any project. This skill interviews the user, generates config, and copies shell scripts so that every teammate gets the same plugins on first session.

## Workflow

### Step 1: Determine Target Directory

Ask the user for the target project directory. Default to the current working directory if they confirm.

### Step 2: Interview — Marketplaces

Ask the user to list marketplace sources. Each source is a GitHub slug or URL passed to `claude plugin marketplace add`. Show this example:

```
Examples of marketplace sources:
  - anthropics/claude-plugins-official
  - golovachruslan/claude-pro-skills
  - https://github.com/anthropics/claude-code.git --sparse .claude-plugin plugins
```

Collect one source per line. Allow the user to finish by sending an empty line or saying "done".

### Step 3: Interview — Plugins

Ask the user to list plugins in `name@marketplace` format. Allow grouping by marketplace with comments. Show this example:

```
Examples:
  - security-pro@claude-code-templates
  - plugin-dev@claude-plugins-official
  - skills-improver@claude-pro-skills
```

Collect entries. Allow the user to finish by sending an empty line or saying "done".

### Step 4: Generate `setup.yaml`

Write `<target>/setup.yaml` using the collected marketplaces and plugins. Use the format documented in `references/setup-yaml-format.md`. Include comments grouping plugins by marketplace for readability.

### Step 5: Copy `setup.sh`

Copy `assets/setup.sh` from this skill's directory into `<target>/setup.sh` and make it executable:

```bash
chmod +x <target>/setup.sh
```

### Step 6: Add SessionStart Hook

Add a SessionStart hook to `<target>/.claude/settings.json` so `setup.sh` runs automatically when a Claude Code session starts. Use this safe merge logic:

1. Read existing `<target>/.claude/settings.json` (or start with `{}` if it doesn't exist)
2. Parse the JSON content
3. Navigate to the `hooks.SessionStart` array (create intermediate keys if missing)
4. Check if the array already contains an entry with `setup.sh` in its command — **skip if already present**
5. Append a new entry:
   ```json
   {
     "matcher": "",
     "hooks": [
       {
         "type": "command",
         "command": "bash \"$CLAUDE_PROJECT_DIR/setup.sh\""
       }
     ]
   }
   ```
6. Write back the merged JSON — all existing hooks and settings must be preserved

### Step 7: Summary

Print a summary listing all created/modified files and next steps:

```
Created/modified files:
  - setup.yaml                  # Plugin ecosystem config
  - setup.sh                    # Installs marketplaces & plugins from setup.yaml
  - .claude/settings.json       # SessionStart hook added for auto-setup

Next steps:
  1. Review setup.yaml and adjust as needed
  2. Run: bash setup.sh --dry-run    (preview)
  3. Run: bash setup.sh              (install)
  4. Commit all files so teammates get the setup automatically
```

## Edge Cases

- If `setup.yaml` already exists in the target, ask the user whether to overwrite or merge.
- If `setup.sh` already exists in the target, warn the user before overwriting.
- If `.claude/settings.json` already has a SessionStart hook with `setup.sh`, skip adding it and inform the user.
- If `.claude/settings.json` has other hooks or settings, preserve them all — only append to the `SessionStart` array.
