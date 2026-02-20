#!/usr/bin/env python3
"""
Project context management utility.
Replaces fragile sed operations with reliable Python-based file management.

Usage:
    python manage_context.py status [--dir DIR]
    python manage_context.py validate [--dir DIR]
    python manage_context.py update-sections [--file FILE]
    python manage_context.py deps [--dir DIR] [--root ROOT]
    python manage_context.py deps-validate [--dir DIR] [--root ROOT]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


CONTEXT_FILES = ["brief.md", "architecture.md", "state.md", "progress.md", "patterns.md", "dependencies.md"]

STALENESS_DAYS = {
    "brief.md": 30,
    "architecture.md": 7,
    "state.md": 1,
    "progress.md": 3,
    "patterns.md": 14,
    "dependencies.md": 30,
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
- `dependencies.md` — Cross-project dependencies (monorepo)

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
- `dependencies.md` — Cross-project dependencies (monorepo)

<!-- PROJECT-CONTEXT:END -->
"""


def find_context_dir(start_dir="."):
    """Find .project-context directory."""
    context_dir = Path(start_dir) / ".project-context"
    if context_dir.is_dir():
        return context_dir
    return None


def parse_dependencies(context_dir):
    """Parse dependencies.md and return structured dependency data.

    Parses the markdown tables in Upstream and Downstream sections.
    Returns dict with upstream, downstream lists and raw integration/impact text.
    """
    deps_file = context_dir / "dependencies.md"
    if not deps_file.exists():
        return None

    content = deps_file.read_text()
    result = {
        "upstream": [],
        "downstream": [],
        "integration_points": [],
        "impact_rules": [],
    }

    # Parse markdown tables in Upstream/Downstream sections
    # Table row pattern: | project | path | what | notes |
    table_row_re = re.compile(
        r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$'
    )

    current_section = None
    for line in content.splitlines():
        stripped = line.strip()

        # Detect section headers
        if re.match(r'^##\s+Upstream', stripped, re.IGNORECASE):
            current_section = "upstream"
            continue
        elif re.match(r'^##\s+Downstream', stripped, re.IGNORECASE):
            current_section = "downstream"
            continue
        elif re.match(r'^##\s+Integration', stripped, re.IGNORECASE):
            current_section = "integration"
            continue
        elif re.match(r'^##\s+Impact', stripped, re.IGNORECASE):
            current_section = "impact"
            continue
        elif stripped.startswith("## "):
            current_section = None
            continue

        if current_section in ("upstream", "downstream"):
            m = table_row_re.match(stripped)
            if m:
                project, path, what, notes = m.groups()
                # Skip header and separator rows
                if project.strip() in ("Project", "---", "") or "---" in path:
                    continue
                result[current_section].append({
                    "project": project.strip(),
                    "path": path.strip(),
                    "what": what.strip(),
                    "notes": notes.strip(),
                })

        elif current_section == "integration" and stripped.startswith("- "):
            result["integration_points"].append(stripped[2:])

        elif current_section == "impact" and stripped.startswith("- "):
            result["impact_rules"].append(stripped[2:])

    return result


