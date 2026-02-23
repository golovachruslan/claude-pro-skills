---
name: project-context:update
description: "Update project context files based on chat history, code changes, or user input. Triggers: 'update context', 'capture learnings', 'retro', 'retrospective', 'what did we learn', 'extract learnings', 'sync context', 'summarize our work', 'capture insights'. Supports --chat (deep conversation analysis with signal recognition), --scan (git diff), --input (interactive)."
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Update Project Context

Update one or more `.project-context/` files based on different sources. The `--chat` mode includes deep conversation analysis with signal recognition, quality filters, and structured proposals.

## Arguments

- `file` (optional): Specific file to update
  - `brief` — Project goals and scope
  - `architecture` — System diagrams and flows
  - `state` — Current position and focus
  - `progress` — Work status and items
  - `patterns` — Patterns and learnings
  - If omitted: Smart update of relevant files

- `--source` (optional): Where to get update information
  - `--chat` — Deep analysis of current conversation history
  - `--scan` — Scan codebase for changes (git diff, new files)
  - `--input` — Interactive input from user
  - Default: Smart detection (chat if recent discussion, else scan)

## Workflow

### Step 1: Verify Context Exists

```bash
ls .project-context/*.md 2>/dev/null
```

If not found: "Run `/project-context:init` first."

### Step 2: Determine Update Source

**Smart Detection:**
1. Meaningful conversation context (decisions, learnings, completed work) → use `--chat`
2. Git status shows changes but no meaningful conversation → use `--scan`
3. Otherwise → prompt for `--input`

---

## --chat Mode: Deep Conversation Analysis

### 2a. Analyze Conversation

Review the current conversation to identify:

**Key Learnings:**
- What new knowledge was gained?
- What worked well?
- What didn't work as expected?
- What would you do differently?

**Decisions Made:**
- Technical choices (libraries, patterns, architecture)
- Design decisions (UI/UX, data structures)
- Trade-offs accepted
- Rationale behind decisions

**Patterns Discovered:**
- Coding patterns established
- Best practices identified
- Anti-patterns to avoid
- Conventions adopted

**Errors & Solutions:**
- Bugs encountered and fixed
- Common pitfalls discovered
- Debugging insights
- Error handling patterns

**Progress Updates:**
- Features completed
- Work in progress
- Blockers resolved
- Next steps identified

Use signal recognition from `references/analysis-patterns.md` to systematically identify these.

### 2b. Check Existing Context

Read existing `.project-context/` files to understand current state and avoid redundancy.

### 2c. Categorize Learnings

Map extracted insights to appropriate files:

| Category | Target File | Examples |
|----------|-------------|----------|
| Project goals, scope changes | `brief.md` | "Pivoted to focus on mobile-first experience" |
| Architecture decisions, tech choices | `architecture.md` | "Switched from REST to GraphQL", diagram updates |
| Coding patterns, conventions | `patterns.md` | "Using custom hooks for data fetching" |
| Bug fixes, learnings, anti-patterns | `patterns.md` | "Avoid prop drilling - use Context API" |
| Completed work, current status | `progress.md` | "Completed auth system, starting on dashboard" |
| Current focus, blockers, next action | `state.md` | "Working on Phase 2, blocked by API design" |

### 2d. Propose Updates

For each identified learning, propose specific updates:

```markdown
## Proposed Updates

### 1. [File Name] - [Section]
**Insight:** [What was learned]
**Proposed Addition:**
[Exact text to add, maintaining file's existing format]

**Rationale:** [Why this belongs here]
```

### 2e. Ask User Confirmation

Present all proposed updates and get explicit approval before applying:

```
I've analyzed our conversation and identified [N] key learnings to capture.

## Proposed Updates

[List all proposed updates with clear sections]

Questions:
1. Do these updates accurately capture our learnings?
2. Should any updates be modified, added, or removed?

I'll apply the approved updates once you confirm.
```

### 2f. Apply Approved Updates

After user confirms:
1. Read the target file
2. Identify the correct section (or create if needed)
3. Use Edit tool to add content in appropriate location
4. Maintain existing formatting and structure
5. Update timestamps

---

## --scan Mode: Codebase Analysis

```bash
git diff --stat HEAD~5 2>/dev/null || git status --short
```

Analyze for:
- New components → `architecture.md`
- New patterns → `patterns.md`
- Completed work → `progress.md`

---

## --input Mode: Interactive

Ask user specific questions based on the file being updated.

---

## Step 3: Refresh Managed Sections

After any mode completes, sync configuration files:

```bash
python project-context/scripts/manage_context.py update-sections --file CLAUDE.md
python project-context/scripts/manage_context.py update-sections --file AGENTS.md
```

## Step 4: Show Summary

```markdown
Updates applied to .project-context files:

- **patterns.md**: Added error handling pattern for async event handlers
- **progress.md**: Documented authentication system completion
- **architecture.md**: Updated auth flow diagram

Configuration files refreshed: CLAUDE.md, AGENTS.md
```

