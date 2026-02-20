---
name: add-dependency
description: "Use when users want to add, declare, or connect cross-project dependencies — local paths (monorepo) or git URLs (remote repos). Triggers: 'add dependency', 'depends on', 'consumed by', 'this project uses', 'connect projects', 'add upstream', 'add downstream', 'link projects', 'git dependency', 'remote dependency'."
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Cross-Project Dependency

Add a dependency relationship to another project. Supports two modes:

- **Local path** — sibling project in a monorepo (e.g., `../shared`)
- **Git link** — remote repository by URL (e.g., `https://github.com/org/auth-service.git`)

Creates `dependencies.json` if needed, appends to it if it exists. Local deps offer reciprocal updates; git link deps fetch the remote `.project-context/` into a local cache.

## Parameter

One optional parameter: a relative path OR a git URL.

```
/project-context:add-dependency ../shared
/project-context:add-dependency https://github.com/org/auth-service.git
/project-context:add-dependency              # no argument — interactive
```

## Workflow

### 1. Detect Current Subproject

```bash
ls .project-context/*.md .project-context/*.json 2>/dev/null
```

If no `.project-context/` exists:
> "No project context found. Run `/project-context:init` first."

Read `brief.md` if available to get the current project name.

### 2. Determine Dependency Type

**If argument was provided**, auto-detect:
- Starts with `https://`, `git@`, `ssh://`, or ends with `.git` → **git link**
- Otherwise → **local path**

**If no argument was provided**, ask with AskUserQuestion:
> "What kind of dependency?"

Options:
- **Local path (Recommended)** — "Sibling project in this monorepo"
- **Git URL** — "Remote repository — only .project-context/ will be fetched"

Then proceed to the matching branch below.

---

## Branch A: Local Path Dependency

### A3. Resolve Target Project

**If path was provided:** validate it resolves to an existing directory. If not, report the error and stop.

**If path was NOT provided:** discover siblings and ask:

```bash
find .. -maxdepth 3 -name ".project-context" -type d 2>/dev/null
```

Use AskUserQuestion to present discovered siblings:
> "Which project?"
- List each sibling by name and relative path
- "Other" for manual path entry

### A4. Resolve Target Name

1. Read `[target-path]/.project-context/brief.md` → extract `**Project Name:**`
2. Fall back to the directory name from the path

### A5–A7. Ask Direction, What, Notes

*(Same as steps 5–7 in the shared section below.)*

### A8. Create or Update dependencies.json

Add a **local path entry**:
```json
{
  "project": "[target-name]",
  "path": "[relative-path]",
  "what": "[what-shared]",
  "note": "[note or empty string]"
}
```

### A9. Reciprocal Update

Use AskUserQuestion:
> "Update [target]'s dependencies.json with the reverse relationship?"
- **Yes (Recommended)** — create or append the reverse entry
- **No** — skip

If yes: apply the same create-or-append logic to `[target-path]/.project-context/dependencies.json` with the reversed direction (upstream ↔ downstream) and the current project's name/path.

### A10. Confirmation

```
Added dependency:
  [current] ──[direction]──▶ [target]
  What: [what]

Files modified:
  ✓ .project-context/dependencies.json
  ✓ [target-path]/.project-context/dependencies.json (reciprocal)
```

---

## Branch B: Git Link Dependency

### B3. Resolve Git URL

**If URL was provided:** validate it looks like a git URL. If invalid, report and stop.

**If URL was NOT provided:** ask with AskUserQuestion:
> "What is the git repository URL?"
- User types the URL

### B4. Ask: Ref / Branch

Use AskUserQuestion:
> "Which branch or ref to track?"

Options:
- **main (Recommended)** — default branch
- **master** — legacy default
- **Custom** — user types a branch name, tag, or commit

### B5. Resolve Project Name

Infer a default name from the git URL (last path segment without `.git`).

Use AskUserQuestion:
> "Project name? (inferred: [name-from-url])"

Options:
- **[name-from-url] (Recommended)** — use inferred name
- **Custom** — user types a name

### B6–B8. Ask Direction, What, Notes

*(Same as steps 5–7 in the shared section below.)*

### B9. Create or Update dependencies.json

Add a **git link entry**:
```json
{
  "project": "[project-name]",
  "git": "[git-url]",
  "ref": "[branch-or-ref]",
  "what": "[what-shared]",
  "note": "[note or empty string]"
}
```

The `git` field distinguishes this from a local path dependency (which uses `path`).

### B10. Fetch Remote Project Context

After adding the entry, immediately fetch the remote `.project-context/`:

```bash
python project-context/scripts/fetch_git_deps.py fetch --dir . --project [project-name]
```

The script uses `git sparse-checkout` to clone only `.project-context/` into `.project-context/.deps-cache/[project-name]/`.

### B11. Confirmation

```
Added git dependency:
  [current] ──[direction]──▶ [target] (via git)
  Git:  [git-url]
  Ref:  [ref]
  What: [what]

Fetched remote context:
  ✓ .project-context/.deps-cache/[project-name]/.project-context/

Files modified:
  ✓ .project-context/dependencies.json
```

---

## Shared Steps (Both Branches)

### 5. Ask: Direction

Use AskUserQuestion:
> "What is the relationship between [current] and [target]?"

Options:
- **[current] consumes [target] (upstream)** — "we import/use from them"
- **[target] consumes [current] (downstream)** — "they import/use from us"

### 6. Ask: What is Shared

Use AskUserQuestion:
> "What does [current] [consume from / expose to] [target]?"

Options (common patterns — user can pick or type custom):
- **Types / interfaces / schemas**
- **API endpoints (REST, GraphQL, gRPC)**
- **Shared utilities / helpers**
- **Database schemas / migrations**

### 7. Ask: Notes (optional)

Use AskUserQuestion:
> "Any additional notes for this dependency?"

Options:
- **No notes**
- **Custom** (user types)

### 8. Create or Update dependencies.json

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

**Important:** Use the Write tool to write the full JSON file. Do NOT use Edit for JSON — always read, modify in memory, write the whole file to avoid formatting issues.

---

## Edge Cases

### Target has no .project-context/ (local only)
> "The target has no `.project-context/`. Create one with just `dependencies.json`, or skip reciprocal?"

### Remote has no .project-context/ (git only)
> "The remote repository has no `.project-context/` directory. The entry was added to `dependencies.json`, but no context files were fetched. The remote project needs to run `/project-context:init` first."

### Duplicate dependency
If target already in the same direction's array (match by `project` field, or by `git` URL):
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
Reject: "A project cannot depend on itself."

For git links: if the URL matches `.git/config` remote URL, suggest using local path instead.

### Invalid path
> "Path `[path]` doesn't exist. Check the path and try again."

### Network failure (git only)
> "Failed to fetch from [url]. The entry was added to `dependencies.json` but context was not fetched. Run `/project-context:fetch-deps` to retry later."

### No reciprocal for git links
Git link dependencies do NOT offer reciprocal updates — you cannot write to a remote repository.