def find_all_contexts(root_dir):
    """Walk a directory tree and find all .project-context/ directories.

    Returns list of (project_path, context_dir) tuples.
    """
    root = Path(root_dir).resolve()
    contexts = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs and node_modules
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d != "node_modules"
        ]

        p = Path(dirpath)
        context_dir = p / ".project-context"
        if context_dir.is_dir():
            contexts.append((p, context_dir))
            # Don't recurse into the .project-context dir itself
            if ".project-context" in dirnames:
                dirnames.remove(".project-context")

    return contexts


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

    # Parse dependencies if present
    deps = parse_dependencies(context_dir)

    # Determine suggested next action
    next_action = _determine_next_action(files, plans, context_dir)

    result = {
        "exists": True,
        "files": files,
        "missing": missing,
        "plans": plans,
        "next_action": next_action,
    }

    if deps:
        result["dependencies"] = {
            "upstream_count": len(deps["upstream"]),
            "downstream_count": len(deps["downstream"]),
            "upstream": [d["project"] for d in deps["upstream"]],
            "downstream": [d["project"] for d in deps["downstream"]],
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
            # dependencies.md is optional
            if fname == "dependencies.md":
                continue
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

    # Validate dependencies.md paths if present
    deps = parse_dependencies(context_dir)
    if deps:
        project_root = Path(args.dir).resolve()
        all_deps = deps["upstream"] + deps["downstream"]
        for dep in all_deps:
            dep_path = (context_dir.parent / dep["path"]).resolve()
            if not dep_path.is_dir():
                issues.append({
                    "file": "dependencies.md",
                    "severity": "warning",
                    "message": f"Dependency '{dep['project']}' path not found: {dep['path']}"
                })
            else:
                # Check if the dependency target also has a .project-context/
                dep_context = dep_path / ".project-context"
                if not dep_context.is_dir():
                    issues.append({
                        "file": "dependencies.md",
                        "severity": "info",
                        "message": f"Dependency '{dep['project']}' at {dep['path']} has no .project-context/ — consider initializing it"
                    })

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


def cmd_deps(args):
    """Resolve and display dependency graph for a project or monorepo.

    When --root is provided, discovers all .project-context/ dirs under root
    and builds a complete dependency graph. Otherwise shows deps for --dir only.
    """
    if args.root:
        return _deps_monorepo(args)
    return _deps_single(args)


def _deps_single(args):
    """Show dependencies for a single project."""
    context_dir = find_context_dir(args.dir)
    if not context_dir:
        print(json.dumps({
            "error": "No .project-context/ directory found.",
            "hint": "Run /project-context:init first, then add dependencies.md"
        }))
        return 1

    deps = parse_dependencies(context_dir)
    if not deps:
        print(json.dumps({
            "has_dependencies": False,
            "message": "No dependencies.md found. This project has no declared cross-project dependencies.",
            "hint": "Create .project-context/dependencies.md to declare monorepo relationships"
        }))
        return 0

    # Resolve paths and check if dependency contexts exist
    for dep_list_key in ("upstream", "downstream"):
        for dep in deps[dep_list_key]:
            dep_abs = (context_dir.parent / dep["path"]).resolve()
            dep["resolved_path"] = str(dep_abs)
            dep["exists"] = dep_abs.is_dir()
            dep["has_context"] = (dep_abs / ".project-context").is_dir()

    result = {
        "project_dir": str(Path(args.dir).resolve()),
        "has_dependencies": True,
        **deps,
    }

    print(json.dumps(result, indent=2))
    return 0


def _deps_monorepo(args):
    """Discover all contexts under root and build a full dependency graph."""
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"Root directory not found: {args.root}"}))
        return 1

    contexts = find_all_contexts(root)
    if not contexts:
        print(json.dumps({
            "error": "No .project-context/ directories found under root",
            "root": str(root)
        }))
        return 1

    # Build graph: project_name -> {path, upstream, downstream}
    projects = {}
    for project_path, context_dir in contexts:
        # Derive project name from brief.md or directory name
        name = project_path.name
        brief_path = context_dir / "brief.md"
        if brief_path.exists():
            content = brief_path.read_text()
            name_match = re.search(r'\*\*Project Name:\*\*\s*(.+)', content)
            if name_match:
                name = name_match.group(1).strip()

        rel_path = str(project_path.relative_to(root))
        deps = parse_dependencies(context_dir)

        projects[name] = {
            "path": rel_path,
            "abs_path": str(project_path),
            "has_dependencies_file": deps is not None,
            "upstream": [d["project"] for d in deps["upstream"]] if deps else [],
            "downstream": [d["project"] for d in deps["downstream"]] if deps else [],
        }

    # Cross-check: verify that declared relationships are reciprocal
    warnings = []
    for name, info in projects.items():
        for up in info["upstream"]:
            if up in projects:
                if name not in projects[up]["downstream"]:
                    warnings.append(
                        f"'{name}' declares upstream dependency on '{up}', "
                        f"but '{up}' does not list '{name}' as downstream"
                    )

        for down in info["downstream"]:
            if down in projects:
                if name not in projects[down]["upstream"]:
                    warnings.append(
                        f"'{name}' declares downstream '{down}', "
                        f"but '{down}' does not list '{name}' as upstream"
                    )

    # Build a Mermaid diagram of the graph
    mermaid_lines = ["graph LR"]
    seen_edges = set()
    for name, info in projects.items():
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        for up in info["upstream"]:
            safe_up = re.sub(r'[^a-zA-Z0-9]', '_', up)
            edge = f"    {safe_up}[{up}] --> {safe_name}[{name}]"
            if edge not in seen_edges:
                mermaid_lines.append(edge)
                seen_edges.add(edge)

    result = {
        "root": str(root),
        "project_count": len(projects),
        "projects": projects,
        "warnings": warnings,
        "mermaid": "\n".join(mermaid_lines) if len(mermaid_lines) > 1 else None,
    }

    print(json.dumps(result, indent=2))
    return 0


