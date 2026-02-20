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

Add a dependency relationship between subprojects in a monorepo. Creates `dependencies.json` if needed, appends to it if it exists, and optionally updates the other side (reciprocal declaration).

## Parameter

Only one optional parameter: the relative path to the target project.

```
/project-context:add-dependency ../shared
/project-context:add-dependency              # no path — discover siblings
```

## Workflow

### 1. Detect Current Subproject

```bash
ls .project-context/*.md .project-context/*.json 2>/dev/null
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

### 7. Create or Update dependencies.json

#### If dependencies.json doesn't exist — create it:

```json
{
  "upstream": [],
  "downstream": []
}
```

Then add the new entry to the correct array.

#### If dependencies.json exists — read, append, write:

1. Read and parse the existing JSON
2. Append the new entry to the correct array (`upstream` or `downstream`)
3. Write back with `indent=2`

**Entry format:**
```json
{
  "project": "[target-name]",
  "path": "[relative-path]",
  "what": "[what-shared]",
  "note": "[note or empty string]"
}
```

**Important:** Use the Write tool to write the full JSON file. Do NOT use Edit for JSON — always read, modify in memory, write the whole file to avoid formatting issues.

### 8. Reciprocal Update

Use AskUserQuestion:
> "Update [target]'s dependencies.json with the reverse relationship?"
- **Yes (Recommended)** — create or append the reverse entry
- **No** — skip

If yes: apply the same create-or-append logic to `[target-path]/.project-context/dependencies.json` with the reversed direction (upstream ↔ downstream) and the current project's name/path.

### 9. Confirmation

```
Added dependency:
  [current] ──[direction]──▶ [target]
  What: [what]

Files modified:
  ✓ .project-context/dependencies.json
  ✓ [target-path]/.project-context/dependencies.json (reciprocal)
```

## Edge Cases

### Target has no .project-context/
> "The target has no `.project-context/`. Create one with just `dependencies.json`, or skip reciprocal?"

### Duplicate dependency
If target already in the same direction's array (match by `project` field):
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
Reject: "A project cannot depend on itself."

### Invalid path
> "Path `[path]` doesn't exist. Check the path and try again."
