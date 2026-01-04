# Retrospective Analysis Patterns

Detailed patterns for extracting learnings from different types of conversations.

## Pattern 1: Feature Implementation Sessions

### Signals to Look For
- "Implemented [feature]"
- "Added [functionality]"
- "Built [component]"
- Technical decisions made during implementation
- Challenges encountered and solved

### What to Extract

**For patterns.md:**
- Code patterns established
- Libraries or utilities created
- Design patterns applied
- Common solutions to problems

**For progress.md:**
- Feature completion status
- Implementation details
- Time/effort spent (if mentioned)
- Dependencies on other work

**For architecture.md:**
- New components added
- Integration points
- Data flow changes
- Updated diagrams

### Example Analysis

**Conversation excerpt:**
```
User: Let's add user authentication
Assistant: [Implements JWT-based auth with refresh tokens]
User: Great! Can we also add OAuth with Google?
Assistant: [Adds OAuth integration]
```

**Extracted learnings:**
1. **architecture.md**: "Authentication using JWT + refresh token strategy"
2. **patterns.md**: "OAuth integration pattern with passport.js"
3. **progress.md**: "Completed: Authentication system with JWT and Google OAuth"

## Pattern 2: Debugging Sessions

### Signals to Look For
- "The bug was..."
- "Fixed by..."
- "The issue was caused by..."
- "Root cause:"
- Error messages and stack traces discussed

### What to Extract

**For patterns.md:**
- Common bugs and solutions
- Debugging techniques that worked
- Anti-patterns to avoid
- Preventive measures

**For progress.md:**
- Bug resolved (if significant)
- Remaining known issues
- Testing outcomes

### Example Analysis

**Conversation excerpt:**
```
User: Getting "Cannot read property of undefined" in production
Assistant: This is a race condition - component renders before data loads
Assistant: Fixed with optional chaining and loading states
```

**Extracted learnings:**
1. **patterns.md**: "Use optional chaining and loading states to prevent race conditions"
2. **patterns.md**: "Anti-pattern: Accessing nested properties without null checks"

## Pattern 3: Architecture Decisions

### Signals to Look For
- "Decided to use..."
- "Switching from X to Y"
- "Better to use..."
- "Chose [option] because..."
- Trade-off discussions

### What to Extract

**For architecture.md:**
- Technology choices with rationale
- Architectural patterns adopted
- System design decisions
- Integration approaches

**For brief.md** (if scope-impacting):
- Changes to project scope
- New requirements
- Shifted priorities

### Example Analysis

**Conversation excerpt:**
```
User: Should we use REST or GraphQL?
Assistant: Given you need flexible queries and have multiple clients, GraphQL is better
User: Agreed, let's go with GraphQL
Assistant: I'll use Apollo Server for the backend
```

**Extracted learnings:**
1. **architecture.md**: "API: GraphQL with Apollo Server. Rationale: Flexible queries, multiple clients (web + mobile), better DX for frontend team"
2. **architecture.md**: Add GraphQL architecture diagram

## Pattern 4: Planning & Design Discussions

### Signals to Look For
- "The plan is to..."
- "We'll approach this by..."
- "Breaking down into phases"
- Requirements gathering
- Scope definition

### What to Extract

**For brief.md:**
- Project goals clarified
- Target users identified
- Core requirements defined
- Success criteria

**For architecture.md:**
- High-level design decisions
- System components planned
- Integration points identified

**For progress.md:**
- Planned work items
- Phases defined
- Priorities set

### Example Analysis

**Conversation excerpt:**
```
User: I want to build a task management app for teams
Assistant: [Asks clarifying questions about features, scale, etc.]
User: MVP should have task creation, assignment, and basic collaboration
Assistant: [Creates implementation plan with phases]
```

**Extracted learnings:**
1. **brief.md**: "Project: Team task management. Target: Small teams (5-20 people). MVP: Create, assign, collaborate on tasks"
2. **progress.md**: "Planned Phases: 1) Core task CRUD, 2) Team features, 3) Real-time collaboration"

## Pattern 5: Refactoring Sessions

### Signals to Look For
- "Refactored [component/module]"
- "Improved [aspect]"
- "Extracted [pattern]"
- "Cleaned up..."
- Performance improvements

### What to Extract

**For patterns.md:**
- New patterns established
- Code organization principles
- Performance optimizations
- Reusable abstractions

**For progress.md:**
- Refactoring completed
- Code quality improvements
- Tech debt addressed

### Example Analysis

**Conversation excerpt:**
```
User: This component is getting too large
Assistant: Let's extract the form logic into a custom hook
Assistant: [Creates useTaskForm hook]
User: Much cleaner!
```

**Extracted learnings:**
1. **patterns.md**: "Custom Hook Pattern: Extract complex form logic into reusable hooks (e.g., useTaskForm)"
2. **progress.md**: "Refactored task form component - extracted logic to custom hook"

## Pattern 6: Learning & Discovery

### Signals to Look For
- "I learned that..."
- "Discovered [fact/limitation]"
- "It turns out..."
- "Interesting finding:"
- Unexpected behaviors

### What to Extract

**For patterns.md:**
- New knowledge about tools/libraries
- Gotchas and edge cases
- Best practices discovered
- Workarounds for limitations

