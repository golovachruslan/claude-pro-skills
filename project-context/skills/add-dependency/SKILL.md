---
name: add-dependency
description: "Use when users want to add, declare, or connect cross-project dependencies in a monorepo. Triggers: 'add dependency', 'depends on', 'consumed by', 'this project uses', 'connect projects', 'add upstream', 'add downstream', 'link projects'."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Add a dependency relationship between subprojects in a monorepo. Creates `dependencies.md` if needed, appends to it if it exists, and optionally updates the other side (reciprocal declaration).

## Parameter

Only one optional parameter: the relative path to the target project.

```
/project-context:add-dependency ../shared
/project-context:add-dependency              # no path — discover siblings
```

## Workflow

### 1. Detect Current Subproject

```bash
ls .project-context/*.md 2>/dev/null
```

If no `.project-context/` exists:
> "No project context found. Run `/project-context:init` first."

Read `brief.md` if available to get the current project name.

### 2. Resolve Target Project

**If path was provided:** validate it resolves to an existing directory. If not, report the error and stop.

**If path was NOT provided:** discover siblings and ask:

```bash
find .. -maxdepth 3 -name ".project-context" -type d 2>/dev/null
```

Use AskUserQuestion to present discovered siblings:
> "Which project?"
- List each sibling by name and relative path
- "Other" for manual path entry

### 3. Resolve Target Name

1. Read `[target-path]/.project-context/brief.md` → extract `**Project Name:**`
2. Fall back to the directory name from the path

### 4. Ask: Direction

Use AskUserQuestion:
> "What is the relationship between [current] and [target]?"

Options:
- **[current] consumes [target] (upstream)** — "we import/use from them"
- **[target] consumes [current] (downstream)** — "they import/use from us"

### 5. Ask: What is Shared

Use AskUserQuestion:
> "What does [current] [consume from / expose to] [target]?"

Options (common patterns — user can pick or type custom):
- **Types / interfaces / schemas**
- **API endpoints (REST, GraphQL, gRPC)**
- **Shared utilities / helpers**
- **Database schemas / migrations**

### 6. Ask: Notes (optional)

Use AskUserQuestion:
> "Any additional notes for this dependency?"

Options:
- **No notes**
- **Custom** (user types)

### 7. Create or Update dependencies.md

#### If dependencies.md doesn't exist — create it:

```markdown
# Dependencies

## Upstream (Consumes)

Projects this subproject depends on.

| Project | Path | What | Notes |
|---------|------|------|-------|

## Downstream (Consumed By)

Projects that depend on this subproject.

| Project | Path | What | Notes |
|---------|------|------|-------|

## Integration Points

Key files/interfaces at dependency boundaries.

## Impact Rules

When changing this project, consider:

---
*Last updated: [current date]*
```

Then insert the new row into the correct section (Upstream or Downstream).

#### If dependencies.md exists — append row:

Read the file. Find the last data row in the target section's table. Insert after it using the Edit tool. Do NOT overwrite existing entries.

**Row format:**
```
| [target-name] | [relative-path] | [what] | [note] |
```

Update the `*Last updated:` timestamp.

### 8. Reciprocal Update

Use AskUserQuestion:
> "Update [target]'s dependencies.md with the reverse relationship?"
- **Yes (Recommended)** — create or append the reverse entry
- **No** — skip

If yes: apply the same create-or-append logic to `[target-path]/.project-context/dependencies.md` with the reversed direction (upstream ↔ downstream) and the current project's name/path.

### 9. Confirmation

```
Added dependency:
  [current] ──[direction]──▶ [target]
  What: [what]

Files modified:
  ✓ .project-context/dependencies.md
  ✓ [target-path]/.project-context/dependencies.md (reciprocal)
```

## Edge Cases

### Target has no .project-context/
> "The target has no `.project-context/`. Create one with just `dependencies.md`, or skip reciprocal?"

### Duplicate dependency
If target already in the same direction's table:
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
Reject: "A project cannot depend on itself."

### Invalid path
> "Path `[path]` doesn't exist. Check the path and try again."
