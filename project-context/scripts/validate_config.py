#!/usr/bin/env python3
"""
Validate .project-context/config.json structure and post-task prompt definitions.

Usage:
    python validate_config.py [--dir DIR]
    python validate_config.py --file path/to/config.json

Returns JSON with validation results.
"""

import argparse
import json
import sys
from pathlib import Path

# Valid values for each field
VALID_TYPES = {"shell", "prompt", "skill", "command"}
VALID_TRIGGERS = {"task-complete", "phase-complete", "plan-complete", "session-end"}
VALID_ON_FAILURE = {"ask", "stop", "warn", "retry"}
VALID_VARIABLES = {"$CHANGED_FILES", "$TASK_NAME", "$PHASE_NAME", "$PLAN_NAME", "$PROJECT_DIR"}

# Schema for a single action
REQUIRED_ACTION_FIELDS = {"name", "type", "value", "trigger"}
OPTIONAL_ACTION_FIELDS = {"blocking", "onFailure", "filePattern", "description"}
ALL_ACTION_FIELDS = REQUIRED_ACTION_FIELDS | OPTIONAL_ACTION_FIELDS


def validate_action(action, index):
    """Validate a single post-task action definition."""
    issues = []
    prefix = f"actions[{index}]"

    if not isinstance(action, dict):
        return [{"path": prefix, "severity": "error", "message": "Action must be an object"}]

    # Check required fields
    for field in REQUIRED_ACTION_FIELDS:
        if field not in action:
            issues.append({
                "path": f"{prefix}.{field}",
                "severity": "error",
                "message": f"Missing required field '{field}'"
            })

    # Check for unknown fields
    unknown = set(action.keys()) - ALL_ACTION_FIELDS
    if unknown:
        issues.append({
            "path": prefix,
            "severity": "warning",
            "message": f"Unknown fields: {', '.join(sorted(unknown))}"
        })

    # Validate name
    name = action.get("name", "")
    if isinstance(name, str):
        if not name.strip():
            issues.append({
                "path": f"{prefix}.name",
                "severity": "error",
                "message": "Name cannot be empty"
            })
        elif len(name) > 64:
            issues.append({
                "path": f"{prefix}.name",
                "severity": "error",
                "message": f"Name too long ({len(name)} chars, max 64)"
            })
    else:
        issues.append({
            "path": f"{prefix}.name",
            "severity": "error",
            "message": "Name must be a string"
        })

    # Validate type
    action_type = action.get("type", "")
    if action_type and action_type not in VALID_TYPES:
        issues.append({
            "path": f"{prefix}.type",
            "severity": "error",
            "message": f"Invalid type '{action_type}'. Must be one of: {', '.join(sorted(VALID_TYPES))}"
        })

    # Validate value
    value = action.get("value", "")
    if isinstance(value, str):
        if not value.strip():
            issues.append({
                "path": f"{prefix}.value",
                "severity": "error",
                "message": "Value cannot be empty"
            })
    else:
        issues.append({
            "path": f"{prefix}.value",
            "severity": "error",
            "message": "Value must be a string"
        })

    # Validate trigger
    trigger = action.get("trigger", "")
    if trigger and trigger not in VALID_TRIGGERS:
        issues.append({
            "path": f"{prefix}.trigger",
            "severity": "error",
            "message": f"Invalid trigger '{trigger}'. Must be one of: {', '.join(sorted(VALID_TRIGGERS))}"
        })

    # Validate blocking (optional, defaults to true)
    if "blocking" in action and not isinstance(action["blocking"], bool):
        issues.append({
            "path": f"{prefix}.blocking",
            "severity": "error",
            "message": "blocking must be a boolean"
        })

    # Validate onFailure
    on_failure = action.get("onFailure", "")
    if on_failure and on_failure not in VALID_ON_FAILURE:
        issues.append({
            "path": f"{prefix}.onFailure",
            "severity": "error",
            "message": f"Invalid onFailure '{on_failure}'. Must be one of: {', '.join(sorted(VALID_ON_FAILURE))}"
        })

    # Validate filePattern (optional glob pattern)
    file_pattern = action.get("filePattern")
    if file_pattern is not None:
        if not isinstance(file_pattern, str):
            issues.append({
                "path": f"{prefix}.filePattern",
                "severity": "error",
                "message": "filePattern must be a string (glob pattern)"
            })
        elif not file_pattern.strip():
            issues.append({
                "path": f"{prefix}.filePattern",
                "severity": "warning",
                "message": "filePattern is empty — action will never match. Remove field or set a pattern."
            })

    # Type-specific validation
    if action_type == "command" and isinstance(value, str) and value.strip():
        if not value.startswith("/"):
            issues.append({
                "path": f"{prefix}.value",
                "severity": "warning",
                "message": f"Command '{value}' doesn't start with '/'. Commands should be slash commands like '/project-context:retro'"
            })

    if action_type == "shell" and isinstance(value, str):
        # Warn about potentially dangerous commands
        dangerous = ["rm -rf", "sudo", "> /dev/", "mkfs", "dd if="]
        for d in dangerous:
            if d in value:
                issues.append({
                    "path": f"{prefix}.value",
                    "severity": "warning",
                    "message": f"Shell command contains potentially dangerous pattern: '{d}'"
                })

    return issues


