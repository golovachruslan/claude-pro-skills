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
