---
name: project-context:validate-plan
description: Validate a plan file for completeness and quality before implementation
allowed-tools:
  - Read
  - Glob
  - Bash
---

# Validate Plan

Verify that a plan meets quality standards before implementation.

## Usage

```
/project-context:validate-plan [path-to-plan]
```

If no path provided, validates the most recently modified plan in `.project-context/plans/`.

## Workflow

1. **Locate the plan file**

   If path provided, use it directly. Otherwise find the most recent:
   ```bash
   ls -t .project-context/plans/*.md 2>/dev/null | head -1
   ```

   If multiple plans exist and no path given, list them and ask user to choose.

2. **Run validation script**

   ```bash
   python project-context/skills/plan-verification/scripts/validate_plan.py <plan-path>
   ```

3. **Present results** to the user

4. **Offer to fix issues** if any errors or warnings are found

## Example

```
> /project-context:validate-plan

Found plans:
1. user-notifications.md (modified 2 hours ago)
2. dark-mode-feature.md (modified 3 days ago)

Validating most recent: user-notifications.md

Plan Verification: NEEDS ATTENTION

ERRORS (must fix):
1. Missing section: Success Criteria

WARNINGS:
1. Phase 2 has no tasks defined

Would you like me to help fix these issues?
```
