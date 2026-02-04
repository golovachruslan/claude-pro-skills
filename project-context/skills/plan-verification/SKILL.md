---
name: plan-verification
description: "Use after the planner skill completes to verify plan quality. Triggers include: 'verify this plan', 'check the plan', 'validate plan', or automatically after saving a plan. Checks completeness, actionability, scope clarity, and risk coverage."
allowed-tools:
  - Read
  - Glob
---

# Plan Verification Skill

Validate plans created by the planner skill to ensure they are complete, actionable, and ready for implementation.

## When to Use

This skill should be triggered:
1. **Automatically** after the planner skill saves a plan to `.project-context/plans/`
2. **On demand** when user asks to verify/validate a plan
3. **Before implementation** to confirm plan readiness

## Verification Workflow

### 1. Locate the Plan

If plan path not provided, find the most recent plan:

```bash
ls -t .project-context/plans/*.md 2>/dev/null | head -1
```

Or ask user which plan to verify if multiple exist.

### 2. Run Validation Script

Use the validation script to check plan structure and quality:

```bash
python project-context/skills/plan-verification/scripts/validate_plan.py <plan-path>
```

The script returns JSON with validation results.

### 3. Report Results

Present findings clearly to the user.

## Validation Criteria

### Required Sections (Structure Check)

Plans must have these sections to be considered complete:

| Section | Purpose | Required |
|---------|---------|----------|
| Overview | What and why | Yes |
| Requirements | Functional/non-functional needs | Yes |
| Technical Approach | How it will be built | Yes |
| Implementation Phases | Phased tasks with checkboxes | Yes |
| Success Criteria | How to measure done | Yes |

### Quality Checks

#### 1. Completeness
- No empty sections
- No unfilled `[placeholder]` or `[TODO]` text
- No `TBD` or `TBA` markers left in content

#### 2. Actionability
- Implementation phases have concrete tasks (checkbox items `- [ ]`)
- Tasks are specific, not vague (e.g., "Implement auth" vs "Do the thing")
- Each phase has a clear goal statement

#### 3. Scope Clarity
- Has explicit scope boundaries (in-scope / out-of-scope)
- Or has "Future Enhancements" / "Not in Scope" section
- MVP vs future phases are distinguished

#### 4. Risk Awareness
- Has at least one risk identified
- Risks have mitigation strategies
- Or explicitly states "Low-risk feature, no significant risks identified"

#### 5. Measurability
- Success criteria are specific and measurable
- Not vague like "works well" or "users are happy"
- Should answer: "How do we know this is done?"

#### 6. Dependencies
- External dependencies are listed
- Internal dependencies (other work needed first) are identified
- Or explicitly states "No dependencies"

## Validation Output Format

### All Checks Pass

```
Plan Verification: PASSED

plan-name.md is ready for implementation.

Summary:
- 5 required sections present
- 12 actionable tasks defined
- 2 risks identified with mitigations
- Clear success criteria defined
```

### Issues Found

```
Plan Verification: NEEDS ATTENTION

plan-name.md has 3 issues to address:

ERRORS (must fix):
1. Missing section: Success Criteria
   - Add measurable criteria for when the feature is complete

2. Empty section: Risks & Mitigation
   - Add at least one risk or state "No significant risks identified"

WARNINGS (recommended):
1. Placeholder found: "[TBD]" in Technical Approach
   - Fill in the specific technology choice

Suggestions:
- Consider adding more specific tasks to Phase 2
- Success criteria could be more measurable

Run verification again after fixing issues.
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| ERROR | Plan cannot proceed without fixing | Must address before implementation |
| WARNING | Quality issue, may cause problems | Strongly recommended to fix |
| SUGGESTION | Could be improved | Optional enhancement |

## Integration with Planner Workflow

After the planner skill saves a plan, it should invoke this skill:

```
Plan saved to .project-context/plans/feature-name.md

Running verification...

[Verification results appear here]
```

## Manual Verification Command

Users can also run verification manually:

```
/project-context:validate-plan [path-to-plan]
```

If no path provided, verifies the most recently created plan.

## Handling Verification Failures

When verification finds issues:

1. **Present issues clearly** with specific line references if possible
2. **Offer to help fix** - "Would you like me to help address these issues?"
3. **If user agrees**, update the plan to fix issues
4. **Re-run verification** after fixes to confirm resolution

## Example Verification Session

**Automatic trigger after plan save:**

```
Plan saved to .project-context/plans/user-notifications.md

Running plan verification...

Plan Verification: NEEDS ATTENTION

user-notifications.md has 2 issues:

ERRORS:
1. Missing section: Success Criteria
   - How will you know the notification system is complete?

WARNINGS:
1. Phase 2 has no tasks defined
   - Add specific tasks or mark as "Tasks to be defined based on Phase 1 learnings"

Would you like me to help add these sections?
```

**User response:** "Yes, help me add success criteria"

**Assistant adds success criteria and re-verifies:**

```
Updated success criteria in the plan.

Re-running verification...

Plan Verification: PASSED

user-notifications.md is now ready for implementation.

Remaining note:
- Phase 2 tasks are intentionally deferred (marked as such)
```

## Quick Reference

### Validation Command
```bash
python project-context/skills/plan-verification/scripts/validate_plan.py <plan.md>
```

### Output Format (JSON)
```json
{
  "status": "pass|fail|warning",
  "errors": [...],
  "warnings": [...],
  "suggestions": [...],
  "summary": {
    "sections_found": 5,
    "tasks_count": 12,
    "risks_count": 2
  }
}
```

### Quick Checks
- Required sections present?
- All placeholders filled?
- Tasks have checkboxes?
- At least one risk or explicit "no risks"?
- Success criteria are measurable?
