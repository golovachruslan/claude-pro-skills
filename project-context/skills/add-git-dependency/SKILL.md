---
name: add-git-dependency
description: "Use when users want to add a cross-project dependency via a git repository URL. Triggers: 'add git dependency', 'git link dependency', 'remote dependency', 'external project dependency', 'depend on repo', 'link remote project', 'add dependency from github', 'fetch project context from git'."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# Add Git Link Dependency

Add a dependency on a remote project by its git repository URL. Only the `.project-context/` directory is fetched from the remote — no application code is cloned. This enables cross-repository dependency tracking without requiring a monorepo structure.

## Parameter

Only one optional parameter: the git repository URL.

```
/project-context:add-git-dependency https://github.com/org/auth-service.git
/project-context:add-git-dependency              # no URL — ask interactively
```

## Workflow

### 1. Detect Current Subproject

```bash
ls .project-context/*.md .project-context/*.json 2>/dev/null
```

If no `.project-context/` exists:
> "No project context found. Run `/project-context:init` first."

Read `brief.md` if available to get the current project name.

### 2. Resolve Git URL

**If URL was provided:** validate it looks like a git URL (contains `github.com`, `gitlab.com`, or ends with `.git`, or matches `git@` SSH pattern). If invalid, report and stop.

**If URL was NOT provided:** ask with AskUserQuestion:
> "What is the git repository URL for the dependency?"
- User types the URL

### 3. Ask: Ref / Branch

Use AskUserQuestion:
> "Which branch or ref to track?"

Options:
- **main (Recommended)** — default branch
- **master** — legacy default
- **Custom** — user types a branch name, tag, or commit

### 4. Ask: Project Name

Infer a default name from the git URL (last path segment without `.git`).

Use AskUserQuestion:
> "Project name? (inferred: [name-from-url])"

Options:
- **[name-from-url] (Recommended)** — use inferred name
- **Custom** — user types a name

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

**Git link entry format:**
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

**Important:** Use the Write tool to write the full JSON file. Do NOT use Edit for JSON — always read, modify in memory, write the whole file to avoid formatting issues.

### 9. Fetch Remote Project Context

After adding the entry, immediately fetch the remote `.project-context/` directory:

```bash
python .claude/skills/project-context/../../../project-context/scripts/fetch_git_deps.py fetch --dir .
```

Or run it relative to the project-context plugin location. The script:
1. Reads `dependencies.json` for entries with a `git` field
2. Uses `git sparse-checkout` to clone only `.project-context/` from each remote
3. Stores results in `.project-context/.deps-cache/<project-name>/`
4. Creates `.project-context/.deps-cache/.gitignore` with `*` to prevent tracking

### 10. Confirmation

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

## Edge Cases

### Remote has no .project-context/
After cloning, if no `.project-context/` exists in the remote repo:
> "The remote repository has no `.project-context/` directory. The dependency entry was added to `dependencies.json`, but no context files were fetched. The remote project needs to run `/project-context:init` first."

### Duplicate dependency
If target already in the same direction's array (match by `project` or `git` field):
> "[target] is already listed as [direction]. Update the existing entry instead?"

### Self-dependency
If the git URL matches the current project's repository (check `.git/config` remote URL):
> "This appears to be the current repository. Use `/project-context:add-dependency` for local dependencies instead."

### Network failure
If `git clone` fails:
> "Failed to fetch from [url]. The dependency entry was added to `dependencies.json` but context was not fetched. Run `/project-context:fetch-deps` to retry later."

### SSH vs HTTPS URLs
Both formats are supported:
- `https://github.com/org/repo.git`
- `git@github.com:org/repo.git`

### No reciprocal update
Unlike local path dependencies, git link dependencies do NOT offer reciprocal updates — you cannot write to a remote repository. If bidirectional tracking is needed, the remote project must independently add a git link dependency pointing back.
