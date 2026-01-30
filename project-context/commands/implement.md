---
name: project-context:implement
description: Implement a feature plan step by step. Provide a plan file path or reference a plan from the conversation.
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

Execute an implementation plan step by step, tracking progress and asking for guidance when needed.

## Task Tool Usage

**Check if your available tools include `Task`.** If you have access to the Task tool, use Task subagents for:

- **Codebase exploration**: Use `subagent_type=Explore` to understand existing patterns, find related code, and gather context before making changes
- **Parallel implementation**: Launch multiple Task subagents for independent tasks within a phase to speed up implementation
- **Complex sub-tasks**: Delegate multi-step sub-tasks to specialized agents

Example usage:
```
Task(subagent_type="Explore", prompt="Find all places where user preferences are stored and understand the data flow")
Task(subagent_type="Bash", prompt="Run the test suite and report any failures")
```

Benefits of using Task subagents:
- Parallel execution of independent tasks
- Reduced context usage for complex operations
- Specialized agents for different task types (Explore, Bash, Plan)

**If `Task` is not in your available tools**, proceed with direct tool operations (Glob, Grep, Read, Bash) as fallback.

## Usage

```
/project-context:implement [plan-path]
```

**Arguments:**
- `plan-path` (optional): Path to a plan file (e.g., `.project-context/plans/feature-name.md`)

## Workflow

### Step 1: Locate the Plan

**If plan path is provided:**
1. Read the specified plan file
2. Validate it contains implementation phases/tasks
3. Proceed to implementation

**If no plan path provided:**
1. Check if there's a plan in the current conversation
2. Check for saved plans in `.project-context/plans/`:
   ```bash
   ls .project-context/plans/*.md 2>/dev/null
   ```
3. If plans found, ask user which one to implement
4. If no plans found and no plan in conversation, inform user:
   ```
   No plan found. You can:
   1. Run `/project-context:plan` to create a new plan
   2. Provide a plan file path: `/project-context:implement path/to/plan.md`
   ```

### Step 2: Confirm Implementation

Before starting, use AskUserQuestion to confirm:

```
I found the following plan: [Plan Name]

Phases:
1. [Phase 1 name] - [X tasks]
2. [Phase 2 name] - [X tasks]
...

Would you like me to implement this plan?

Options:
1. Yes, implement all phases
2. Yes, but only implement Phase [N]
3. Yes, but let me pick specific tasks
4. No, cancel
```

**Do not proceed without user confirmation.**

### Step 3: Read Project Context

Before implementing, read existing context to ensure consistency:

```bash
ls .project-context/*.md 2>/dev/null
```

If context exists, read:
- `.project-context/architecture.md` - Follow existing patterns
- `.project-context/patterns.md` - Respect established conventions
- `.project-context/progress.md` - Understand current state

### Step 4: Implement Phase by Phase

For each phase in the plan:

1. **Announce the phase:**
   ```
   Starting Phase [N]: [Phase Name]
   Tasks in this phase:
   - [ ] Task 1
   - [ ] Task 2
   ...
   ```

2. **Implement each task:**
   - Follow the plan's technical approach
   - Use existing patterns from project context
   - Create/modify files as needed
   - Run tests if applicable

3. **Mark completed tasks:**
   ```
   Completed: [Task description]
   ```

4. **Handle blockers:**
   If you encounter an issue that blocks progress:
   ```
   Blocker encountered: [Description]

   Options:
   1. Skip this task and continue
   2. Try alternative approach: [suggestion]
   3. Stop and discuss
   ```

5. **Phase completion:**
   ```
   Phase [N] complete!
   - [X] tasks completed
   - [Y] tasks skipped (if any)

   Proceeding to Phase [N+1]...
   ```

### Step 5: Update Progress

After completing implementation (or each phase):

1. **Update `.project-context/progress.md`:**
   - Move completed items to "Completed" section
   - Update current focus
   - Note any remaining work

2. **Update plan file status** (if saved):
   - Change status from "Planning" to "In Progress" or "Completed"
   - Add completion notes

3. **Update `.project-context/patterns.md`** if new patterns emerged

### Step 6: Summary

After implementation, provide a summary:

```
Implementation Complete!

Phases completed: [X/Y]
Tasks completed: [N]
Tasks skipped: [M] (if any)

Files created:
- path/to/file1.ts
- path/to/file2.ts

Files modified:
- path/to/existing1.ts
- path/to/existing2.ts

Next steps:
1. [Suggested next action]
2. [Testing recommendations]
```

## Best Practices

### DO:
- Confirm with user before starting
- Announce each phase/task before starting
- Follow existing project patterns and conventions
- Update progress after each phase
- Ask for guidance when encountering ambiguity
- Run relevant tests after changes
- Provide clear summary at the end

### DON'T:
- Start implementing without user confirmation
- Skip reading project context
- Ignore established patterns
- Make major architectural decisions without asking
- Continue past blockers without user input
- Forget to update progress tracking

## Examples

### Example 1: Implement from saved plan file

```
User: /project-context:implement .project-context/plans/dark-mode.md
Assistant: I found the Dark Mode plan. It has 3 phases with 12 total tasks.
Would you like me to implement this plan?
User: Yes, implement all phases
Assistant: Starting Phase 1: Core Theme Setup...
```

### Example 2: Implement plan from conversation

```
User: /project-context:implement
Assistant: I found a plan in our conversation for "User Authentication Feature".
Would you like me to implement this plan?
User: Yes
Assistant: Starting implementation...
```

### Example 3: No plan found

```
User: /project-context:implement
Assistant: No plan found. You can:
1. Run /project-context:plan to create a new plan
2. Provide a plan file path: /project-context:implement path/to/plan.md
```