---

## Step 5: Propagate to Downstream Dependencies

After applying updates, check if any downstream local-path dependencies exist and if changes are relevant to them.

### 5a. Check for Downstream Deps

Read `.project-context/dependencies.json` (if it exists):

```bash
cat .project-context/dependencies.json 2>/dev/null
```

If no `downstream` entries exist, or all downstream entries are git URLs (have a `git` field) → skip this step entirely.

Only local-path downstream deps (entries with a `path` field) are eligible for propagation.

### 5b. Determine What Changed

Compare the files that were just updated against each downstream dep's `what` field to assess relevance.

**Relevance mapping:**

| Changed file | Relevant if `what` mentions |
|---|---|
| `architecture.md` | API, endpoints, schema, interface, contract, integration, architecture, structure |
| `brief.md` | requirements, goals, scope, vision, purpose |
| `patterns.md` | patterns, conventions, standards, practices |
| `progress.md` | *(rarely relevant to downstream — skip unless `what` mentions milestones)* |
| `state.md` | *(rarely relevant — skip)* |

If no changed files are relevant to any downstream dep's `what` field → skip propagation silently.

### 5c. Ask User Confirmation

Present only the downstream deps with relevant changes:

```
Your context changes may affect downstream projects:

  📦 web — consumes: API types, REST endpoints
     Relevant changes: architecture.md (new /users/bulk endpoint)

  📦 mobile — consumes: API types, push notification schemas
     Relevant changes: architecture.md (new /users/bulk endpoint), brief.md (scope change)

Propagate upstream changes to these projects?
```

Use AskUserQuestion with options:
- **Yes, all** — propagate to all listed projects
- **Pick** — ask per-project (Yes/No for each)
- **Skip** — do not propagate

### 5d. Build Propagation Entry

For each confirmed downstream project, compose a concise entry summarizing what changed and what action may be needed:

```markdown
## Upstream Changes (from: {current-project-name}, {YYYY-MM-DD})

- **{changed-file}**: {brief description of what changed}
- **Action needed**: {what the downstream project may need to update}
```

Infer the current project name from `.project-context/brief.md` (`**Project Name:**` field) or fall back to the current directory name.

### 5e. Append to Downstream state.md

For each confirmed downstream project:

1. Check the target path exists:
   ```bash
   ls {dep-path}/.project-context/state.md 2>/dev/null
   ```
   If `state.md` does not exist → skip with a warning: `"{dep-path} has no state.md — skipping propagation"`

2. Read the current `state.md`

3. Check if an `## Upstream Changes` section already exists:
   - If yes → append new entry below the existing ones (keep history)
   - If no → append a new `## Upstream Changes` section at the end of the file

4. Use Edit tool to apply the change.

---

## Step 6: Commit Changes

After all context updates and propagations are applied, offer to commit.

### 6a. Detect Git Roots

```bash
# Your project's git root
git rev-parse --show-toplevel

# Each downstream dep's git root (for propagated deps only)
git -C {dep-path} rev-parse --show-toplevel 2>/dev/null
```

Group downstream deps by whether their git root matches yours:
- **Same root** → can be included in one commit with your changes
- **Different root** → requires a separate branch + commit in their repo

### 6b. Ask Commit Confirmation

Present a summary of what will be committed:

```
Commit context changes?

  This repo:
    .project-context/architecture.md
    .project-context/progress.md
    ../web/.project-context/state.md   ← same git root

  ../mobile/ (separate repo):
    .project-context/state.md          ← will create branch context/upstream-{name}-{date}
```

Use AskUserQuestion:
- **Yes** — commit all
- **Skip** — leave files modified, do not commit

If user skips → show summary of modified files and exit.

### 6c. Commit Same-Root Changes

Stage and commit all same-root files together:

```bash
git add .project-context/ {same-root-dep-paths...}
git commit -m "chore(context): update {project-name} context + propagate to {dep-names}"
```

### 6d. Commit Different-Root Deps

For each separate-repo downstream dep that was propagated to:

```bash
# Determine branch name
BRANCH="context/upstream-{current-project-name}-{YYYY-MM-DD}"

# Check if branch already exists
git -C {dep-path} branch --list {BRANCH}
# If exists → reuse it (checkout, amend or add new commit)
# If not → create it

git -C {dep-path} checkout -b {BRANCH}   # or: checkout {BRANCH} if already exists
git -C {dep-path} add .project-context/state.md
git -C {dep-path} commit -m "chore(context): upstream changes from {current-project-name} ({YYYY-MM-DD})"
git -C {dep-path} checkout -   # return to their previous branch
```

If the downstream repo has a conflict on checkout (rare — only if state.md has staged/conflicting changes):
```
Could not create branch in ../mobile — working tree has conflicts on .project-context/state.md.
File was modified but not committed. Please commit or stash changes in ../mobile first.
```

