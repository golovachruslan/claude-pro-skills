---
name: update
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

- `file` (optional): Specific file to update — `brief`, `architecture`, `state`, `progress`, `patterns`. If omitted: smart update of relevant files.
- `--source` (optional): `--chat` (conversation analysis), `--scan` (git diff), `--input` (interactive). Default: smart detection.

## Workflow

### Step 1: Verify Context Exists

```bash
ls .project-context/*.md 2>/dev/null
```

If not found: "Run `/project-context:init` first."

### Step 2: Determine Update Source

1. Meaningful conversation context (decisions, learnings, completed work) → `--chat`
2. Git status shows changes but no meaningful conversation → `--scan`
3. Otherwise → prompt for `--input`

## --chat Mode: Deep Conversation Analysis

### 2a. Analyze Conversation

Review conversation to identify:
- **Key Learnings**: New knowledge, what worked, what didn't
- **Decisions Made**: Technical choices, trade-offs, rationale
- **Patterns Discovered**: Coding patterns, best practices, anti-patterns
- **Errors & Solutions**: Bugs fixed, debugging insights
- **Progress Updates**: Features completed, blockers resolved, next steps

Use signal recognition from `references/analysis-patterns.md`.

### 2b–2c. Check Existing Context & Categorize

Read existing `.project-context/` files to avoid redundancy. Map insights to target files:

| Category | Target File |
|----------|-------------|
| Project goals, scope changes | `brief.md` |
| Architecture decisions, tech choices | `architecture.md` |
| Coding patterns, conventions, anti-patterns | `patterns.md` |
| Completed work, current status | `progress.md` |
| Current focus, blockers, next action | `state.md` |

### 2d–2f. Propose → Confirm → Apply

Propose specific updates with insight, proposed text, and rationale. Get explicit user approval before applying. Then edit target files, maintaining existing formatting.

## --scan Mode

```bash
git diff --stat HEAD~5 2>/dev/null || git status --short
```

Analyze for: new components → `architecture.md`, new patterns → `patterns.md`, completed work → `progress.md`.

## --input Mode

Ask user specific questions based on the file being updated.

## Step 3: Refresh Managed Sections

```bash
python project-context/scripts/manage_context.py update-sections --file CLAUDE.md
python project-context/scripts/manage_context.py update-sections --file AGENTS.md
```

## Quality Filters

Only capture insights that are: **Actionable**, **Specific**, **Contextual**, **Valuable**, **Not trivial**, **Not redundant**.

## References

- **File-specific guidelines, examples, edge cases, best practices**: See `references/examples-and-guidelines.md`
- **Signal recognition patterns**: See `references/analysis-patterns.md`
