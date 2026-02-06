---
name: project-context:discuss
description: Brainstorm and resolve gray areas before planning. Captures locked decisions that constrain the planner.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
  - Task
---

# Discuss & Brainstorm

Use the `project-context:discuss` skill to brainstorm requirements and resolve ambiguities BEFORE planning.

## Task Tool Usage

**If `Task` is available**, use subagents for:
- `subagent_type=Explore` to analyze existing codebase patterns relevant to the feature
- Parallel exploration of multiple areas the feature might touch

## Workflow

1. Read existing project context (brief.md, architecture.md, patterns.md)
2. Understand what the user wants to build
3. Identify 3-5 domain-specific gray areas
4. Deep-dive each gray area with focused questions (2-3 per area)
5. Lock decisions explicitly with rationale and trade-offs
6. Present complete decisions summary
7. Offer to save decisions or continue directly to `/project-context:plan`

## Key Rule

**Clarify HOW to implement, never expand WHAT to implement.** This phase resolves ambiguity within scope — it does not add new scope.
