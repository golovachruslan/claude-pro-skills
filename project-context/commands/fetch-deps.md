---
name: project-context:fetch-deps
description: Fetch or refresh .project-context/ from all git link dependencies
argument-hint: "[project-name]"
allowed-tools:
  - Read
  - Bash
---

# Fetch Git Link Dependencies

Fetch (or refresh) the `.project-context/` directories from all git link dependencies declared in `dependencies.json`. Only context files are fetched — no application code.

## Parameter

| Parameter | Required | Description |
|-----------|----------|-------------|
| `[project-name]` | No | Fetch only this specific dependency (by project name) |

If omitted, fetches all git link dependencies.

## Examples

```bash
# Fetch all git link deps
/project-context:fetch-deps

# Fetch only a specific dependency
/project-context:fetch-deps auth-service
```

## Workflow

Runs `fetch_git_deps.py fetch` to:
1. Read `dependencies.json` for entries with a `git` field
2. Shallow-clone each remote to a temp directory
3. Copy only `.project-context/` files into `.deps-cache/<project>/` (flat — no `.git/`)
4. Clean up temp clones and report fetch status
