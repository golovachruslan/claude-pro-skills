---
name: project-context:implement
description: Implement a plan using multi-agent execution with deviation rules. Provide a plan file path or reference a plan from the conversation.
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Implement Plan

Execute an implementation plan with multi-agent parallelism and automatic deviation handling.

## Task Tool Usage

**If `Task` is available**, use Task subagents for:
- **Parallel task execution**: Launch independent tasks within a phase simultaneously
- **Fresh context per task**: Each subagent gets a clean context window
- **Codebase exploration**: Use `subagent_type=Explore` before modifying unfamiliar code

**If `Task` is not available**, execute tasks sequentially with direct tool operations.

## Usage

```
/project-context:implement [plan-path]
```

## Workflow

### Step 1: Locate the Plan

**If path provided:** Read the specified plan file.

**If no path:**
1. Check conversation for a plan
2. Check `.project-context/plans/` for saved plans
3. If multiple plans, ask user which one
4. If no plans found: "Run `/project-context:plan` first"

### Step 2: Confirm Scope

Present the plan summary and ask:
```
Plan: [Name]
Phases: [N] with [M] total tasks

Options:
1. Implement all phases
2. Implement only Phase [N]
3. Pick specific tasks
4. Cancel
```

**Do not proceed without confirmation.**

### Step 3: Read Project Context

Before implementing, read:
- `.project-context/architecture.md` — Follow existing patterns
- `.project-context/patterns.md` — Respect conventions
- `.project-context/state.md` — Current position

### Step 4: Execute Phase by Phase

For each phase:

1. **Announce the phase** with task list
2. **Group tasks by dependencies**:
   - Independent tasks within a phase → execute in parallel via Task subagents
   - Dependent tasks → execute sequentially
3. **For each task**, follow the executable format:
   - Read the **Action** field for what to do
   - Implement the change
   - Run the **Verify** check
   - Confirm against **Done when** criteria
4. **Mark completed tasks** immediately
5. **Handle deviations** using the rules below

### Step 5: Deviation Rules

When encountering unexpected situations during execution:

| Priority | Situation | Action |
|----------|-----------|--------|
| **Auto-fix** | Bugs (null pointers, inverted logic, security holes) | Fix immediately without asking |
| **Auto-add** | Missing validation, error handling, auth checks | Add without asking |
| **Auto-fix** | Blocking issues (missing imports, broken deps) | Fix without asking |
| **ASK** | Architecture changes (new tables, schema changes, framework switches) | **STOP and ask user** |
| **ASK** | Scope expansion (features not in the plan) | **STOP and ask user** |
| **NEVER** | Skip tests, ignore patterns, change unrelated code | Never do this |

**Rule: ASK always supersedes Auto-fix/Auto-add.** When in doubt, ask.

### Step 6: Update State

After each phase:
- Update `.project-context/state.md` with current position
- Update `.project-context/progress.md` with completed items
- Update plan file status (Planning → In Progress → Completed)

### Step 7: Summary

```
Implementation Complete!

Phases: [X/Y] completed
Tasks: [N] completed, [M] skipped

Files created:
- path/to/new-file.ts

Files modified:
- path/to/existing.ts

Next steps:
1. [Testing recommendations]
2. [Consider running /project-context:retro to capture learnings]
```

## Multi-Agent Execution Pattern

When using Task subagents for parallel execution:

```
Phase 1 has 3 independent tasks:
  Task 1 (auth middleware)    → Subagent A [fresh context]
  Task 2 (login endpoint)    → Subagent B [fresh context]
  Task 3 (auth tests)        → Subagent C [fresh context]

Phase 2 depends on Phase 1:
  Task 4 (depends on 1+2)    → Sequential after Phase 1
  Task 5 (independent)       → Can parallel with Task 4
```

Each subagent receives:
- The specific task (Action, Verify, Done criteria)
- Relevant project context (architecture, patterns)
- Locked decisions from the plan

## Best Practices

- **Confirm before starting** — Never implement without user approval
- **Follow existing patterns** — Read architecture.md and patterns.md
- **Atomic progress** — Update state after each task, not just at the end
- **Deviation rules** — Auto-fix bugs, ask about architecture changes
- **Fresh context** — Use subagents for independent tasks to avoid context degradation
