---
name: info
description: Ask a question about the current project
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
---

# Info Command

Answer questions about the current project by researching the codebase and any available project context.

## Instructions

1. **Take the user's question** from the command argument (e.g., `/info how does auth work?`)
2. **Invoke the info skill** to research and answer the question
3. **If no question was provided**, ask the user what they'd like to know about the project

## What This Command Does

This command gives you a quick way to ask questions about your project. It combines:
- Structured project context (`.project-context/` files) if available
- Live codebase exploration (file search, code search, reading source)
- Git history when relevant

## Example Usage

```
/info how is the database layer structured?
/info where are API routes defined?
/info what testing framework does this project use?
/info why do we use a monorepo?
/info what does the UserService class do?
```
