#!/usr/bin/env python3
"""
Plan Validation Script

Validates plan markdown files created by the planner skill.
Checks for completeness, actionability, and quality.

Usage:
    python validate_plan.py <plan.md>
    python validate_plan.py --help

Output:
    JSON with validation results
"""

import sys
import re
import json
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    status: str  # "pass", "fail", "warning"
    errors: list
    warnings: list
    suggestions: list
    summary: dict


# Required sections that every plan should have
REQUIRED_SECTIONS = [
    "overview",
    "requirements",
    "technical",  # matches "Technical Approach", "Technical Design", etc.
    "implementation",  # matches "Implementation Phases", "Implementation Plan"
    "success",  # matches "Success Criteria"
]

# Section name patterns for matching
SECTION_PATTERNS = {
    "overview": r"^#+\s*(overview|summary|introduction)",
    "requirements": r"^#+\s*(requirements?|functional requirements?|non-functional)",
    "technical": r"^#+\s*(technical\s*(approach|design|architecture)|architecture)",
    "implementation": r"^#+\s*(implementation\s*(phases?|plan)|phases?)",
    "success": r"^#+\s*(success\s*criteria|done\s*criteria|acceptance\s*criteria)",
    "risks": r"^#+\s*(risks?|risks?\s*(&|and)\s*mitigation)",
    "scope": r"^#+\s*(scope|out\s*of\s*scope|not\s*in\s*scope|future\s*enhancements?)",
    "dependencies": r"^#+\s*(dependencies|external\s*dependencies)",
}

# Placeholder patterns that indicate incomplete content
PLACEHOLDER_PATTERNS = [
    r"\[placeholder\]",
    r"\[todo\]",
    r"\[tbd\]",
    r"\[tba\]",
    r"\[fill\s*in\]",
    r"\[add\s*here\]",
    r"\[describe\]",
    r"\[insert\]",
    r"\[your\s+\w+\s+here\]",
    r"\[name\]",
    r"\[date\]",
    r"\[owner\]",
    r"xxx+",
]

# Vague task patterns
VAGUE_TASK_PATTERNS = [
    r"do\s+the\s+thing",
    r"implement\s+stuff",
    r"add\s+things",
    r"fix\s+issues",
    r"make\s+it\s+work",
    r"finish\s+this",
    r"complete\s+later",
]

# Vague success criteria patterns
VAGUE_SUCCESS_PATTERNS = [
    r"works?\s+well",
    r"users?\s+(are\s+)?happy",
    r"looks?\s+good",
    r"is\s+complete",
    r"is\s+done",
    r"no\s+bugs",
    r"everything\s+works",
]


def parse_plan(content: str) -> dict:
    """Parse plan content and extract structure."""
    lines = content.split("\n")

    result = {
        "title": "",
        "sections": {},
        "tasks": [],
        "has_metadata": False,
    }

    current_section = None
    current_content = []

    for i, line in enumerate(lines):
        # Check for title (first H1)
        if line.startswith("# ") and not result["title"]:
            result["title"] = line[2:].strip()
            continue

        # Check for metadata block
        if line.startswith("**Status:**") or line.startswith("**Created:**"):
            result["has_metadata"] = True

        # Check for section headers (H2 or H3)
        if re.match(r"^#{2,3}\s+", line):
            # Save previous section
            if current_section:
                result["sections"][current_section] = {
                    "content": "\n".join(current_content),
                    "line": current_section_line,
                }

            current_section = line.lstrip("#").strip().lower()
            current_section_line = i + 1
            current_content = []
        elif current_section:
            current_content.append(line)

        # Check for tasks (checkbox items)
        if re.match(r"^\s*-\s*\[\s*[xX ]?\s*\]", line):
            task_text = re.sub(r"^\s*-\s*\[\s*[xX ]?\s*\]\s*", "", line)
            result["tasks"].append({
                "text": task_text,
                "line": i + 1,
                "completed": "[x]" in line.lower() or "[X]" in line,
            })

    # Save last section
    if current_section:
        result["sections"][current_section] = {
            "content": "\n".join(current_content),
            "line": current_section_line,
        }

    return result


def find_section(sections: dict, pattern_key: str) -> tuple:
    """Find a section matching the pattern, return (name, content) or (None, None)."""
    pattern = SECTION_PATTERNS.get(pattern_key, "")
    for name, data in sections.items():
        if re.search(pattern, f"## {name}", re.IGNORECASE):
            return name, data
    return None, None


def check_required_sections(sections: dict) -> tuple:
    """Check for required sections."""
    errors = []
    found = []

    for req in REQUIRED_SECTIONS:
        name, _ = find_section(sections, req)
        if name:
            found.append(req)
        else:
            errors.append({
                "type": "missing_section",
                "section": req,
                "message": f"Missing required section: {req.title()}",
                "suggestion": get_section_suggestion(req),
            })

    return errors, found


