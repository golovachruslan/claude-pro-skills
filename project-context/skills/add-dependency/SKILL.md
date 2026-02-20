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

Interactively add a dependency relationship between subprojects in a monorepo. Creates `dependencies.md` if needed, appends to it if it exists, and optionally updates the other side (reciprocal declaration).

## Workflow

### 1. Detect Current Subproject

Check for existing context:

```bash
ls .project-context/*.md 2>/dev/null
```

If no `.project-context/` exists:
> "No project context found. Run `/project-context:init` first to set up this subproject."

Read `brief.md` if available to know the current project name.

### 2. Discover Sibling Projects

Scan for other `.project-context/` directories in the monorepo:

```bash
# Look for sibling project contexts (up to 3 levels)
find .. -maxdepth 3 -name ".project-context" -type d 2>/dev/null
```

Build a list of known sibling projects with their names (from `brief.md`) and paths.

### 3. Ask: Direction and Target

Use AskUserQuestion to gather:

**Question 1: Direction**
> "What kind of dependency are you adding?"
- **Upstream (this project consumes)** — e.g., "we import types from shared"
- **Downstream (this project is consumed by)** — e.g., "web calls our API"

**Question 2: Target project**

If sibling projects were discovered, present them as options:
> "Which project?"
- List discovered siblings by name
- "Other" for manual path entry

If no siblings found, ask for the relative path directly:
> "What is the relative path to the dependency? (e.g., `../shared`, `../../packages/api`)"

### 4. Ask: What is Shared

> "What does this project consume from / expose to [target]?"

Examples to guide the user:
- Types, interfaces, or schemas
- API endpoints (REST, GraphQL, gRPC)
- Shared utilities or helpers
- Database schemas or migrations
- Event definitions or message formats

### 5. Ask: Integration Points (Optional)

> "Any key files or interfaces at the boundary? (optional, press enter to skip)"

Examples:
- `src/types/api.ts`
- `docs/openapi.yaml`
- `src/client/sdk.ts`

### 6. Create or Update dependencies.md

#### If dependencies.md doesn't exist — create from template:

```markdown
# Dependencies

## Upstream (Consumes)

Projects this subproject depends on.

| Project | Path | What | Notes |
|---------|------|------|-------|
| [target] | [relative-path] | [what-shared] | [notes] |

## Downstream (Consumed By)

Projects that depend on this subproject.

| Project | Path | What | Notes |
|---------|------|------|-------|

## Integration Points

[If user provided integration points, list them here]

## Impact Rules

When changing this project, consider:
- [Generated from the dependency added]

---
*Last updated: [current date]*
```

Place the dependency row in the correct section (Upstream or Downstream).

#### If dependencies.md exists — append row:

Read the existing file. Add a new table row to the appropriate section (Upstream or Downstream). Do NOT overwrite existing entries.

When editing, find the last row in the target table and insert after it. Use the Edit tool for precision.

### 7. Offer Reciprocal Update

After updating the current project, ask:

> "[target] should also declare this relationship (as [reverse-direction]). Update [target]'s dependencies.md too?"
- **Yes** — Update or create `[target-path]/.project-context/dependencies.md` with the reverse entry
- **No** — Skip (warn: `deps-validate` will flag this as a mismatch)

If yes, apply the same logic (create or append) to the target project's `dependencies.md` with the reversed direction:
- If we added upstream here → add downstream there
- If we added downstream here → add upstream there

### 8. Confirmation

Display summary:

```
Added dependency:
  [current-project] ──[direction]──▶ [target-project]
  What: [what-shared]

Files modified:
  ✓ .project-context/dependencies.md
  ✓ [target-path]/.project-context/dependencies.md (reciprocal)

Run `python manage_context.py deps-validate --root [monorepo-root]` to verify the full graph.
```

## Edge Cases

### Target has no .project-context/
Ask: "The target project has no `.project-context/`. Create one with just `dependencies.md`, or skip the reciprocal update?"

### Duplicate dependency
If the target project already appears in the same direction's table, warn:
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
Reject: "A project cannot depend on itself."
