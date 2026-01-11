---
name: project-context:plan
description: Start planning a feature or project with structured requirements gathering
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
---

# Plan Feature or Project

Help me plan this feature or project. Use the `project-context:planner` skill to:

1. Gather requirements through clarifying questions (never assume or guess)
2. Understand technical constraints and preferences
3. Create a structured implementation plan with phases
4. Identify risks, trade-offs, and dependencies
5. Define clear success criteria

If the user has already provided some context in this conversation, incorporate it and ask about what's still unclear.

Force the use of AskUserQuestion tool to clarify any ambiguities before proposing solutions.

## Saving Plans

After creating the plan, **always ask the user** if they want to save it.

### Filename Selection

**If user provided a feature name during planning:**
- Use the provided name directly (convert to hyphen-case)
- Example: "Dark Mode Toggle" → `dark-mode-toggle.md`

**If no explicit feature name was provided:**
- Generate 2-3 descriptive filename options based on the plan content
- Ask user to choose or provide their own

```
Would you like me to save this plan?

Suggested filenames:
1. user-authentication-flow.md
2. auth-feature-implementation.md
3. login-system-plan.md

Options:
- Enter 1, 2, or 3 to use a suggested name
- Type your own filename
- Type "no" to skip saving
```

### Save Process

If the user confirms:
1. Create the `plans/` directory under `.project-context/` if it doesn't exist
2. Save the plan with the selected filename in hyphen-case
3. Update `.project-context/progress.md` to reference the new plan
