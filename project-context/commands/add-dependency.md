---
name: project-context:add-dependency
description: Add, fetch, or refresh cross-project dependencies — local paths or git URLs
argument-hint: "<path-or-git-url | --fetch [name] | --clean [name]>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Cross-Project Dependency Management

Single command for all dependency operations.

## Parameter

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<path>` | No | Relative path to local sibling project |
| `<git-url>` | No | Git repository URL (HTTPS or SSH) |
| `--fetch [name]` | No | Fetch/refresh git dep caches (all or specific) |
| `--clean [name]` | No | Clean cached git dep contexts (all or specific) |

If omitted, asks interactively whether to add or fetch.

## Examples

```bash
# Add local dependency
/project-context:add-dependency ../shared

# Add git dependency (auto-fetches context)
/project-context:add-dependency https://github.com/org/auth-service.git

# Refresh all cached git deps
/project-context:add-dependency --fetch

# Refresh a specific git dep
/project-context:add-dependency --fetch auth-service

# Clean all cached contexts
/project-context:add-dependency --clean

# Interactive mode
/project-context:add-dependency
```

## Workflow

Invoke the `add-dependency` skill — it auto-detects intent from the argument (path, git URL, `--fetch`, or `--clean`), then proceeds accordingly.
