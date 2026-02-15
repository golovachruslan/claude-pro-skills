---
name: project-context:config
description: View and manage post-task action configuration in .project-context/config.json. Add, remove, enable, or disable automated actions that run after task/phase/plan completion.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# Manage Post-Task Configuration

View and manage `.project-context/config.json` for automated post-task actions.

## Usage

```
/project-context:config                  # Show current configuration status
/project-context:config add              # Add a new post-task action (interactive)
/project-context:config remove <name>    # Remove an action by name
/project-context:config enable           # Enable post-task actions
/project-context:config disable          # Disable post-task actions
/project-context:config validate         # Validate config.json structure
/project-context:config reset            # Reset to defaults (disabled, empty actions)
```

## Workflow: Show Status (default)

1. Read `.project-context/config.json`
2. If not found, tell user to run `/project-context:init` or offer to create a default config
3. Present status:

```
Post-Task Configuration
  Status: enabled
  Actions: 3 configured

  1. run-tests (shell, task-complete, blocking)
     npm test -- --related
     File pattern: *.ts

  2. lint-check (shell, task-complete, blocking)
     npx eslint $CHANGED_FILES

  3. auto-retro (command, plan-complete, non-blocking)
     /project-context:retro
```

## Workflow: Add Action

Use AskUserQuestion to gather details:

1. **Name** — identifier for the action (hyphen-case, e.g., `run-tests`)
2. **Type** — ask with options:
   - `shell` — Run a bash command (e.g., `npm test`)
   - `prompt` — Send a prompt to Claude (e.g., review changes)
   - `skill` — Invoke a skill (e.g., `project-context:retro`)
   - `command` — Run a slash command (e.g., `/project-context:retro`)
3. **Value** — the command/prompt/skill to run
4. **Trigger** — ask with options:
   - `task-complete` — After each task
   - `phase-complete` — After each phase
   - `plan-complete` — After entire plan
   - `session-end` — When pausing
5. **Blocking** — should execution wait for this action? (default: yes)
6. **Failure behavior** — ask with options:
   - `ask` — Prompt user on failure (default)
   - `warn` — Log warning, continue
   - `stop` — Halt all remaining actions
   - `retry` — Retry once, then ask
7. **File pattern** (optional) — glob to filter by changed files (e.g., `*.ts`)

After gathering inputs:
1. Build the action object
2. Read current config.json
3. Append action to the `postTask.actions` array
4. If `postTask.enabled` is false, ask user if they want to enable it now
5. Write updated config.json
6. Run validation: `python project-context/scripts/validate_config.py --file .project-context/config.json`
7. Confirm addition

## Workflow: Remove Action

1. Read config.json
2. Find action with matching name (case-sensitive)
3. If not found, list available action names
4. Remove the action from the array
5. Write updated config.json
6. Confirm removal

## Workflow: Enable / Disable

1. Read config.json
2. Set `postTask.enabled` to `true` or `false`
3. Write updated config.json
4. Confirm: "Post-task actions [enabled/disabled]. [N] actions configured."

## Workflow: Validate

Run the validation script:

```bash
python project-context/scripts/validate_config.py --file .project-context/config.json
```

Parse JSON output and present human-readable results:
- Show valid/invalid status
- List any errors with field paths
- List any warnings
- Show summary: N actions, triggers used, enabled status

## Workflow: Reset

1. Confirm with user: "This will reset config.json to defaults (disabled, no actions). Continue?"
2. Write default config:

```json
{
  "postTask": {
    "enabled": false,
    "actions": []
  }
}
```

3. Confirm reset

## Config Not Found

If `.project-context/config.json` doesn't exist:
1. Check if `.project-context/` directory exists
2. If directory exists: offer to create default config.json
3. If directory missing: suggest running `/project-context:init` first
