---
name: post-task-runner
description: Execute configured post-task actions after task/phase/plan completion or session end. Use when the implement or pause command needs to run automated actions from .project-context/config.json — reads config, resolves variables ($CHANGED_FILES, $TASK_NAME, etc.), evaluates filePattern conditions, and runs shell/prompt/skill/command actions sequentially.
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Skill
---

# Post-Task Action Runner

Orchestrates execution of post-task actions configured in `.project-context/config.json`.

## When This Skill Runs

Called internally by:
- **`/project-context:implement`** — after each task (`task-complete`), phase (`phase-complete`), and plan (`plan-complete`)
- **`/project-context:pause`** — before saving state (`session-end`)

## Inputs

The calling command provides:
- **trigger**: `task-complete` | `phase-complete` | `plan-complete` | `session-end`
- **changed_files**: Files modified during the task/phase (from `git diff --name-only`)
- **task_name**: Current task name (empty for phase/plan/session triggers)
- **phase_name**: Current phase name
- **plan_name**: Plan identifier

## Execution Workflow

### 1. Resolve Actions (Dry Run)

Run the helper script to resolve variables and evaluate conditions:

```bash
python project-context/scripts/run_post_task.py \
  --config .project-context/config.json \
  --trigger [trigger] \
  --changed-files "[comma-separated files]" \
  --task-name "[name]" \
  --phase-name "[phase]" \
  --plan-name "[plan]" \
  --project-dir . \
  --dry-run
```

Parse the JSON output. If `enabled` is false or `pending` is 0, return immediately.

### 2. Execute Each Pending Action

Process actions in array order:

| Type | Execution Method |
|------|-----------------|
| `shell` | Run resolved command via Bash tool. Capture exit code and output. |
| `prompt` | Process the resolved value as a prompt — interpret and act on it in context. |
| `skill` | Invoke the named skill via Skill tool (e.g., `project-context:retro`). |
| `command` | Invoke the slash command via Skill tool (strip leading `/`). |

For **blocking** actions (`blocking: true`, the default), wait for completion before proceeding to the next action.

### 3. Handle Failures

When an action fails (non-zero exit for shell, error for others):

| `onFailure` | Behavior |
|-------------|----------|
| `ask` (default) | Present the failure and ask: Continue / Retry / Stop |
| `stop` | Halt all remaining actions, report failure |
| `warn` | Log warning, continue to next action |
| `retry` | Retry once, then fall back to `ask` if it fails again |

### 4. Report Summary

Output a concise summary:

```
Post-Task Actions ([trigger]):
  [pass] run-tests — npm test passed (2.3s)
  [skip] lint-check — no matching files for *.py
  [fail] type-check — tsc found 3 errors → user chose to continue
```

## Built-in Variables

| Variable | Source | Example |
|----------|--------|---------|
| `$CHANGED_FILES` | `git diff --name-only` from task start | `src/auth.ts src/middleware.ts` (space-separated for shell, comma-separated for others) |
| `$TASK_NAME` | Current task being executed | `Add auth middleware` |
| `$PHASE_NAME` | Current phase name | `Phase 1: Core Auth` |
| `$PLAN_NAME` | Plan file name or title | `auth-system` |
| `$PROJECT_DIR` | Working directory | `/home/user/myproject` |

## File-Pattern Matching

When an action has `filePattern`, it only runs if at least one changed file matches:

- Pattern without `/` (e.g., `*.ts`) → matches against **basename** only
- Pattern with `/` (e.g., `src/api/*.ts`) → matches against **full path**

If no files match, the action is skipped silently with a log note.

## Anti-Recursion Protection

The `POST_TASK_RUNNING` environment variable prevents re-entrant execution. If a post-task action triggers another implement cycle, the nested post-task runner will detect the flag and skip execution.

## Agent Teams Considerations

When Agent Teams are active, post-task actions run on the **team lead** only. After a teammate completes a task, the lead gathers changed files from the teammate's report, then runs the configured post-task actions centrally. This prevents duplicated work and conflicts.
