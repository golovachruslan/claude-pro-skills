---
name: agent-setup
description: >
  Use this skill when a user wants to configure Claude Code plugin setup for a project —
  creating setup.sh, setup.yaml, and a git hook so teammates can install all plugins
  with a single command. Triggers on requests like "set up plugin ecosystem",
  "add setup script", "configure marketplaces and plugins for this project".
allowed-tools:
  - Read
  - Write
  - Bash
---

# Agent Setup Skill

Set up a reusable Claude Code plugin ecosystem for any project. This skill interviews the user, generates config, and copies shell scripts so that every teammate gets the same plugins on first clone.

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

### Step 5: Copy Asset Files

Copy these files from the skill's `assets/` directory into the target project:

| Source                    | Destination                        |
|---------------------------|------------------------------------|
| `assets/setup.sh`        | `<target>/setup.sh`               |
| `assets/install-hooks.sh`| `<target>/install-hooks.sh`        |
| `assets/post-checkout`   | `<target>/.githooks/post-checkout` |

Create the `.githooks/` directory if it doesn't exist.

### Step 6: Make Scripts Executable

```bash
chmod +x <target>/setup.sh <target>/install-hooks.sh <target>/.githooks/post-checkout
```

### Step 7: Offer to Install Hooks

Ask the user if they want to run `bash install-hooks.sh` now to activate the post-checkout hook in `.git/hooks/`.

### Step 8: Summary

Print a summary listing all created files and next steps:

```
Created files:
  - setup.yaml          # Plugin ecosystem config
  - setup.sh            # Installs marketplaces & plugins from setup.yaml
  - install-hooks.sh    # Copies .githooks/ to .git/hooks/
  - .githooks/post-checkout  # Auto-runs setup.sh on first clone

Next steps:
  1. Review setup.yaml and adjust as needed
  2. Run: bash setup.sh --dry-run    (preview)
  3. Run: bash setup.sh              (install)
  4. Commit all files so teammates get the setup on clone
```

## Edge Cases

- If `setup.yaml` already exists in the target, ask the user whether to overwrite or merge.
- If any asset file already exists, warn the user before overwriting.
- If the target is not a git repository, skip the hook installation step and note that hooks require a git repo.
