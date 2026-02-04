#!/bin/bash
# Plan Validation Hook Script
#
# Called by the planner skill after a Write tool completes.
# Validates plan files written to .project-context/plans/

set -e

# Read JSON input from stdin
INPUT=$(cat)

# Extract file path from Write tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Check if this is a plan file
if [[ "$FILE_PATH" == *".project-context/plans/"* && "$FILE_PATH" == *.md ]]; then
    # Get the directory where this script lives
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Run validation script
    if [[ -f "$SCRIPT_DIR/validate_plan.py" ]]; then
        RESULT=$(python "$SCRIPT_DIR/validate_plan.py" "$FILE_PATH" --json 2>&1) || true

        # Extract status from JSON result
        STATUS=$(echo "$RESULT" | jq -r '.status // "unknown"' 2>/dev/null || echo "unknown")

        if [[ "$STATUS" == "pass" ]]; then
            # Plan passed validation - add context for Claude
            SUMMARY=$(echo "$RESULT" | jq -r '.summary | "Sections: \(.sections_found)/\(.sections_required), Tasks: \(.tasks_count), Risks: \(.risks_count)"' 2>/dev/null || echo "")
            cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Plan verification PASSED. $SUMMARY. Plan is ready for implementation."
  }
}
EOF
        else
            # Plan has issues - provide feedback to Claude
            ERRORS=$(echo "$RESULT" | jq -r '.errors | length' 2>/dev/null || echo "0")
            WARNINGS=$(echo "$RESULT" | jq -r '.warnings | length' 2>/dev/null || echo "0")
            ERROR_MSGS=$(echo "$RESULT" | jq -r '[.errors[].message] | join("; ")' 2>/dev/null || echo "")
            WARNING_MSGS=$(echo "$RESULT" | jq -r '[.warnings[].message] | join("; ")' 2>/dev/null || echo "")

            cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Plan verification found issues. Errors ($ERRORS): $ERROR_MSGS. Warnings ($WARNINGS): $WARNING_MSGS. Please offer to help fix these issues before marking the plan as ready."
  }
}
EOF
        fi
    else
        echo '{"systemMessage": "Warning: validate_plan.py not found"}'
    fi
else
    # Not a plan file, no action needed
    exit 0
fi
