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

Update project context files using the specified source.

**Modes:**
- `--chat` — Deep conversation analysis with signal recognition (default when conversation has meaningful content)
- `--scan` — Git diff/status analysis
- `--input` — Interactive user prompts

**File targeting:** Optionally specify a single file to update: `brief`, `architecture`, `state`, `progress`, or `patterns`.

Use the `project-context:update` skill to perform the update workflow.