### 6e. Final Summary

```markdown
## Done

Context updates applied:
  ✓ .project-context/architecture.md
  ✓ .project-context/progress.md

Propagated to:
  ✓ web — state.md updated
  ✓ mobile — state.md updated

Commits:
  ✓ This repo — "chore(context): update api context + propagate to web"
  ✓ ../mobile — branch context/upstream-api-2026-02-21 created
```

## Quality Filters

Only capture insights that are:
- **Actionable** — Can be applied in future work
- **Specific** — Concrete examples, not vague generalizations
- **Contextual** — Include when/why it applies
- **Valuable** — Worth preserving for future reference
- **Not trivial** — Skip obvious or one-off details
- **Not redundant** — Don't duplicate existing context

## File-Specific Guidelines

### brief.md
Update when: Project goals/vision change, target users evolve, scope expands/contracts, core requirements shift.

### architecture.md
Update when: New technology adopted, architecture patterns change, components added/modified, integration points established, flows change.
**Always use Mermaid diagrams** with clear titles, descriptive labels, and step-by-step descriptions below.

### patterns.md
Update when: Coding pattern established, convention adopted, best practice identified, anti-pattern discovered, solution to common problem found.
**Organize by category** (Error Handling, State Management, etc.)

### progress.md
Update when: Feature completed, milestone reached, current work changes, blocker resolved, next steps identified.
**Format:** Chronological entries with dates, clear status indicators.

### state.md
Update when: Current focus changes, active plan changes, new blockers, session context shifts.

## Edge Cases

### No .project-context Directory
```
No .project-context directory found. Run `/project-context:init` first to set up context files.
```

### Uncertain Categorization
```
This learning could go in either:
- patterns.md (as a coding pattern)
- architecture.md (as an architectural decision)

Which makes more sense for your project structure?
```

### Large Volume of Learnings
```
I found [N] learnings in our conversation. Would you prefer to:
1. Review and approve all at once
2. Prioritize the top [X] most important ones
3. Review category by category
```

### Conflicting Information
```
This learning conflicts with existing content in [file]:

**Existing:** [Current content]
**New learning:** [Proposed content]

Should I:
1. Replace the old content (learning evolved)
2. Add both with explanation (context-dependent)
3. Skip this update (keep existing)
```

## Examples

### Example 1: After Implementing a Feature

**User:** `/update` (after completing dark mode feature)

**Analysis identifies:**
```markdown
## Proposed Updates

### 1. patterns.md - Theme Management
**Insight:** Established pattern for theme switching with Context API
**Proposed Addition:**
## Theme Management Pattern
Use Context API for app-wide theme state. Store preference in localStorage.
Best practices: manual toggle + system preference detection, CSS variables for colors.

**Rationale:** This pattern worked well and should be reused

### 2. progress.md - Recent Completions
**Insight:** Dark mode feature is complete
**Proposed Addition:**
- **2026-01-04**: Dark Mode Feature — Theme Context, system preference detection, manual toggle, all components updated

**Rationale:** Significant milestone completion

### 3. architecture.md - State Management
**Insight:** Added new global context for theme
**Proposed Addition:** Update React Context diagram to include ThemeContext

**Rationale:** Architectural change to global state structure
```

### Example 2: After Debugging Session

**User:** `/update --chat` (after fixing async bug)

**Analysis identifies:**
```markdown
## Proposed Updates

### 1. patterns.md - Error Handling
**Insight:** Discovered race condition with concurrent API calls
**Proposed Addition:**
## Avoiding Race Conditions
Use abort controllers to cancel stale requests in useEffect.
Anti-pattern: Not canceling previous requests when dependencies change.

**Rationale:** Hard-to-find bug — documenting prevents recurrence
```

### Example 3: Architecture Decision

**User:** `/update` (after choosing database)

**Analysis identifies:**
```markdown
## Proposed Updates

### 1. architecture.md - Database Choice
**Insight:** Decided on PostgreSQL over MongoDB
**Proposed Addition:**
Database: PostgreSQL. Rationale: complex relational queries, ACID compliance, Prisma tooling, team experience.
Trade-offs: rigid schema, more complex setup. Alternatives rejected: MongoDB (no ACID), MySQL (weaker JSON).

**Rationale:** Major architectural decision worth documenting with reasoning
```

## Best Practices

### DO:
- Extract concrete, actionable learnings
- Include code examples where relevant
- Document the "why" behind decisions
- Preserve context for future reference
- Organize by category for easy discovery
- Use consistent formatting with existing files
- Ask for confirmation before applying changes
- Update timestamps and dates

### DON'T:
- Capture trivial or obvious information
- Duplicate existing context
- Make assumptions about user intent
- Apply updates without confirmation
- Ignore existing file structure
- Add redundant or verbose content
- Miss important architectural decisions
