---
name: project-context:implement
description: "Use when users want to execute an implementation plan. Triggers: 'implement this plan', 'start implementing', 'execute the plan', 'build this'. Executes plans with multi-agent parallelism and enforces context file updates on completion."
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
hooks:
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: agent
          prompt: |
            Check if the file just edited is a plan in .project-context/plans/.
            Input: $ARGUMENTS

            If it's NOT a plan file, return {"ok": true}.

            If it IS a plan file, check if the edit changed the Status field to "Completed".
            To determine this, read the plan file and look for "**Status:** Completed".

            If status is NOT being set to Completed → return {"ok": true} (implementation still in progress).

            If status IS set to Completed, verify that context files were updated:
            1. Read .project-context/state.md — it should reflect post-implementation state
               (should NOT still reference "Planning" or "Implementing" as current focus
               without noting completion).
            2. Read .project-context/progress.md — it should have a recent entry referencing
               the completed feature/plan.

            If BOTH files appear updated with completion info → return {"ok": true}
            If either file is missing completion info → return {"ok": false,
              "reason": "Implementation marked complete but context files not synced. You MUST update state.md (set current focus to completed feature, set next action) and progress.md (add completed items with date) before finishing. This is mandatory per Step 7 of the implement workflow."}
          statusMessage: "Verifying context sync..."
          timeout: 90
---

# Implementation Skill

This skill enforces context file synchronization when plans are implemented. It works alongside the `/project-context:implement` command.

## Context Sync Enforcement

The PostToolUse hook on this skill monitors plan file edits. When a plan's status is changed to "Completed", the hook verifies that `.project-context/state.md` and `.project-context/progress.md` have been updated accordingly.

If context files are not updated, the hook returns an error instructing the agent to update them before proceeding.

## Required Updates on Plan Completion

When marking a plan as completed, you MUST also update:

1. **state.md** — Current focus, next action, recently completed
2. **progress.md** — Completed items with dates and deliverables
3. **patterns.md** — Any new patterns discovered (if applicable)

See the `/project-context:implement` command for full workflow details.
