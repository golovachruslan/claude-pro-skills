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

## Parameters

The command accepts inline parameters. Any parameter not provided is gathered interactively.

| Parameter | Position/Flag | Description |
|-----------|---------------|-------------|
| direction | 1st positional | `upstream` or `downstream` |
| project-path | 2nd positional | Relative path to target (e.g., `../shared`) |
| `--what` | Flag | What is shared (e.g., "Types, validators") |
| `--note` | Flag | Optional note (e.g., "Core domain types") |
| `--no-reciprocal` | Flag | Skip reciprocal update on the target project |

### Parse Rules

Extract from the user's command invocation:

1. **Direction**: first word after the command name — must be exactly `upstream` or `downstream`
2. **Project path**: next non-flag argument — a relative path (starts with `../` or `./`)
3. **--what "..."**: value after `--what` flag
4. **--note "..."**: value after `--note` flag
5. **--no-reciprocal**: presence of flag (boolean)

If a value is ambiguous or missing, ask for it. Never guess.

## Workflow

### 1. Detect Current Subproject

Check for existing context:

```bash
ls .project-context/*.md 2>/dev/null
```

If no `.project-context/` exists:
> "No project context found. Run `/project-context:init` first to set up this subproject."

Read `brief.md` if available to know the current project name.

### 2. Resolve Provided Params

Parse any inline params from the command invocation. Track which are provided vs. missing:

```
provided = {direction, path, what, note, no_reciprocal}  # from params
missing  = required - provided
```

### 3. Gather Missing: Direction

**Skip if provided as param.**

Use AskUserQuestion:
> "What kind of dependency are you adding?"
- **Upstream (this project consumes)** — e.g., "we import types from shared"
- **Downstream (this project is consumed by)** — e.g., "web calls our API"

### 4. Gather Missing: Target Project

**Skip if provided as param.**

Scan for sibling `.project-context/` directories:

```bash
find .. -maxdepth 3 -name ".project-context" -type d 2>/dev/null
```

If siblings found, present as options via AskUserQuestion:
> "Which project?"
- List discovered siblings by name and relative path
- "Other" for manual path entry

If no siblings found, ask for the relative path directly:
> "What is the relative path to the dependency? (e.g., `../shared`, `../../packages/api`)"

### 5. Resolve Target Name

Derive the target project name:
1. Read `[target-path]/.project-context/brief.md` and extract `**Project Name:**`
2. Fall back to the directory name from the path

### 6. Gather Missing: What is Shared

**Skip if provided via `--what`.**

> "What does this project [consume from / expose to] [target]?"

Examples to guide the user:
- Types, interfaces, or schemas
- API endpoints (REST, GraphQL, gRPC)
- Shared utilities or helpers
- Database schemas or migrations
- Event definitions or message formats

### 7. Gather Missing: Notes

**Skip if provided via `--note`.** If not provided and not interactive, default to empty.

### 8. Create or Update dependencies.md

#### If dependencies.md doesn't exist — create from template:

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

Then insert the new row into the correct section.

#### If dependencies.md exists — append row:

Read the existing file. Add a new table row to the appropriate section (Upstream or Downstream). Do NOT overwrite existing entries.

**Row format:**
```
| [target-name] | [relative-path] | [what] | [note] |
```

When editing, find the last data row in the target table (after the `|---|` separator, before the next `##` or empty line) and insert after it. Use the Edit tool for precision.

### 9. Reciprocal Update

**Skip if `--no-reciprocal` flag is set.**

Otherwise ask via AskUserQuestion:
> "[target] should also declare this relationship (as [reverse-direction]). Update [target]'s dependencies.md too?"
- **Yes (Recommended)** — Update or create the target's `dependencies.md`
- **No** — Skip

If yes, apply the same create-or-append logic to `[target-path]/.project-context/dependencies.md` with the reversed direction:
- If we added upstream here → add downstream there
- If we added downstream here → add upstream there

### 10. Confirmation

Display summary:

```
Added dependency:
  [current-project] ──[direction]──▶ [target-project]
  What: [what-shared]

Files modified:
  ✓ .project-context/dependencies.md
  ✓ [target-path]/.project-context/dependencies.md (reciprocal)
```

## Edge Cases

### Target has no .project-context/
Ask: "The target project has no `.project-context/`. Create one with just `dependencies.md`, or skip the reciprocal update?"

### Duplicate dependency
If the target project already appears in the same direction's table, warn:
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
Reject: "A project cannot depend on itself."

### Invalid direction param
If direction is not `upstream` or `downstream`, treat it as unprovided and ask interactively.

### Invalid path param
If path doesn't resolve to an existing directory, warn and ask for correction:
> "Path `[path]` doesn't exist. Enter the correct relative path:"
