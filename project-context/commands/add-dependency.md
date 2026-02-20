---
name: project-context:add-dependency
description: Add a cross-project dependency to the current subproject's dependencies.md in a monorepo
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Interactively add an upstream or downstream dependency to the current subproject's `dependencies.md`. Creates the file if it doesn't exist.

## When to Use

- Monorepo with multiple subprojects that share code, APIs, or types
- Adding a new import/API relationship between subprojects
- Declaring that another project consumes this project's output

## Workflow

Invoke the `add-dependency` skill — it handles context reading, user prompts, file creation/editing, and reciprocal updates.
