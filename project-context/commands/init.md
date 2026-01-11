---
name: project-context:init
description: Initialize project context structure with 4 markdown files for tracking project state
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Initialize Project Context

Create the `.project-context/` directory with 4 structured markdown files for maintaining project context across sessions.

## Workflow

### Step 1: Check Existing Context

Check if `.project-context/` already exists:

```bash
ls -la .project-context/ 2>/dev/null
```

If exists, ask user:
- "Project context already exists. Would you like to reinitialize (overwrites existing) or skip?"

### Step 2: Create Directory Structure

```bash
mkdir -p .project-context
```

### Step 3: Gather Initial Context

Ask user for basic project information using AskUserQuestion:

1. **Project name and brief description** (for brief.md)
2. **Primary tech stack** (for architecture.md)
3. **Current focus/goals** (for progress.md)

### Step 4: Create Context Files

Create 4 files with templates. Use the reference templates from the `project-context:project-context` skill.

#### brief.md
```markdown
# Project Brief

## Overview
[Project name and description from user input]

## Goals
- [Primary goal]
- [Secondary goals]

## Scope
### In Scope
-

### Out of Scope
-

## Success Criteria
-

---
*Last updated: [current date]*
```

#### architecture.md
```markdown
# Architecture

## Tech Stack
[From user input]

## System Overview

```mermaid
graph TB
    subgraph "System Architecture"
        A[Component A] --> B[Component B]
        B --> C[Component C]
    end
```

**Flow Description:**
1. Step 1 description
2. Step 2 description
3. Step 3 description

## Key Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| | | |

---
*Last updated: [current date]*
```

#### progress.md
```markdown
# Progress

## Current Focus
[From user input]

## Status
- **Phase**: [Development/Testing/Production]
- **Sprint/Cycle**:
- **Blockers**: None

## Completed
- [ ]

## In Progress
- [ ]

## Upcoming
- [ ]

## Known Issues
-

---
*Last updated: [current date]*
```

#### patterns.md
```markdown
# Patterns & Learnings

## Established Patterns

### Code Patterns
-

### Architecture Patterns
-

### Process Patterns
-

## Learnings

### What Worked
-

### What Didn't Work
-

### Key Insights
-

---
*Last updated: [current date]*
```

### Step 5: Update AI Agent Configuration Files

#### Update CLAUDE.md (if exists)

Check if CLAUDE.md exists in project root:
```bash
ls CLAUDE.md 2>/dev/null
```

If exists, check if managed section already present:
```bash
grep -q "<!-- PROJECT-CONTEXT:START -->" CLAUDE.md 2>/dev/null
```

If managed section does NOT exist, append the following:

```markdown

<!-- PROJECT-CONTEXT:START -->
## Project Context

These instructions are for AI assistants working in this project.

Always read `.project-context/` files when starting work to understand:
- Project goals and scope (`brief.md`)
- System architecture and flows (`architecture.md`)
- Current status and blockers (`progress.md`)
- Established patterns and learnings (`patterns.md`)

Use these files to:
- Understand project constraints before making changes
- Follow established patterns and conventions
- Avoid duplicate work or conflicting approaches
- Maintain consistency with project goals

Keep this managed block so project-context commands can refresh the instructions.

<!-- PROJECT-CONTEXT:END -->
```

If managed section ALREADY exists, inform user that CLAUDE.md already has project-context configuration.

#### Update AGENTS.md (if exists)

Check if AGENTS.md exists:
```bash
ls AGENTS.md 2>/dev/null
```

If exists, check if managed section already present:
```bash
grep -q "<!-- PROJECT-CONTEXT:START -->" AGENTS.md 2>/dev/null
```

If managed section does NOT exist, append the following:

```markdown

<!-- PROJECT-CONTEXT:START -->
## Project Context

These instructions are for AI agents working in this project.

Before executing tasks, read `.project-context/` files:
- `brief.md` - Understand project scope and goals
- `architecture.md` - Review system design and flows
- `progress.md` - Check current status and blockers
- `patterns.md` - Follow established patterns

Use these files to:
- Align work with project goals
- Apply established architecture patterns
- Avoid conflicts with current work
- Make context-aware decisions

Keep this managed block so project-context commands can refresh the instructions.

<!-- PROJECT-CONTEXT:END -->
```

If managed section ALREADY exists, inform user that AGENTS.md already has project-context configuration.

### Step 6: Confirmation

Display summary:
- List created files
- Show any updates to CLAUDE.md/AGENTS.md
- Suggest next steps: "Run `/project-context:update` to add more detail"

## Tips

- Keep brief.md stable - it's the foundation
- Update architecture.md when adding new components or flows
- Update progress.md frequently during active development
- Add to patterns.md when you learn something valuable
