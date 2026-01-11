---
name: retro
description: "Use when users request retrospective analysis or learning extraction. Triggers include: 'retro', 'retrospective', 'what did we learn', 'extract learnings', 'summarize our work', 'capture insights'. Analyzes conversation to extract key learnings, decisions, patterns, and updates .project-context files."
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Retrospective Analysis Skill

Analyzes conversation history to extract key learnings, decisions, patterns, errors, and insights. Proposes updates to `.project-context/` files to preserve valuable knowledge across sessions.

## Core Principle

**Capture learnings systematically.** Extract meaningful insights from conversations and preserve them in the right context files for future reference.

## Retrospective Workflow

### 1. Analyze Conversation

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

### 2. Check Existing Context

Read existing `.project-context/` files to understand current state:

```bash
# Check what files exist
ls .project-context/*.md 2>/dev/null
```

Read relevant files:
- `.project-context/brief.md` - For scope/goal changes
- `.project-context/architecture.md` - For architectural decisions/diagrams
- `.project-context/patterns.md` - For patterns and learnings
- `.project-context/progress.md` - For status updates

### 3. Categorize Learnings

Map extracted insights to appropriate files:

| Category | Target File | Examples |
|----------|-------------|----------|
| Project goals, scope changes | `brief.md` | "Pivoted to focus on mobile-first experience" |
| Architecture decisions, tech choices | `architecture.md` | "Switched from REST to GraphQL", diagram updates |
| Coding patterns, conventions | `patterns.md` | "Using custom hooks for data fetching" |
| Bug fixes, learnings, anti-patterns | `patterns.md` | "Avoid prop drilling - use Context API" |
| Completed work, current status | `progress.md` | "Completed auth system, starting on dashboard" |
| Design decisions | `architecture.md` or `patterns.md` | "Using optimistic updates for better UX" |

### 4. Propose Updates

For each identified learning, propose specific updates:

