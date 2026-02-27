# Update Skill: Examples, Edge Cases & Guidelines

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
