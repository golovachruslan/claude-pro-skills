#!/usr/bin/env python3
"""
Project context management utility.
Replaces fragile sed operations with reliable Python-based file management.

Usage:
    python manage_context.py status [--dir DIR]
    python manage_context.py validate [--dir DIR]
    python manage_context.py update-sections [--file FILE]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


CONTEXT_FILES = ["brief.md", "architecture.md", "state.md", "progress.md", "patterns.md"]

STALENESS_DAYS = {
    "brief.md": 30,
    "architecture.md": 7,
    "state.md": 1,
    "progress.md": 3,
    "patterns.md": 14,
}

MANAGED_SECTION_START = "<!-- PROJECT-CONTEXT:START -->"
MANAGED_SECTION_END = "<!-- PROJECT-CONTEXT:END -->"

CLAUDE_MANAGED_CONTENT = """
<!-- PROJECT-CONTEXT:START -->
## Project Context

Always read `.project-context/` files when starting work:
- `brief.md` — Project goals, scope, requirements
- `architecture.md` — System design, tech stack, flows
- `state.md` — Current position, blockers, next action
- `progress.md` — Completed/in-progress/upcoming work
- `patterns.md` — Established patterns and learnings

<!-- PROJECT-CONTEXT:END -->
"""

AGENTS_MANAGED_CONTENT = """
<!-- PROJECT-CONTEXT:START -->
## Project Context

Before executing tasks, read `.project-context/` files:
- `brief.md` — Project scope and goals
- `architecture.md` — System design and flows
- `state.md` — Current position and blockers
- `progress.md` — Work status
- `patterns.md` — Established patterns

