# Project Context Hooks

The `planner` skill has a built-in agent hook that automatically validates plans after saving.

## How It Works

When a plan is saved to `.project-context/plans/`, the planner skill's `PostToolUse` hook triggers an agent that:

1. Checks if the written file is a plan
2. Reads and validates the plan against quality criteria
3. Returns pass/fail with specific issues

## Configuration

The hook is defined in the planner skill's frontmatter:

```yaml
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: agent
          prompt: |
            Check if the file just written is a plan...
            [validation criteria]
          statusMessage: "Validating plan..."
```

No additional setup required - validation runs automatically when using `/project-context:plan`.

## Manual Validation

Use `/project-context:validate-plan` to manually validate any plan file.
