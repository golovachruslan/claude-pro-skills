---
name: project-context:add-dependency
description: Add a cross-project dependency to the current subproject's dependencies.md in a monorepo
argument-hint: "<project-path>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Add a dependency to the current subproject's `dependencies.json`.

## Parameter

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<project-path>` | No | Relative path to target project (e.g., `../shared`) |

If omitted, discovers sibling projects and presents them as choices.

## Examples

```bash
# With path — asks direction/what/notes interactively
/project-context:add-dependency ../shared

# Fully interactive
/project-context:add-dependency
```

## Workflow

Invoke the `add-dependency` skill — it resolves the path, then uses AskUserQuestion to gather direction, what's shared, and notes.