**Format:**
```markdown
## Proposed Updates

### 1. [File Name] - [Section]
**Insight:** [What was learned]
**Proposed Addition:**
```
[Exact text to add, maintaining file's existing format]
```

**Rationale:** [Why this belongs here]
```

**Example:**
```markdown
## Proposed Updates

### 1. patterns.md - Error Handling
**Insight:** Discovered that async errors in event handlers need explicit try-catch
**Proposed Addition:**
```markdown
## Error Handling Patterns

### Async Event Handlers
Always wrap async operations in try-catch when called from event handlers:

```javascript
const handleSubmit = async (e) => {
  e.preventDefault()
  try {
    await api.submitForm(data)
  } catch (error) {
    setError(error.message)
  }
}
```

**Rationale:** Event handlers don't automatically catch async errors, causing unhandled rejections.
```
**Rationale:** This pattern was discovered after debugging unhandled promise rejections

### 2. progress.md - Completed Work
**Insight:** Authentication system is now complete
**Proposed Addition:**
```markdown
## Recent Completions
- **2026-01-04**: Authentication system
  - Email/password login
  - JWT token management
  - Protected route middleware
  - Session persistence
```
**Rationale:** Tracks significant milestone completion
```

### 5. Ask User Confirmation

Use AskUserQuestion to present proposed updates and get approval:

**Good confirmation format:**
```
I've analyzed our conversation and identified [N] key learnings to capture in .project-context files.

## Proposed Updates

[List all proposed updates with clear sections]

Questions:
1. Do these updates accurately capture our learnings?
2. Should any updates be modified, added, or removed?
3. Are the target files appropriate, or should anything go elsewhere?

I'll apply the approved updates once you confirm.
```

### 6. Apply Approved Updates

After user confirms, update the files:

**For each approved update:**
1. Read the target file
2. Identify the correct section (or create if needed)
3. Use Edit tool to add content in appropriate location
4. Maintain existing formatting and structure

**Example workflow:**
```bash
# Read current file
Read .project-context/patterns.md

# Add new content to appropriate section
Edit file to insert learning in relevant section

# Verify update was successful
Read updated section to confirm
```

### 7. Summarize Changes

After applying updates, provide a summary:

```markdown
✅ Retrospective updates applied to .project-context files:

- **patterns.md**: Added error handling pattern for async event handlers
- **progress.md**: Documented authentication system completion
- **architecture.md**: Updated auth flow diagram

These learnings are now preserved for future sessions.
```

## Analysis Techniques

### Conversation Pattern Recognition

Look for these signals in conversation:

**Learning signals:**
- "I learned that..."
- "It turns out..."
- "The solution was to..."
- "This works better than..."
- "We should always/never..."

**Decision signals:**
- "We decided to..."
- "Going with [option] because..."
- "Chose [X] over [Y] due to..."
- "The trade-off is..."

**Pattern signals:**
- "This pattern works well..."
- "Consistently using..."
- "Standard approach is..."
- "Following convention of..."

**Error signals:**
- "The bug was caused by..."
- "Fixed by..."
- "Common mistake is..."
- "Watch out for..."

**Progress signals:**
- "Completed..."
- "Finished implementing..."
- "Now working on..."
- "Next step is..."

### Context Extraction

For each identified insight:

1. **Extract the core learning** - What's the essential insight?
2. **Identify the context** - When/why does this apply?
3. **Capture the rationale** - Why was this decision made?
4. **Note alternatives** - What other options were considered?
5. **Document the outcome** - What was the result?

### Quality Filters

Only capture insights that are:
- ✅ **Actionable** - Can be applied in future work
- ✅ **Specific** - Concrete examples, not vague generalizations
- ✅ **Contextual** - Include when/why it applies
- ✅ **Valuable** - Worth preserving for future reference
- ❌ **Not trivial** - Skip obvious or one-off details
- ❌ **Not redundant** - Don't duplicate existing context

## File-Specific Guidelines

### brief.md Updates

Add to brief.md when:
- Project goals or vision changes
- Target users or use cases evolve
- Scope significantly expands or contracts
- Core requirements shift

**Format:** Update relevant sections, add new sections if needed

### architecture.md Updates

Add to architecture.md when:
- New technology is adopted
- Architecture patterns change
- System components are added/modified
- Integration points are established
- Flows change (update Mermaid diagrams)

**Format:** Add diagrams with descriptions, document tech choices with rationale

### patterns.md Updates

Add to patterns.md when:
- Coding pattern is established
- Convention is adopted
- Best practice is identified
- Anti-pattern is discovered
- Solution to common problem is found

**Format:** Organized by category (Error Handling, State Management, etc.)

### progress.md Updates

Add to progress.md when:
- Feature is completed
- Milestone is reached
- Current work changes
- Blocker is resolved
- Next steps are identified

**Format:** Chronological entries with dates, clear status indicators

## Edge Cases

### No .project-context Directory

If `.project-context/` doesn't exist:
```
I found valuable learnings in our conversation, but no .project-context directory exists.

Would you like me to:
1. Initialize project context with `/project-context:init`, then add these learnings?
2. Just summarize the learnings without persisting them?
```

### Uncertain Categorization

If unsure which file to update:
```
This learning could go in either:
- patterns.md (as a coding pattern)
- architecture.md (as an architectural decision)

Which makes more sense for your project structure?
```

### Large Volume of Learnings

If many learnings are identified:
```
I found [N] learnings in our conversation. This is quite a lot.

Would you prefer to:
1. Review and approve all at once
2. Prioritize the top [X] most important ones
3. Review category by category (patterns, progress, etc.)
```

### Conflicting Information

If proposed update conflicts with existing context:
```
I noticed this learning conflicts with existing content in [file]:

**Existing:** [Current content]
**New learning:** [Proposed content]

Should I:
1. Replace the old content (learning evolved)
2. Add both with explanation (context-dependent)
3. Skip this update (keep existing)
```

## Examples

### Example 1: After Implementing a Feature

**User:** "/project-context:retro" (after completing dark mode feature)

**Assistant analyzes and proposes:**
```markdown
I've analyzed our dark mode implementation session. Here are the key learnings:

## Proposed Updates

### 1. patterns.md - Theme Management
**Insight:** Established pattern for theme switching with Context API
**Proposed Addition:**
```markdown
## Theme Management Pattern

Use Context API for app-wide theme state:

```javascript
// themes/ThemeContext.js
export const ThemeContext = createContext()
export const useTheme = () => useContext(ThemeContext)

// App.js
<ThemeProvider>
  <App />
</ThemeProvider>
```

**Best Practices:**
- Store preference in localStorage for persistence
- Provide both manual toggle and system preference detection
- Use CSS variables for theme colors (easier switching)
```
**Rationale:** This pattern worked well and should be reused for future theming needs

### 2. progress.md - Recent Completions
**Insight:** Dark mode feature is complete
**Proposed Addition:**
```markdown
## Recent Completions
- **2026-01-04**: Dark Mode Feature
  - Theme Context with localStorage persistence
  - System preference detection
  - Manual toggle in settings
  - Updated all components to use theme variables
```
**Rationale:** Significant feature completion worth documenting

### 3. architecture.md - State Management
**Insight:** Added new global context for theme
**Proposed Addition:**
Update the React Context diagram to include ThemeContext alongside existing contexts
**Rationale:** Architectural change to global state structure

Do these updates look good? Should I modify anything before applying?
```

### Example 2: After Debugging Session

**User:** "/project-context:retro" (after fixing complex async bug)

**Assistant analyzes and proposes:**
```markdown
I've analyzed our debugging session. Key learning identified:

## Proposed Updates

### 1. patterns.md - Error Handling
**Insight:** Discovered race condition with concurrent API calls
**Proposed Addition:**
```markdown
## Avoiding Race Conditions

When making sequential API calls, use abort controllers to cancel stale requests:

```javascript
useEffect(() => {
  const controller = new AbortController()

  async function fetchData() {
    try {
      const result = await api.getData(id, { signal: controller.signal })
      setData(result)
    } catch (error) {
      if (error.name !== 'AbortError') {
        handleError(error)
      }
    }
  }

  fetchData()
  return () => controller.abort()
}, [id])
```

**Anti-pattern:** Not canceling previous requests when dependencies change leads to race conditions and stale data.
```
**Rationale:** This bug was hard to find - documenting the solution prevents recurrence

Does this accurately capture the learning?
```

### Example 3: Architecture Decision

**User:** "/project-context:retro" (after choosing database solution)

**Assistant analyzes and proposes:**
```markdown
## Proposed Updates

### 1. architecture.md - Database Choice
**Insight:** Decided on PostgreSQL over MongoDB
**Proposed Addition:**
```markdown
## Database: PostgreSQL

**Choice:** PostgreSQL
**Rationale:**
- Need for complex relational queries (user permissions, multi-table joins)
- ACID compliance critical for financial transactions
- Better tooling for migrations (we use Prisma)
- Team has more PostgreSQL experience

**Trade-offs:**
- More rigid schema (requires migrations for changes)
- Slightly more complex setup than MongoDB
- Vertical scaling limits (acceptable for current scale)

**Alternatives considered:**
- MongoDB: Rejected due to lack of ACID guarantees for transactions
- MySQL: Similar to PostgreSQL but weaker JSON support
```
**Rationale:** Major architectural decision that should be documented with reasoning

### 2. progress.md - Current Work
**Insight:** Database setup is in progress
**Proposed Addition:**
```markdown
## Current Work
- **Database Setup**
  - PostgreSQL instance configured
  - Prisma ORM integrated
  - Initial schema designed
  - TODO: Run migrations, seed data
```
**Rationale:** Tracks current state of database work

Are these updates appropriate?
```

## Best Practices

### DO:
- ✅ Extract concrete, actionable learnings
- ✅ Include code examples where relevant
- ✅ Document the "why" behind decisions
- ✅ Preserve context for future reference
- ✅ Organize by category for easy discovery
- ✅ Use consistent formatting with existing files
- ✅ Ask for confirmation before applying changes
- ✅ Update timestamps and dates

### DON'T:
- ❌ Capture trivial or obvious information
- ❌ Duplicate existing context
- ❌ Make assumptions about user intent
- ❌ Apply updates without confirmation
- ❌ Ignore existing file structure
- ❌ Add redundant or verbose content
- ❌ Miss important architectural decisions

## Success Signals

You've done a good retro when:
- ✅ All significant learnings are identified
- ✅ Insights are categorized appropriately
- ✅ Updates fit naturally into existing context files
- ✅ User confirms the analysis is accurate
- ✅ Future sessions benefit from preserved knowledge
- ✅ Nothing important is forgotten or lost