def cmd_deps_validate(args):
    """Validate dependency declarations across a monorepo.

    Checks: path resolution, reciprocal declarations, circular dependencies,
    and context file existence.
    """
    root = Path(args.root).resolve() if args.root else Path(args.dir).resolve()
    contexts = find_all_contexts(root)

    if not contexts:
        print(json.dumps({"valid": True, "message": "No project contexts found", "issues": []}))
        return 0

    issues = []

    # Build name -> path mapping
    name_to_path = {}
    name_to_deps = {}

    for project_path, context_dir in contexts:
        name = project_path.name
        brief_path = context_dir / "brief.md"
        if brief_path.exists():
            content = brief_path.read_text()
            name_match = re.search(r'\*\*Project Name:\*\*\s*(.+)', content)
            if name_match:
                name = name_match.group(1).strip()

        name_to_path[name] = project_path
        deps = parse_dependencies(context_dir)
        name_to_deps[name] = deps

    # Validate each project's dependencies
    for name, deps in name_to_deps.items():
        if not deps:
            continue

        project_path = name_to_path[name]

        for dep_list_key, direction in [("upstream", "upstream"), ("downstream", "downstream")]:
            for dep in deps[dep_list_key]:
                dep_name = dep["project"]
                dep_rel_path = dep["path"]

                # 1. Check path resolves
                dep_abs = (project_path / ".project-context" / ".." / dep_rel_path).resolve()
                if not dep_abs.is_dir():
                    issues.append({
                        "project": name,
                        "severity": "error",
                        "message": f"{direction} dependency '{dep_name}' path does not exist: {dep_rel_path}"
                    })
                    continue

                # 2. Check dependency has context
                if not (dep_abs / ".project-context").is_dir():
                    issues.append({
                        "project": name,
                        "severity": "warning",
                        "message": f"{direction} dependency '{dep_name}' has no .project-context/"
                    })

                # 3. Check reciprocal declaration
                reverse_dir = "downstream" if direction == "upstream" else "upstream"
                if dep_name in name_to_deps and name_to_deps[dep_name]:
                    peer_deps = name_to_deps[dep_name]
                    peer_names = [d["project"] for d in peer_deps[reverse_dir]]
                    if name not in peer_names:
                        issues.append({
                            "project": name,
                            "severity": "warning",
                            "message": (
                                f"'{name}' declares {direction} dependency on '{dep_name}', "
                                f"but '{dep_name}' does not list '{name}' as {reverse_dir}"
                            )
                        })

    # 4. Check for circular dependencies (simple cycle detection via DFS)
    def find_cycles():
        visited = set()
        path = set()
        cycles = []

        def dfs(node, current_path):
            if node in path:
                cycle_start = list(current_path)
                idx = cycle_start.index(node)
                cycles.append(cycle_start[idx:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            path.add(node)
            current_path.append(node)

            deps = name_to_deps.get(node)
            if deps:
                for dep in deps["upstream"]:
                    dfs(dep["project"], current_path[:])

            path.discard(node)

        for name in name_to_deps:
            dfs(name, [])

        return cycles

    cycles = find_cycles()
    for cycle in cycles:
        issues.append({
            "project": cycle[0],
            "severity": "error",
            "message": f"Circular dependency detected: {' → '.join(cycle)}"
        })

    valid = not any(i["severity"] == "error" for i in issues)
    print(json.dumps({
        "valid": valid,
        "project_count": len(name_to_deps),
        "with_dependencies": sum(1 for d in name_to_deps.values() if d is not None),
        "issues": issues,
    }, indent=2))
    return 0 if valid else 1


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

    # deps command
    deps_parser = subparsers.add_parser("deps", help="Show dependency graph")
    deps_parser.add_argument("--dir", default=".", help="Project directory")
    deps_parser.add_argument("--root", default=None, help="Monorepo root (discovers all contexts)")

    # deps-validate command
    deps_validate_parser = subparsers.add_parser("deps-validate", help="Validate dependencies across monorepo")
    deps_validate_parser.add_argument("--dir", default=".", help="Project directory")
    deps_validate_parser.add_argument("--root", default=None, help="Monorepo root")

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "validate": cmd_validate,
        "update-sections": cmd_update_sections,
        "deps": cmd_deps,
        "deps-validate": cmd_deps_validate,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