def get_section_suggestion(section: str) -> str:
    """Get suggestion for adding a missing section."""
    suggestions = {
        "overview": "Add an Overview section explaining what is being built and why",
        "requirements": "Add Requirements section with functional and non-functional requirements",
        "technical": "Add Technical Approach section describing architecture and technology choices",
        "implementation": "Add Implementation Phases section with phased tasks",
        "success": "Add Success Criteria section with measurable completion criteria",
    }
    return suggestions.get(section, f"Add a {section.title()} section")


def check_placeholders(content: str) -> list:
    """Check for unfilled placeholders."""
    warnings = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        for pattern in PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                warnings.append({
                    "type": "placeholder",
                    "line": i + 1,
                    "text": matches[0],
                    "message": f"Unfilled placeholder found: {matches[0]}",
                })

    return warnings


def check_empty_sections(sections: dict) -> list:
    """Check for empty or near-empty sections."""
    warnings = []

    for name, data in sections.items():
        content = data["content"].strip()
        # Remove sub-headers and check if content remains
        content_without_headers = re.sub(r"^#+\s+.*$", "", content, flags=re.MULTILINE).strip()

        if len(content_without_headers) < 10:
            warnings.append({
                "type": "empty_section",
                "section": name,
                "line": data["line"],
                "message": f"Section '{name}' appears to be empty or has minimal content",
            })

    return warnings


def check_actionable_tasks(tasks: list) -> tuple:
    """Check if tasks are actionable and not vague."""
    warnings = []

    for task in tasks:
        text = task["text"].lower()
        for pattern in VAGUE_TASK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                warnings.append({
                    "type": "vague_task",
                    "line": task["line"],
                    "text": task["text"],
                    "message": f"Task may be too vague: '{task['text'][:50]}...'",
                })
                break

    return warnings, len(tasks)


def check_risks(sections: dict, content: str) -> tuple:
    """Check for risk identification."""
    warnings = []
    risk_count = 0

    name, data = find_section(sections, "risks")

    if name:
        risk_content = data["content"].lower()
        # Count risk items (look for bullet points or numbered items)
        risk_items = re.findall(r"^\s*[-*]\s*\*?\*?risk", risk_content, re.MULTILINE | re.IGNORECASE)
        table_risks = re.findall(r"\|\s*[^|]+risk", risk_content, re.IGNORECASE)
        risk_count = len(risk_items) + len(table_risks)

        # Check if risks have mitigations
        if risk_count > 0:
            if "mitigation" not in risk_content and "mitigate" not in risk_content:
                warnings.append({
                    "type": "missing_mitigation",
                    "section": name,
                    "message": "Risks identified but no mitigation strategies found",
                })
    else:
        # Check if content mentions this is low-risk
        low_risk_patterns = [
            r"no\s+significant\s+risks?",
            r"low[- ]risk",
            r"minimal\s+risk",
        ]
        is_low_risk = any(re.search(p, content, re.IGNORECASE) for p in low_risk_patterns)

        if not is_low_risk:
            warnings.append({
                "type": "no_risks",
                "message": "No Risks section found. Add risks with mitigations or state 'No significant risks identified'",
            })

    return warnings, risk_count


def check_success_criteria(sections: dict) -> list:
    """Check if success criteria are measurable."""
    warnings = []

    name, data = find_section(sections, "success")

    if name and data:
        content = data["content"].lower()

        for pattern in VAGUE_SUCCESS_PATTERNS:
            if re.search(pattern, content):
                warnings.append({
                    "type": "vague_success",
                    "section": name,
                    "line": data["line"],
                    "message": "Success criteria may be too vague. Use specific, measurable criteria.",
                })
                break

    return warnings


def check_scope(sections: dict) -> list:
    """Check for scope clarity."""
    suggestions = []

    name, _ = find_section(sections, "scope")

    if not name:
        # Check if scope is mentioned elsewhere
        has_scope_mention = False
        for section_name, data in sections.items():
            if "out of scope" in data["content"].lower() or "not in scope" in data["content"].lower():
                has_scope_mention = True
                break

        if not has_scope_mention:
            suggestions.append({
                "type": "no_scope",
                "message": "Consider adding explicit scope boundaries (what's in/out of scope)",
            })

    return suggestions


def check_dependencies(sections: dict, content: str) -> list:
    """Check for dependency documentation."""
    suggestions = []

    name, _ = find_section(sections, "dependencies")

    if not name:
        # Check if dependencies mentioned elsewhere
        dep_patterns = [
            r"no\s+dependencies",
            r"depends\s+on",
            r"requires?\s+",
            r"blocked\s+by",
        ]
        has_deps = any(re.search(p, content, re.IGNORECASE) for p in dep_patterns)

        if not has_deps:
            suggestions.append({
                "type": "no_dependencies",
                "message": "Consider documenting dependencies or state 'No dependencies'",
            })

    return suggestions