### Example Analysis

**Conversation excerpt:**
```
User: Why isn't React re-rendering?
Assistant: Object mutation doesn't trigger re-renders - you need to create new objects
User: Ah! So I should use spread operator
Assistant: Exactly, or use immer for complex state
```

**Extracted learnings:**
1. **patterns.md**: "React State Immutability: Always create new objects/arrays when updating state. Use spread operator or immer library"
2. **patterns.md**: "Anti-pattern: Mutating state directly (state.items.push()) - won't trigger re-render"

## Pattern 7: Configuration & Setup

### Signals to Look For
- "Set up [tool/service]"
- "Configured [environment]"
- "Integrated [third-party]"
- Environment variables
- Build configuration changes

### What to Extract

**For architecture.md:**
- Build tools and configuration
- Development environment setup
- CI/CD pipeline
- Third-party services integrated

**For patterns.md:**
- Configuration patterns
- Environment management
- Deployment procedures

### Example Analysis

**Conversation excerpt:**
```
User: Let's add TypeScript
Assistant: [Configures tsconfig.json, adds type definitions]
User: Also set up ESLint and Prettier
Assistant: [Configures linting and formatting]
```

**Extracted learnings:**
1. **architecture.md**: "TypeScript configured with strict mode. ESLint + Prettier for code quality"
2. **patterns.md**: "Use TypeScript strict mode for better type safety. Pre-commit hooks run linting/formatting"

## Pattern 8: Performance Optimization

### Signals to Look For
- "Optimized [component/query]"
- "Performance improved by..."
- "Reduced [metric]"
- "Memoized..."
- Load time discussions

### What to Extract

**For patterns.md:**
- Optimization techniques applied
- Performance patterns
- Memoization strategies
- Query optimization

**For progress.md:**
- Performance improvements made
- Benchmarks (if measured)
- Remaining optimization opportunities

### Example Analysis

**Conversation excerpt:**
```
User: The dashboard is slow with large datasets
Assistant: Implemented virtualization for the list
Assistant: Added useMemo for expensive calculations
Assistant: Debounced the search input
User: Much faster now!
```

**Extracted learnings:**
1. **patterns.md**: "Performance: Use react-window for virtualizing long lists (>100 items)"
2. **patterns.md**: "Performance: Memoize expensive calculations with useMemo, debounce user inputs"
3. **progress.md**: "Optimized dashboard performance - added virtualization and memoization"

## Pattern 9: Testing & Quality Assurance

### Signals to Look For
- "Wrote tests for..."
- "Test coverage..."
- "Found edge case:"
- "Testing strategy..."
- CI/CD setup

### What to Extract

**For patterns.md:**
- Testing patterns
- Test organization
- Mocking strategies
- Edge cases discovered

**For progress.md:**
- Test coverage status
- Testing milestones
- QA findings

### Example Analysis

**Conversation excerpt:**
```
User: How should we test the API calls?
Assistant: Use MSW (Mock Service Worker) to mock API responses
Assistant: [Sets up test with MSW]
User: This is much better than mocking fetch
```

**Extracted learnings:**
1. **patterns.md**: "Testing API calls: Use MSW (Mock Service Worker) for realistic API mocking. Better than mocking fetch directly"
2. **progress.md**: "Set up testing infrastructure with Jest + MSW"

## Extraction Decision Tree

```
Is this learning...

├─ About project goals/scope?
│  └─ → brief.md
│
├─ About system architecture/tech choices?
│  └─ → architecture.md
│
├─ About coding patterns/conventions?
│  └─ → patterns.md
│
├─ About work completed/in-progress?
│  └─ → progress.md
│
└─ Unclear/spans multiple categories?
   └─ → Ask user for guidance
```

## Quality Checklist

Before proposing an update, verify:

- [ ] **Specific**: Includes concrete examples/code?
- [ ] **Actionable**: Can be applied in future work?
- [ ] **Contextual**: Explains when/why it applies?
- [ ] **Non-redundant**: Doesn't duplicate existing content?
- [ ] **Valuable**: Worth preserving for future reference?
- [ ] **Well-organized**: Fits into existing file structure?
- [ ] **Clear**: Easy to understand months later?

## Common Mistakes to Avoid

### ❌ Too Granular
```markdown
# Bad
Added semicolon to line 42
```

### ✅ Right Level of Detail
```markdown
# Good
Established convention: Use semicolons consistently (enforced by ESLint)
```

### ❌ Too Vague
```markdown
# Bad
Made the code better
```

### ✅ Specific and Actionable
```markdown
# Good
Refactored error handling to use a centralized error boundary instead of try-catch in every component
```

### ❌ Missing Context
```markdown
# Bad
Use Redux for state management
```

### ✅ Includes Rationale
```markdown
# Good
Use Redux for state management. Rationale: Complex state shared across many components, need time-travel debugging, team familiar with Redux patterns
```

### ❌ No Examples
```markdown
# Bad
Use composition pattern for components
```

### ✅ Includes Example
```markdown
# Good
Use composition pattern for components:

```javascript
// Instead of prop drilling
<Button variant="primary" size="large" disabled={loading} />

// Use composition
<Button>
  <Icon name="save" />
  Save Changes
</Button>
```
```
