---
name: project-context:update
description: Update project context files based on chat history, code changes, or user input
argument-hint: "[file:brief|architecture|state|progress|patterns] [--chat|--scan|--input]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Update Project Context

Update one or more project context files based on different sources.

## Arguments

- `file` (optional): Specific file to update
  - `brief` — Project goals and scope
  - `architecture` — System diagrams and flows
  - `state` — Current position and focus
  - `progress` — Work status and items
  - `patterns` — Patterns and learnings
  - If omitted: Smart update of relevant files

- `--source` (optional): Where to get update information
  - `--chat` — Extract from current conversation history
  - `--scan` — Scan codebase for changes (git diff, new files)
  - `--input` — Interactive input from user
  - Default: Smart detection (chat if recent discussion, else scan)

## Workflow

### Step 1: Verify Context Exists

```bash
ls .project-context/*.md 2>/dev/null
```

If not found: "Run `/project-context:init` first."

### Step 2: Determine Update Source

**Smart Detection:**
1. Meaningful conversation context → use chat
2. Git status shows changes → use scan
3. Otherwise → prompt for input

### Step 3: Gather Update Information

#### For --chat:
Analyze conversation for decisions, progress, patterns, architecture changes.

#### For --scan:
```bash
git diff --stat HEAD~5 2>/dev/null || git status --short
```

Analyze for new components → architecture.md, new patterns → patterns.md, completed work → progress.md.

#### For --input:
Ask user specific questions based on the file being updated.

### Step 4: Update Files

For each file:
1. Read current content
2. Preserve existing content
3. Add new information in appropriate section
4. Update timestamp

**File-specific guidance:**

| File | What to update |
|------|----------------|
| `brief.md` | Goals, scope changes |
| `architecture.md` | New components, Mermaid diagrams (always with descriptions), tech decisions |
| `state.md` | Current focus, active plan, blockers, next action, session info |
| `progress.md` | Move items between Completed/In Progress/Upcoming |
| `patterns.md` | New patterns, conventions, learnings |

### Step 5: Refresh Managed Sections

Use the Python script for reliable updates:

```bash
python project-context/scripts/manage_context.py update-sections --file CLAUDE.md
python project-context/scripts/manage_context.py update-sections --file AGENTS.md
```

### Step 6: Show Summary

- Files updated
- Key changes made
- Configuration files refreshed

## Architecture Update Guidelines

When updating architecture.md:
1. **Always use Mermaid diagrams** for visual representation
2. **Every diagram needs** a clear title, descriptive labels, and step-by-step description below
3. Common types: `graph TD` (flow), `sequenceDiagram` (API calls), `classDiagram` (models)
