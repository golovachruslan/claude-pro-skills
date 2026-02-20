---
name: project-context:add-dependency
description: Add a cross-project dependency — local path (monorepo) or git URL (remote repo)
argument-hint: "<path-or-git-url>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Add a dependency to the current project's `dependencies.json`. Accepts either a local path (monorepo sibling) or a git URL (remote repository — only `.project-context/` is fetched).

## Parameter

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path-or-git-url>` | No | Relative path (e.g., `../shared`) or git URL (e.g., `https://github.com/org/repo.git`) |

If omitted, asks whether to add a local or git dependency, then proceeds interactively.

## Examples

```bash
# Local path — asks direction/what/notes interactively
/project-context:add-dependency ../shared

# Git URL — asks ref/name/direction/what/notes interactively
/project-context:add-dependency https://github.com/org/auth-service.git

# Fully interactive — asks dependency type first
/project-context:add-dependency
```

## Workflow

Invoke the `add-dependency` skill — it auto-detects local path vs git URL from the argument, then uses AskUserQuestion to gather the remaining details.
