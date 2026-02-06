---
name: project-context
description: "Use this skill when users ask about project context, project goals, current progress, architecture, technical decisions, project status, or current state. Triggers: 'what is this project', 'project goals', 'current progress', 'architecture', 'tech stack', 'what are we working on', 'project status', 'where are we'."
---

# Project Context Skill

Provide informed responses about project state by reading structured context files from `.project-context/`.

## Context Files (5-file model)

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `brief.md` | Project goals, scope, requirements | Rarely (on pivots) |
| `architecture.md` | Tech stack, Mermaid diagrams, system design | On architecture changes |
| `state.md` | Current position, blockers, next action | Every session |
| `progress.md` | Completed/in-progress/upcoming work | Multiple times per week |
| `patterns.md` | Established patterns and learnings | As patterns emerge |

## Workflow

### 1. Check for Context Files

```bash
ls .project-context/*.md 2>/dev/null
```

If not found: "No project context found. Run `/project-context:init` to set up."

### 2. Read Relevant Files

| Query Type | Primary File | Secondary |
|------------|--------------|-----------|
| "What is this project?" | brief.md | architecture.md |
| "Current status/progress" | state.md | progress.md |
| "Where are we?" | state.md | progress.md |
| "Architecture/how it works" | architecture.md | patterns.md |
| "Tech stack" | architecture.md | - |
| "What patterns do we use?" | patterns.md | architecture.md |
| General context | All files | - |

### 3. Synthesize Response

- **Be concise** — Extract key points, don't dump files
- **Reference diagrams** — Describe flows from Mermaid diagrams
- **Note currency** — Check timestamps, warn if stale
- **Connect dots** — Link related info across files

### 4. Handle Missing Context

1. Answer with available information
2. Note what's missing
3. Suggest: "Run `/project-context:update [file]` to add this"

### 5. Staleness Detection

If context seems stale (state.md >1 day, progress.md >3 days during active dev):
- Suggest: "Context may be outdated. Run `/project-context:update --scan` to refresh."

## Reference

- `references/file-templates.md` — Template structures for each file
- `references/best-practices.md` — Guidelines for maintaining context