def validate_config(config_path):
    """Validate a config.json file."""
    config_path = Path(config_path)
    issues = []

    if not config_path.exists():
        return {
            "valid": False,
            "issues": [{"path": "config.json", "severity": "error", "message": "File not found"}]
        }

    # Parse JSON
    try:
        content = config_path.read_text()
        config = json.loads(content)
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "issues": [{"path": "config.json", "severity": "error", "message": f"Invalid JSON: {e}"}]
        }

    if not isinstance(config, dict):
        return {
            "valid": False,
            "issues": [{"path": "config.json", "severity": "error", "message": "Config must be a JSON object"}]
        }

    # Check for postTask section
    post_task = config.get("postTask")
    if post_task is None:
        issues.append({
            "path": "postTask",
            "severity": "warning",
            "message": "No 'postTask' section found. Config is valid but has no post-task actions."
        })
        return {"valid": True, "issues": issues, "actions_count": 0}

    if not isinstance(post_task, dict):
        return {
            "valid": False,
            "issues": [{"path": "postTask", "severity": "error", "message": "postTask must be an object"}]
        }

    # Validate enabled flag
    enabled = post_task.get("enabled", True)
    if not isinstance(enabled, bool):
        issues.append({
            "path": "postTask.enabled",
            "severity": "error",
            "message": "enabled must be a boolean"
        })

    # Validate actions array
    actions = post_task.get("actions", [])
    if not isinstance(actions, list):
        return {
            "valid": False,
            "issues": [{"path": "postTask.actions", "severity": "error", "message": "actions must be an array"}]
        }

    if len(actions) == 0:
        issues.append({
            "path": "postTask.actions",
            "severity": "warning",
            "message": "actions array is empty"
        })

    # Check for duplicate names
    names = [a.get("name") for a in actions if isinstance(a, dict) and "name" in a]
    seen = set()
    for name in names:
        if name in seen:
            issues.append({
                "path": "postTask.actions",
                "severity": "error",
                "message": f"Duplicate action name: '{name}'"
            })
        seen.add(name)

    # Validate each action
    for i, action in enumerate(actions):
        issues.extend(validate_action(action, i))

    valid = not any(i["severity"] == "error" for i in issues)
    return {
        "valid": valid,
        "issues": issues,
        "actions_count": len(actions),
        "enabled": enabled if isinstance(enabled, bool) else None,
        "triggers_used": list(set(
            a.get("trigger") for a in actions
            if isinstance(a, dict) and a.get("trigger") in VALID_TRIGGERS
        ))
    }


def main():
    parser = argparse.ArgumentParser(description="Validate .project-context/config.json")
    parser.add_argument("--dir", default=".", help="Project root directory")
    parser.add_argument("--file", help="Direct path to config.json")
    args = parser.parse_args()

    if args.file:
        config_path = Path(args.file)
    else:
        config_path = Path(args.dir) / ".project-context" / "config.json"

    result = validate_config(config_path)
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
