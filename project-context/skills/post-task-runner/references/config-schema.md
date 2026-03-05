# Config Schema Reference

Complete schema documentation for `.project-context/config.json`.

## Top-Level Structure

```json
{
  "postTask": {
    "enabled": true,
    "actions": [...]
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `postTask` | object | — | Post-task automation configuration |
| `postTask.enabled` | boolean | `false` | Whether post-task actions are active |
| `postTask.actions` | array | `[]` | Ordered list of action definitions |

The config file may contain additional top-level keys in the future. Unknown keys are ignored.

## Action Schema

```json
{
  "name": "run-tests",
  "type": "shell",
  "value": "npm test -- --related $CHANGED_FILES",
  "trigger": "task-complete",
  "blocking": true,
  "onFailure": "ask",
  "filePattern": "*.ts",
  "description": "Run related tests after each task"
}
```

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `name` | string | 1-64 chars, unique across actions | Identifier for the action |
| `type` | string | `shell` \| `prompt` \| `skill` \| `command` | How the value is executed |
| `value` | string | Non-empty | The command, prompt text, skill name, or slash command |
| `trigger` | string | `task-complete` \| `phase-complete` \| `plan-complete` \| `session-end` | When this action runs |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `blocking` | boolean | `true` | Wait for completion before next action |
| `onFailure` | string | `"ask"` | Failure behavior: `ask` \| `stop` \| `warn` \| `retry` |
| `filePattern` | string | — | Glob pattern to filter by changed files |
| `description` | string | — | Human-readable description |

## Field Values

### `type`

| Value | Execution | Example `value` |
|-------|-----------|-----------------|
| `shell` | Runs as bash command via subprocess | `npm test -- --related` |
| `prompt` | Sent as text prompt to Claude | `Review changes in $CHANGED_FILES for security issues` |
| `skill` | Invoked as a named skill | `project-context:retro` |
| `command` | Invoked as a slash command | `/project-context:retro` |

### `trigger`

| Value | When Fired | Typical Use |
|-------|-----------|-------------|
| `task-complete` | After each task in a plan finishes | Unit tests, linting |
| `phase-complete` | After all tasks in a phase finish | Integration tests, state review |
| `plan-complete` | After the entire plan finishes | Full test suite, retrospective |
| `session-end` | When `/pause` is invoked | Cleanup, state export |

### `onFailure`

| Value | Behavior |
|-------|----------|
| `ask` | Present failure to user, ask: Continue / Retry / Stop |
| `stop` | Halt remaining actions, report failure |
| `warn` | Log warning, continue to next action |
| `retry` | Retry once, then fall back to `ask` on second failure |

## Built-in Variables

Available in the `value` field. Interpolated before execution.

| Variable | Description | Shell Format | Other Format |
|----------|-------------|-------------|--------------|
| `$CHANGED_FILES` | Files changed during the task | Space-separated | Comma-separated |
| `$TASK_NAME` | Current task name | String | String |
| `$PHASE_NAME` | Current phase name | String | String |
| `$PLAN_NAME` | Plan identifier | String | String |
| `$PROJECT_DIR` | Project root directory | Absolute path | Absolute path |

## Example Configurations

### Run tests after every task

```json
{
  "postTask": {
    "enabled": true,
    "actions": [
      {
        "name": "run-tests",
        "type": "shell",
        "value": "npm test",
        "trigger": "task-complete",
        "blocking": true,
        "onFailure": "ask",
        "description": "Run test suite after each completed task"
      }
    ]
  }
}
```

### Lint only TypeScript files

```json
{
  "name": "lint-ts",
  "type": "shell",
  "value": "npx eslint $CHANGED_FILES",
  "trigger": "task-complete",
  "blocking": true,
  "onFailure": "warn",
  "filePattern": "*.ts",
  "description": "Lint changed TypeScript files"
}
```

### Auto-retro after plan completion

```json
{
  "name": "auto-retro",
  "type": "command",
  "value": "/project-context:retro",
  "trigger": "plan-complete",
  "blocking": false,
  "onFailure": "warn",
  "description": "Run retrospective after plan finishes"
}
```

### Prompt-based review after each phase

```json
{
  "name": "phase-review",
  "type": "prompt",
  "value": "Review the changes made in $PHASE_NAME. Check for consistency with architecture.md and patterns.md. Flag any concerns.",
  "trigger": "phase-complete",
  "blocking": true,
  "onFailure": "warn",
  "description": "AI-driven review after each phase"
}
```

### Session-end cleanup

```json
{
  "name": "format-on-pause",
  "type": "shell",
  "value": "npx prettier --write $CHANGED_FILES",
  "trigger": "session-end",
  "blocking": true,
  "onFailure": "warn",
  "description": "Format changed files before pausing"
}
```

### Multi-action configuration

```json
{
  "postTask": {
    "enabled": true,
    "actions": [
      {
        "name": "run-tests",
        "type": "shell",
        "value": "npm test -- --related $CHANGED_FILES",
        "trigger": "task-complete",
        "blocking": true,
        "onFailure": "ask",
        "filePattern": "*.ts",
        "description": "Run related tests for changed TypeScript files"
      },
      {
        "name": "lint",
        "type": "shell",
        "value": "npx eslint $CHANGED_FILES",
        "trigger": "task-complete",
        "blocking": true,
        "onFailure": "warn",
        "filePattern": "*.{ts,tsx,js,jsx}",
        "description": "Lint changed JS/TS files"
      },
      {
        "name": "integration-tests",
        "type": "shell",
        "value": "npm run test:integration",
        "trigger": "phase-complete",
        "blocking": true,
        "onFailure": "ask",
        "description": "Run integration tests after each phase"
      },
      {
        "name": "auto-retro",
        "type": "command",
        "value": "/project-context:retro",
        "trigger": "plan-complete",
        "blocking": false,
        "onFailure": "warn",
        "description": "Capture learnings after plan completion"
      }
    ]
  }
}
```

## Validation

Validate config.json using the included script:

```bash
python project-context/scripts/validate_config.py --file .project-context/config.json
```

Returns JSON with `valid` (boolean), `issues` (array of errors/warnings), and `actions_count`.
