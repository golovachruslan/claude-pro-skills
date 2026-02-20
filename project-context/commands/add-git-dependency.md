---
name: project-context:add-git-dependency
description: Add a cross-project dependency via git repository URL — fetches only .project-context/ from the remote
argument-hint: "<git-url>"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Git Link Dependency

Add a dependency on a remote project by its git URL. Only the `.project-context/` directory is fetched — no application code.

## Parameter

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<git-url>` | No | Git repository URL (HTTPS or SSH) |

If omitted, prompts for the URL interactively.

## Examples

```bash
# With URL — asks ref/direction/what/notes interactively
/project-context:add-git-dependency https://github.com/org/auth-service.git

# Fully interactive
/project-context:add-git-dependency
```

## Workflow

Invoke the `add-git-dependency` skill — it validates the URL, gathers metadata via AskUserQuestion, updates `dependencies.json`, and fetches the remote `.project-context/` into `.deps-cache/`.
