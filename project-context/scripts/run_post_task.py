#!/usr/bin/env python3
"""
Resolve and optionally execute post-task actions from .project-context/config.json.

Handles variable interpolation, file-pattern matching, and shell execution.
For prompt/skill/command types, returns resolved values for the skill to execute.

Usage:
    python run_post_task.py --config .project-context/config.json --trigger task-complete \
        --changed-files "src/auth.ts,src/middleware.ts" --task-name "Add auth" \
        --phase-name "Phase 1" --plan-name "auth-system" --project-dir . [--dry-run]

Returns JSON with action resolution results.
"""

import argparse
import json
import os
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path


VALID_TRIGGERS = {"task-complete", "phase-complete", "plan-complete", "session-end"}
VALID_TYPES = {"shell", "prompt", "skill", "command"}

# Environment flag to prevent recursive post-task execution
POST_TASK_RUNNING_ENV = "POST_TASK_RUNNING"


def load_config(config_path):
    """Load and parse config.json."""
    path = Path(config_path)
    if not path.exists():
        return None, f"Config file not found: {config_path}"
    try:
        config = json.loads(path.read_text())
        return config, None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in config: {e}"


def match_file_pattern(pattern, changed_files):
    """Match changed files against a glob pattern.

    If the pattern contains '/', match against the full path.
    Otherwise, match against the basename only.
    """
    if not changed_files:
        return []

    use_full_path = "/" in pattern
    matched = []
    for filepath in changed_files:
        target = filepath if use_full_path else os.path.basename(filepath)
        if fnmatch(target, pattern):
            matched.append(filepath)
    return matched


def interpolate_variables(value, variables, action_type="shell"):
    """Replace built-in variables in the action value.

    For shell type: $CHANGED_FILES becomes space-separated (for command args).
    For other types: $CHANGED_FILES becomes comma-separated.
    """
    result = value
    for var_name, var_value in variables.items():
        if var_name == "$CHANGED_FILES" and isinstance(var_value, list):
            if action_type == "shell":
                replacement = " ".join(var_value)
            else:
                replacement = ",".join(var_value)
        elif isinstance(var_value, list):
            replacement = ",".join(var_value)
        else:
            replacement = str(var_value) if var_value is not None else ""
        result = result.replace(var_name, replacement)
    return result


def resolve_actions(config, trigger, changed_files, variables):
    """Resolve which actions to run for a given trigger.

    Returns a list of action results with status (pending/skipped) and resolved values.
    """
    post_task = config.get("postTask", {})

    if not post_task.get("enabled", False):
        return {
            "trigger": trigger,
            "enabled": False,
            "actions": [],
            "total": 0,
            "pending": 0,
            "skipped": 0,
            "message": "Post-task actions are disabled"
        }

    actions = post_task.get("actions", [])
    results = []

    for action in actions:
        if not isinstance(action, dict):
            continue

        action_trigger = action.get("trigger", "")
        if action_trigger != trigger:
            continue

        action_type = action.get("type", "shell")
        name = action.get("name", "unnamed")
        value = action.get("value", "")
        file_pattern = action.get("filePattern")
        blocking = action.get("blocking", True)
        on_failure = action.get("onFailure", "ask")
        description = action.get("description", "")

        result = {
            "name": name,
            "type": action_type,
            "blocking": blocking,
            "onFailure": on_failure,
            "description": description,
        }

        # Evaluate file pattern condition
        if file_pattern:
            matched = match_file_pattern(file_pattern, changed_files)
            if not matched:
                result["status"] = "skipped"
                result["reason"] = f"No files matching pattern '{file_pattern}'"
                result["matched_files"] = []
                results.append(result)
                continue
            result["matched_files"] = matched
        else:
            result["matched_files"] = changed_files

        # Interpolate variables
        resolved_value = interpolate_variables(value, variables, action_type)
        result["resolved_value"] = resolved_value
        result["original_value"] = value
        result["status"] = "pending"

        results.append(result)

    pending = sum(1 for r in results if r["status"] == "pending")
    skipped = sum(1 for r in results if r["status"] == "skipped")

    return {
        "trigger": trigger,
        "enabled": True,
        "actions": results,
        "total": len(results),
        "pending": pending,
        "skipped": skipped,
    }


def execute_shell_action(resolved_value, project_dir):
    """Execute a shell action and return the result."""
    try:
        result = subprocess.run(
            resolved_value,
            shell=True,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ, POST_TASK_RUNNING_ENV: "1"},
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout[:5000],  # Limit output size
            "stderr": result.stderr[:2000],
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 300 seconds",
            "success": False,
        }
    except Exception as e:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False,
        }


def main():
    parser = argparse.ArgumentParser(description="Resolve and run post-task actions")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--trigger", required=True, choices=sorted(VALID_TRIGGERS),
                        help="Trigger type")
    parser.add_argument("--changed-files", default="",
                        help="Comma-separated list of changed files")
    parser.add_argument("--task-name", default="", help="Current task name")
    parser.add_argument("--phase-name", default="", help="Current phase name")
    parser.add_argument("--plan-name", default="", help="Plan name")
    parser.add_argument("--project-dir", default=".", help="Project root directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Resolve actions without executing")

    args = parser.parse_args()

    # Anti-recursion check
    if os.environ.get(POST_TASK_RUNNING_ENV) == "1":
        print(json.dumps({
            "trigger": args.trigger,
            "enabled": False,
            "actions": [],
            "total": 0,
            "pending": 0,
            "skipped": 0,
            "message": "Skipped: post-task actions already running (anti-recursion)"
        }, indent=2))
        return 0

    # Load config
    config, error = load_config(args.config)
    if error:
        print(json.dumps({
            "trigger": args.trigger,
            "error": error,
            "actions": [],
            "total": 0,
            "pending": 0,
            "skipped": 0,
        }, indent=2))
        return 1

    # Parse changed files
    changed_files = [f.strip() for f in args.changed_files.split(",") if f.strip()]

    # Build variables map
    variables = {
        "$CHANGED_FILES": changed_files,
        "$TASK_NAME": args.task_name,
        "$PHASE_NAME": args.phase_name,
        "$PLAN_NAME": args.plan_name,
        "$PROJECT_DIR": args.project_dir,
    }

    # Resolve actions
    result = resolve_actions(config, args.trigger, changed_files, variables)

    # Execute shell actions if not dry-run
    if not args.dry_run:
        for action in result["actions"]:
            if action["status"] != "pending":
                continue
            if action["type"] == "shell":
                exec_result = execute_shell_action(
                    action["resolved_value"], args.project_dir
                )
                action["execution"] = exec_result
                action["status"] = "completed" if exec_result["success"] else "failed"

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