def validate_plan(file_path: str) -> ValidationResult:
    """Main validation function."""
    path = Path(file_path)

    if not path.exists():
        return ValidationResult(
            status="fail",
            errors=[{"type": "file_not_found", "message": f"File not found: {file_path}"}],
            warnings=[],
            suggestions=[],
            summary={"file": file_path},
        )

    content = path.read_text(encoding="utf-8")
    parsed = parse_plan(content)

    errors = []
    warnings = []
    suggestions = []

    # Check required sections
    section_errors, found_sections = check_required_sections(parsed["sections"])
    errors.extend(section_errors)

    # Check for placeholders
    placeholder_warnings = check_placeholders(content)
    warnings.extend(placeholder_warnings)

    # Check for empty sections
    empty_warnings = check_empty_sections(parsed["sections"])
    warnings.extend(empty_warnings)

    # Check tasks
    task_warnings, task_count = check_actionable_tasks(parsed["tasks"])
    warnings.extend(task_warnings)

    # Check risks
    risk_warnings, risk_count = check_risks(parsed["sections"], content)
    warnings.extend(risk_warnings)

    # Check success criteria quality
    success_warnings = check_success_criteria(parsed["sections"])
    warnings.extend(success_warnings)

    # Check scope
    scope_suggestions = check_scope(parsed["sections"])
    suggestions.extend(scope_suggestions)

    # Check dependencies
    dep_suggestions = check_dependencies(parsed["sections"], content)
    suggestions.extend(dep_suggestions)

    # Determine overall status
    if errors:
        status = "fail"
    elif warnings:
        status = "warning"
    else:
        status = "pass"

    summary = {
        "file": str(path.name),
        "title": parsed["title"],
        "has_metadata": parsed["has_metadata"],
        "sections_found": len(found_sections),
        "sections_required": len(REQUIRED_SECTIONS),
        "tasks_count": task_count,
        "risks_count": risk_count,
        "errors_count": len(errors),
        "warnings_count": len(warnings),
        "suggestions_count": len(suggestions),
    }

    return ValidationResult(
        status=status,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
        summary=summary,
    )


def format_output(result: ValidationResult, verbose: bool = True) -> str:
    """Format validation result for display."""
    lines = []

    # Header
    status_emoji = {"pass": "PASSED", "warning": "NEEDS ATTENTION", "fail": "FAILED"}
    lines.append(f"\nPlan Verification: {status_emoji.get(result.status, result.status.upper())}\n")
    lines.append(f"{result.summary['file']}")

    if result.summary.get("title"):
        lines.append(f"Title: {result.summary['title']}")

    lines.append("")

    # Errors
    if result.errors:
        lines.append("ERRORS (must fix):")
        for i, err in enumerate(result.errors, 1):
            lines.append(f"  {i}. {err['message']}")
            if err.get("suggestion"):
                lines.append(f"     -> {err['suggestion']}")
        lines.append("")

    # Warnings
    if result.warnings:
        lines.append("WARNINGS (recommended to fix):")
        for i, warn in enumerate(result.warnings, 1):
            msg = warn["message"]
            if warn.get("line"):
                msg += f" (line {warn['line']})"
            lines.append(f"  {i}. {msg}")
        lines.append("")

    # Suggestions
    if result.suggestions:
        lines.append("SUGGESTIONS (optional):")
        for i, sug in enumerate(result.suggestions, 1):
            lines.append(f"  {i}. {sug['message']}")
        lines.append("")

    # Summary
    if result.status == "pass":
        lines.append("Summary:")
        lines.append(f"  - {result.summary['sections_found']}/{result.summary['sections_required']} required sections present")
        lines.append(f"  - {result.summary['tasks_count']} actionable tasks defined")
        lines.append(f"  - {result.summary['risks_count']} risks identified")
        if result.summary.get("has_metadata"):
            lines.append("  - Metadata block present (Status, Created, etc.)")
        lines.append("\nPlan is ready for implementation.")
    else:
        lines.append(f"\nFix {len(result.errors)} error(s) and review {len(result.warnings)} warning(s) before proceeding.")

    return "\n".join(lines)


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\nExample:")
        print("  python validate_plan.py .project-context/plans/my-feature.md")
        sys.exit(0 if "--help" in sys.argv or "-h" in sys.argv else 1)

    file_path = sys.argv[1]
    json_output = "--json" in sys.argv

    result = validate_plan(file_path)

    if json_output:
        output = {
            "status": result.status,
            "errors": result.errors,
            "warnings": result.warnings,
            "suggestions": result.suggestions,
            "summary": result.summary,
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_output(result))

    # Exit code based on status
    exit_codes = {"pass": 0, "warning": 0, "fail": 1}
    sys.exit(exit_codes.get(result.status, 1))


if __name__ == "__main__":
    main()