<!-- PROJECT-CONTEXT:END -->
"""


def find_context_dir(start_dir="."):
    """Find .project-context directory."""
    context_dir = Path(start_dir) / ".project-context"
    if context_dir.is_dir():
        return context_dir
    return None


def cmd_status(args):
    """Show current project context status."""
    context_dir = find_context_dir(args.dir)
    if not context_dir:
        print(json.dumps({
            "exists": False,
            "message": "No .project-context/ directory found. Run /project-context:init to create."
        }))
        return 1

    now = datetime.now()
    files = {}
    missing = []

    for fname in CONTEXT_FILES:
        fpath = context_dir / fname
        if fpath.exists():
            stat = fpath.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            age_days = (now - mtime).days
            stale_threshold = STALENESS_DAYS.get(fname, 7)
            is_stale = age_days > stale_threshold
            size_lines = len(fpath.read_text().splitlines())

            files[fname] = {
                "exists": True,
                "lines": size_lines,
                "last_modified": mtime.isoformat(),
                "age_days": age_days,
                "stale": is_stale,
                "stale_threshold_days": stale_threshold,
            }
        else:
            missing.append(fname)
            files[fname] = {"exists": False}

    # Check for plans
    plans_dir = context_dir / "plans"
    plans = []
    if plans_dir.is_dir():
        plans = [f.name for f in plans_dir.glob("*.md")]

    # Determine suggested next action
    next_action = _determine_next_action(files, plans, context_dir)

    result = {
        "exists": True,
        "files": files,
        "missing": missing,
        "plans": plans,
        "next_action": next_action,
    }

    print(json.dumps(result, indent=2))
    return 0


def _determine_next_action(files, plans, context_dir):
    """Determine what the user should do next (used by /project-context:next)."""
    # Check if state.md exists and has content
    state_file = context_dir / "state.md"
    state_content = ""
    if state_file.exists():
        state_content = state_file.read_text()

    # Missing critical files
    missing_critical = [f for f in ["brief.md", "architecture.md"] if not files.get(f, {}).get("exists")]
    if missing_critical:
        return {"action": "init", "reason": f"Missing critical files: {', '.join(missing_critical)}"}

    # Check for stale state
    if files.get("state.md", {}).get("stale"):
        return {"action": "update", "reason": "state.md is stale — update current position"}

    # Check for active plans not yet implemented
    if plans:
        # Look for plans with "Planning" status
        for plan_name in plans:
            plan_path = context_dir / "plans" / plan_name
            content = plan_path.read_text()
            if "**Status:** Planning" in content:
                return {"action": "implement", "reason": f"Plan '{plan_name}' is ready for implementation", "plan": plan_name}

    # Check if any files are stale
    stale_files = [f for f, info in files.items() if info.get("stale")]
    if stale_files:
        return {"action": "update", "reason": f"Stale files: {', '.join(stale_files)}"}

    # Default
    return {"action": "discuss", "reason": "Context is up to date. Ready for new work."}


def cmd_validate(args):
    """Validate project context files."""
    context_dir = find_context_dir(args.dir)
    if not context_dir:
        print(json.dumps({"valid": False, "error": "No .project-context/ directory found."}))
        return 1

    issues = []

    for fname in CONTEXT_FILES:
        fpath = context_dir / fname
        if not fpath.exists():
            if fname == "state.md":
                issues.append({"file": fname, "severity": "warning", "message": "state.md missing — add for session continuity"})
            elif fname in ("brief.md", "architecture.md"):
                issues.append({"file": fname, "severity": "error", "message": f"{fname} missing — critical context file"})
            continue

        content = fpath.read_text()
        lines = content.splitlines()

        # Check if file is essentially empty (only template markers)
        non_empty = [l for l in lines if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("---") and not l.strip().startswith("*Last")]
        if len(non_empty) < 3:
            issues.append({"file": fname, "severity": "warning", "message": f"{fname} appears to be mostly empty template"})

        # Check for TODO/placeholder markers
        if re.search(r'\[.*\.\.\.\]|\[TODO\]|\[TBD\]', content):
            issues.append({"file": fname, "severity": "info", "message": f"{fname} contains unfilled placeholders"})

        # Check for stale timestamps
        timestamp_match = re.search(r'\*Last updated: (\d{4}-\d{2}-\d{2})', content)
        if timestamp_match:
            try:
                last_updated = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d")
                threshold = STALENESS_DAYS.get(fname, 7)
                if (datetime.now() - last_updated).days > threshold:
                    issues.append({"file": fname, "severity": "warning", "message": f"{fname} timestamp is stale (>{threshold} days)"})
            except ValueError:
                pass

        # architecture.md specific: check for Mermaid diagrams
        if fname == "architecture.md":
            if "```mermaid" not in content:
                issues.append({"file": fname, "severity": "warning", "message": "architecture.md has no Mermaid diagrams"})

    # Check plans directory
    plans_dir = context_dir / "plans"
    if plans_dir.is_dir():
        for plan_file in plans_dir.glob("*.md"):
            content = plan_file.read_text()
            # Check for executable task format
            if "**Action:**" not in content and "- **Action:**" not in content:
                issues.append({"file": f"plans/{plan_file.name}", "severity": "info", "message": "Plan lacks executable task format (Action/Verify/Done)"})

    valid = not any(i["severity"] == "error" for i in issues)
    print(json.dumps({"valid": valid, "issues": issues}, indent=2))
    return 0 if valid else 1


def cmd_update_sections(args):
    """Update managed sections in CLAUDE.md or AGENTS.md."""
    file_path = Path(args.file)
    if not file_path.exists():
        print(json.dumps({"updated": False, "reason": f"{args.file} not found"}))
        return 1

    content = file_path.read_text()

    # Determine which content to use
    if file_path.name == "AGENTS.md":
        new_section = AGENTS_MANAGED_CONTENT
    else:
        new_section = CLAUDE_MANAGED_CONTENT

    if MANAGED_SECTION_START in content:
        # Replace existing managed section
        pattern = re.compile(
            re.escape(MANAGED_SECTION_START) + r".*?" + re.escape(MANAGED_SECTION_END),
            re.DOTALL
        )
        new_content = pattern.sub(new_section.strip(), content)
    else:
        # Append managed section
        new_content = content.rstrip() + "\n" + new_section

    file_path.write_text(new_content)
    print(json.dumps({"updated": True, "file": str(file_path)}))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Project context management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status command
    status_parser = subparsers.add_parser("status", help="Show context status")
    status_parser.add_argument("--dir", default=".", help="Project root directory")

    # validate command
    validate_parser = subparsers.add_parser("validate", help="Validate context files")
    validate_parser.add_argument("--dir", default=".", help="Project root directory")

    # update-sections command
    sections_parser = subparsers.add_parser("update-sections", help="Update managed sections in CLAUDE.md/AGENTS.md")
    sections_parser.add_argument("--file", required=True, help="Path to CLAUDE.md or AGENTS.md")

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "validate": cmd_validate,
        "update-sections": cmd_update_sections,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
