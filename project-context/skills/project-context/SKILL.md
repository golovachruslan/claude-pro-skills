---
name: project-context
description: "Use this skill when users ask about project context, project goals, current progress, architecture, technical decisions, what the project does, project status, or need to understand the project state. Triggers include: 'what is this project', 'project goals', 'current progress', 'architecture', 'tech stack', 'what are we working on', 'project status', 'how does this work'."
---

# Project Context Skill

Provide informed responses about project state by reading structured context files from `.project-context/`.

## Context Files Location

All project context is stored in `.project-context/`:
- `brief.md` - Project goals, scope, requirements
- `architecture.md` - Tech stack, Mermaid diagrams, system design
- `progress.md` - Current status, completed/pending work
- `patterns.md` - Established patterns and learnings

## Workflow

### 1. Check for Context Files

First, verify context exists:
```bash
ls .project-context/*.md 2>/dev/null
```

If not found:
- Inform user: "No project context found. Run `/project-context:init` to set up."
- Offer to initialize

### 2. Read Relevant Files

Based on user query, read appropriate files:

| Query Type | Primary File | Secondary Files |
|------------|--------------|-----------------|
| "What is this project?" | brief.md | architecture.md |
| "Current status/progress" | progress.md | - |
| "Architecture/how it works" | architecture.md | patterns.md |
| "Tech stack" | architecture.md | - |
| "What patterns do we use?" | patterns.md | architecture.md |
| General context | All files | - |

### 3. Synthesize Response

When answering:

1. **Be concise** - Extract key points, don't dump entire files
2. **Reference diagrams** - If architecture.md has Mermaid diagrams, describe the flows
3. **Note currency** - Check "Last updated" timestamps, warn if stale
4. **Connect dots** - Link related information across files

### 4. Response Format

Structure responses based on query:

**For "What is this project?"**
```
## [Project Name]

[Brief description from brief.md]

**Goals:**
- Goal 1
- Goal 2

**Tech Stack:** [From architecture.md]

**Current Focus:** [From progress.md]
```

**For "Architecture" queries**
```
## System Architecture

[Describe the architecture from diagrams]

**Key Components:**
1. Component A - Description
2. Component B - Description

**Main Flows:**
[Summarize flow descriptions from architecture.md]
```

**For "Progress" queries**
```
## Current Status

**Focus:** [Current focus]
**Phase:** [Development phase]

**Completed:**
- Item 1
- Item 2

**In Progress:**
- Item 1

**Blockers:** [Any blockers]
```

## Handling Missing Context

If specific context is missing:

1. Answer with available information
2. Note what's missing: "Note: architecture.md doesn't have diagrams for this flow yet"
3. Suggest updating: "Consider running `/project-context:update architecture` to add this"

## Proactive Context Awareness

When working on tasks, proactively:

1. **Check patterns.md** before implementing - follow established patterns
2. **Check progress.md** to understand current focus
3. **Check architecture.md** to understand system design

## Cross-Reference with CLAUDE.md

If CLAUDE.md exists, it should reference the context files. Read both for complete picture.

## Keep Context Fresh

If context seems stale (>7 days old with active development):
- Suggest: "Project context may be outdated. Run `/project-context:update --scan` to refresh."

## Reference Files

For detailed templates and best practices, see:
- `references/file-templates.md` - Template structures for each file
- `references/best-practices.md` - Guidelines for maintaining context
