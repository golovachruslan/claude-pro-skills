# Project Context Hooks

Optional hooks for automating project context workflows.

## Available Hooks

### validate-plan-hook.sh

Automatically validates plan files when saved to `.project-context/plans/`.

**Triggers on:** `PostToolUse` (Write tool)
**Filters:** Only runs for `.md` files in `.project-context/plans/`

## Setup

Add hook configuration to your Claude Code settings.

### Option 1: Project-level settings

Add to `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "project-context/hooks/validate-plan-hook.sh"
          }
        ]
      }
    ]
  }
}
```

### Option 2: User-level settings

Add to `~/.claude/settings.json` for all projects:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/project-context/hooks/validate-plan-hook.sh"
          }
        ]
      }
    ]
  }
}
```

## How It Works

1. When Claude uses the Write tool to save a file
2. The hook checks if the file is in `.project-context/plans/` and ends with `.md`
3. If yes, runs `validate_plan.py` to check plan quality
4. Validation results appear after the file is saved

## Dependencies

- `jq` - for parsing JSON input (usually pre-installed on most systems)
- Python 3 - for running the validation script

## Troubleshooting

### Hook not running

1. Check hook is registered: `cat .claude/settings.json`
2. Ensure script is executable: `chmod +x project-context/hooks/validate-plan-hook.sh`
3. Check Claude Code version supports hooks

### Validation script not found

If you see "validate_plan.py not found", ensure the project-context plugin is installed and the path is correct relative to your project root.
