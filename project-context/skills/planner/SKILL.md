---
name: planner
description: "Use when users request feature planning, project planning, or implementation planning. Triggers: 'plan this feature', 'help me plan', 'how should I implement'. Creates structured executable plans from locked decisions. Run /project-context:discuss first to brainstorm."
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: agent
          prompt: |
            Check if the file just written is a plan in .project-context/plans/.
            Input: $ARGUMENTS

            If it's NOT a plan file, return {"ok": true}.

            If it IS a plan file, use the plan-verification skill to validate it.
            Return {"ok": true} if plan passes, or {"ok": false, "reason": "Issues found: ..."} if not.
          statusMessage: "Validating plan..."
          timeout: 60
---

# Feature & Project Planning Skill

Create structured, executable implementation plans. **Plans should flow from locked decisions** produced by the discuss skill.

## Core Principles

1. **Ask, don't assume** — Use AskUserQuestion when information is missing
2. **Plans are executable prompts** — Every task must have: Files, Action, Verify, Done
3. **Context-first** — Always read project context before planning
4. **Decisions before details** — Check for locked decisions from /project-context:discuss
5. **Leverage native features** — Use Plan Mode for research, native Tasks for tracking

## Planning Workflow

### 1. Read Project Context

**Always do this first:**
```bash
ls .project-context/*.md 2>/dev/null
```

If context exists, read:
- `brief.md` — goals, scope, constraints
- `architecture.md` — tech stack, system design
- `patterns.md` — established conventions
- `state.md` — current position, blockers
- `plans/*.md` — check for existing discussions/decisions

Use context to ask **informed** questions (reference specific tech, patterns, decisions).

### 2. Check for Locked Decisions

Look for decisions from a prior `/project-context:discuss` session:
- In conversation history
- In plan files with a "Decisions" section
- In `state.md` referencing a discuss session

If locked decisions exist, honor them. Do not re-ask resolved questions.

### 3. Gather Missing Requirements

If no prior discuss session, ask clarifying questions (max 4-5 per round):

**Good format:**
```
I need to understand [aspect] to plan this effectively.

1. [Specific question]?
2. [Specific question]?
3. [Specific question]?

This will help me [why it matters].
```

Refer to `references/question-patterns.md` for scenario-specific patterns.

### 4. Create Executable Plan

Use templates from `references/planning-templates.md`. Key structure:

```markdown
# [Feature Name] Plan

**Status:** Planning
**Created:** YYYY-MM-DD

## Overview
**Problem:** [What this solves]
**Solution:** [High-level approach]

## Decisions
[From discuss phase or gathered during planning]

## Implementation Phases

### Phase 1: [Name]
**Goal:** [What this achieves]

#### Task 1: [Name]
- **Files:** [exact paths]
- **Action:** [Concrete steps — what to build, which patterns to follow]
- **Verify:** [Command or check to confirm it works]
- **Done when:** [Observable acceptance criteria from user's perspective]

#### Task 2: [Name]
[Same structure]

## Risks & Mitigation
[Key risks with strategies]

## Next Steps
[What to do after planning]
```

**Task rules:**
- 2-4 tasks per phase (keeps context fresh if using subagents or Agent Teams)
- Specify exact file paths
- Verification must be executable (a command, URL check, or test)
- "Done when" describes observable behavior, not code details
- Mark task dependencies explicitly — these map to native Tasks DAG dependencies

### 5. Register in Native Tasks

After creating the plan, **register tasks in Claude Code's native task system** (`Ctrl+T` to view):
- Create task entries with proper dependency chains matching the plan phases
- Set `CLAUDE_CODE_TASK_LIST_ID=plan-[feature-name]` for cross-session persistence
- Tasks persist on disk — safe to `/clear` or `/compact` without losing the plan roadmap
- When Agent Teams are used for implementation, teammates share the same task list

**Fallback:** If native Tasks are not available, use TodoWrite for in-session tracking.

### 6. Save Plan

**Always ask the user** if they want to save:
- Propose hyphen-case filename from feature name
- Save to `.project-context/plans/[name].md`
- Update `progress.md` and `state.md` to reference the plan

Plan verification runs automatically after saving (via skill hook).

## Reference

- `references/planning-templates.md` — Full plan templates
- `references/question-patterns.md` — Question frameworks by scenario
