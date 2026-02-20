---
name: project-context:add-dependency
description: Add a cross-project dependency to the current subproject's dependencies.md in a monorepo
argument-hint: "<upstream|downstream> <project-path> [--what DESCRIPTION] [--note NOTE] [--no-reciprocal]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Add an upstream or downstream dependency to the current subproject's `dependencies.md`. Creates the file if it doesn't exist.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<direction>` | No | `upstream` (this project consumes) or `downstream` (consumed by) |
| `<project-path>` | No | Relative path to target project (e.g., `../shared`) |
| `--what` | No | What is shared (e.g., "Types, validation utilities") |
| `--note` | No | Optional note (e.g., "Core domain types") |
| `--no-reciprocal` | No | Skip reciprocal update on target project |

All parameters are optional — missing ones are gathered interactively.

## Examples

```bash
# Fully specified — no prompts
/project-context:add-dependency upstream ../shared --what "Types, validators" --note "Core domain"

# Direction + path only — prompts for what/note
/project-context:add-dependency downstream ../web

# Interactive — prompts for everything
/project-context:add-dependency
```

## Workflow

Invoke the `add-dependency` skill — it parses provided params, skips interactive prompts for any that were supplied, and gathers the rest.
