---
name: project-context:validate-plan
description: Validate a plan file for completeness and quality
allowed-tools:
  - Read
  - Glob
---

# Validate Plan

Verify that a plan meets quality standards before implementation.

## Usage

```
/project-context:validate-plan [path-to-plan]
```

If no path provided, validates the most recently modified plan in `.project-context/plans/`.

## Workflow

1. **Locate the plan** - Use provided path or find most recent
2. **Read the plan** content
3. **Check against criteria** from plan-verification skill
4. **Report results** and offer to fix issues

Use the `plan-verification` skill criteria to validate.
