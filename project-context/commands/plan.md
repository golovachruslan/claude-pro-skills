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

Help me plan this feature or project. Use the planner skill to:

1. Gather requirements through clarifying questions (never assume or guess)
2. Understand technical constraints and preferences
3. Create a structured implementation plan with phases
4. Identify risks, trade-offs, and dependencies
5. Define clear success criteria

If the user has already provided some context in this conversation, incorporate it and ask about what's still unclear.

Force the use of AskUserQuestion tool to clarify any ambiguities before proposing solutions.

## Saving Plans

After creating the plan, **always ask the user** if they want to save it:

```
Would you like me to save this plan?

Default location: `.project-context/plans/[feature-name].md`

Options:
1. Yes, save to default location
2. Yes, save to a different location: [specify path]
3. No, don't save
```

If the user confirms:
1. Create the `plans/` directory under `.project-context/` if it doesn't exist
2. Save the plan with a descriptive filename (e.g., `dark-mode-implementation.md`)
3. Update `.project-context/progress.md` to reference the new plan
