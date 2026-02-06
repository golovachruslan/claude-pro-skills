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

## Usage

```
/project-context:implement [plan-path] [--solo] [--strategy teams|subagents|sequential]
```

**Execution flags:**
- **`--solo`** — Skip Agent Teams, use subagents or sequential (shorthand for `--strategy subagents`)
- **`--strategy teams`** — Force Agent Teams (fails if not enabled)
- **`--strategy subagents`** — Force Task subagents (same as `--solo`)
- **`--strategy sequential`** — Force sequential execution, no parallelism

If no flag is provided, auto-selects the best available strategy.

## Execution Strategy Selection

Resolve strategy from flags first, then auto-detect:

1. **Parse flags** — `--solo` or `--strategy` override auto-detection
2. **Auto-detect** (no flags) — Agent Teams > Task subagents > Sequential

### Strategy: Agent Teams (auto or `--strategy teams`)

**When:** No `--solo`, plan has 3+ independent tasks, and Agent Teams is enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).

Agent Teams provide true parallel execution with separate context windows and inter-agent coordination:

1. **Team lead** (this session) coordinates execution and tracks progress
2. **Teammates** execute independent tasks in parallel with fresh context
3. **Shared task list** provides DAG-based dependency tracking
4. **Inter-agent messaging** allows teammates to flag conflicts or shared concerns

**Setup:**
- Enable delegate mode (`Shift+Tab`) so the lead focuses on coordination
- Assign each independent task to a separate teammate
- Teammates should read architecture.md and patterns.md before implementing
- Use the shared task list to track dependencies between phases

**Teammate assignment pattern:**
```
Phase 1 — 3 independent tasks:
  Teammate A: auth middleware    [reads architecture.md → implements → verifies]
  Teammate B: login endpoint     [reads patterns.md → implements → verifies]
  Teammate C: auth tests         [reads both → implements → verifies]

Team lead: monitors progress, resolves conflicts, handles deviations

Phase 2 — depends on Phase 1:
  Lead waits for Phase 1 completion → assigns Phase 2 tasks
```

### Strategy: Task Subagents (`--solo` / `--strategy subagents` / default fallback)

**When:** `--solo` specified, or Agent Teams not available/plan too small.

Use Task tool subagents for parallel execution:
- **Parallel task execution**: Launch independent tasks within a phase simultaneously
- **Fresh context per task**: Each subagent gets a clean context window
- **Codebase exploration**: Use `subagent_type=Explore` before modifying unfamiliar code

### Strategy: Sequential (`--strategy sequential` / final fallback)

**When:** `--strategy sequential` specified, or neither Agent Teams nor Task tool is available.

Execute tasks sequentially with direct tool operations.

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
Execution: [Agent Teams / Task subagents / Sequential]

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

### Step 4: Initialize Task Tracking

**Use native Tasks** (press `Ctrl+T` to view) for tracking implementation progress:
- Create a task entry for each plan task with proper dependencies
- Tasks persist across sessions — if the session is interrupted, progress is preserved
- Set `CLAUDE_CODE_TASK_LIST_ID=project-[name]` to share task state across sessions

**Fallback:** If native Tasks are not available, use TodoWrite for in-session tracking.

### Step 5: Execute Phase by Phase

For each phase:

1. **Announce the phase** with task list
2. **Group tasks by dependencies**:
   - Independent tasks within a phase → execute in parallel (per selected strategy)
   - Dependent tasks → execute sequentially
3. **For each task**, follow the executable format:
   - Read the **Action** field for what to do
   - Implement the change
   - Run the **Verify** check
   - Confirm against **Done when** criteria
4. **Mark completed tasks** immediately (in native Tasks and plan file)
5. **Handle deviations** using the rules below

### Step 6: Deviation Rules

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

**Agent Teams deviation handling:** Teammates should message the team lead when they encounter ASK-level deviations. The lead coordinates with the user and broadcasts the decision to all teammates.

### Step 7: Update State

After each phase:
- Update `.project-context/state.md` with current position
- Update `.project-context/progress.md` with completed items
- Update plan file status (Planning → In Progress → Completed)
- Mark native Tasks as completed

### Step 8: Summary

```
Implementation Complete!

Phases: [X/Y] completed
Tasks: [N] completed, [M] skipped
Execution: [Agent Teams with N teammates / Task subagents / Sequential]

Files created:
- path/to/new-file.ts

Files modified:
- path/to/existing.ts

Next steps:
1. [Testing recommendations]
2. [Consider running /project-context:retro to capture learnings]
```

## Best Practices

- **Confirm before starting** — Never implement without user approval
- **Follow existing patterns** — Read architecture.md and patterns.md
- **Atomic progress** — Update state after each task, not just at the end
- **Deviation rules** — Auto-fix bugs, ask about architecture changes
- **Fresh context** — Use Agent Teams or subagents for independent tasks to avoid context degradation
- **Persistent tracking** — Use native Tasks so progress survives session interruptions
- **Use `--solo` for small plans** — Agent Teams overhead isn't worth it for 1-2 tasks
