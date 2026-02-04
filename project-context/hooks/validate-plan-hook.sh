#!/bin/bash
# Plan Validation Hook
#
# This hook runs after Write tool calls and validates plan files
# when they are saved to .project-context/plans/
#
# Setup: Add to your .claude/settings.json:
# {
#   "hooks": {
#     "PostToolUse": [
#       {
#         "matcher": "Write",
#         "hooks": [
#           {
#             "type": "command",
#             "command": "project-context/hooks/validate-plan-hook.sh"
#           }
#         ]
#       }
#     ]
#   }
# }

# Read input from stdin (JSON with tool info)
INPUT=$(cat)

# Extract file path from Write tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Check if this is a plan file
if [[ "$FILE_PATH" == *".project-context/plans/"* && "$FILE_PATH" == *.md ]]; then
    # Run validation script
    SCRIPT_DIR="$(dirname "$0")/../skills/plan-verification/scripts"

    if [[ -f "$SCRIPT_DIR/validate_plan.py" ]]; then
        echo "Validating plan: $FILE_PATH"
        python "$SCRIPT_DIR/validate_plan.py" "$FILE_PATH"
        exit $?
    else
        echo "Warning: validate_plan.py not found at $SCRIPT_DIR"
        exit 0
    fi
fi

# Not a plan file, pass through
exit 0
