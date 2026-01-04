---
name: planner
description: "Use when users request feature planning, project planning, or implementation planning. Triggers include: 'plan this feature', 'help me plan', 'what do I need to consider', 'planning this project', 'how should I implement'. Forces clarification questions instead of making assumptions."
allowed-tools:
  - AskUserQuestion
  - Read
  - Write
  - Glob
  - Grep
---

# Feature & Project Planning Skill

Systematically gather requirements through clarifying questions before creating implementation plans. **Never guess or assume** - always ask when information is unclear.

## Core Principle

**Ask, don't assume.** Use the AskUserQuestion tool to clarify requirements, constraints, and expectations before proposing solutions.

## Planning Workflow

### 1. Understand the Request

First, identify what type of planning is needed:
- **Feature planning** - New functionality to add
- **Project planning** - Entire project/system design
- **Implementation planning** - How to build something specific
- **Refactoring planning** - How to improve existing code

### 2. Gather Context

Before asking questions, gather available context:

```bash
# Check for project context
ls .project-context/*.md 2>/dev/null

# Check for relevant documentation
ls README.md CLAUDE.md docs/ 2>/dev/null
```

Read relevant context files to understand:
- Current architecture
- Established patterns
- Tech stack
- Project goals

### 3. Identify Knowledge Gaps

Determine what's unclear or missing. Common gaps:

**Requirements:**
- What problem does this solve?
- Who are the users?
- What are the success criteria?

**Technical constraints:**
- Performance requirements?
- Scale/load expectations?
- Browser/platform support?
- Security/compliance needs?

**Scope:**
- What's in scope vs. out of scope?
- MVP vs. future enhancements?
- Dependencies on other work?

**Design preferences:**
- UI/UX preferences?
- Architecture patterns?
- Library/framework choices?

### 4. Ask Clarifying Questions

Use AskUserQuestion tool to gather missing information. Structure questions clearly:

**Good question format:**
```
I need to understand [aspect] to plan this effectively.

[Question 1]?
[Question 2]?
[Question 3]?

This will help me [explain why this matters for the plan].
```

**Example:**
```
I need to understand the scope and technical constraints to plan the authentication feature.

1. What authentication methods do you want to support (email/password, OAuth, SSO)?
2. Do you need session management or token-based auth (JWT)?
3. What are your security requirements (MFA, password policies)?
4. Should this integrate with existing user management or be built from scratch?

This will help me design the right architecture and identify dependencies.
```

### 5. Ask Follow-up Questions

If initial answers reveal new gaps, ask follow-ups. Common patterns:

**If they choose a complex option:**
```
You mentioned [complex requirement]. Let me clarify:

1. [Specific detail]?
2. [Implementation preference]?
```

**If there's a trade-off:**
```
I see a trade-off between [option A] and [option B]:
- Option A: [pros/cons]
- Option B: [pros/cons]

Which approach aligns better with your priorities?
```

**If scope is unclear:**
```
To define the MVP scope, which of these is most critical for the first version:
1. [Feature A]
2. [Feature B]
3. [Feature C]

The others can be planned for later phases.
```

### 6. Create Structured Plan

Once you have sufficient information, create a comprehensive plan:

#### Plan Structure

```markdown
# [Feature/Project Name] Plan

## Overview
[Brief description of what's being built and why]

## Requirements
### Functional Requirements
- Requirement 1
- Requirement 2

### Non-functional Requirements
- Performance: [expectations]
- Security: [requirements]
- Scalability: [needs]

## Technical Approach
### Architecture
[High-level architecture description, consider Mermaid diagram]

### Technology Choices
- [Technology 1]: [Why chosen]
- [Technology 2]: [Why chosen]

### Key Components
1. **Component Name**
   - Purpose: [what it does]
   - Implementation: [how it works]
   - Dependencies: [what it needs]

## Implementation Phases

### Phase 1: [Name] (MVP)
**Goal:** [What this achieves]
**Tasks:**
- [ ] Task 1
- [ ] Task 2

**Deliverables:**
- Deliverable 1

**Estimated effort:** [If known]

### Phase 2: [Name]
[Same structure]

## Considerations & Trade-offs
### Design Decisions
- **Decision:** [What was decided]
  - Rationale: [Why]
  - Trade-offs: [What we're giving up]

### Risks & Mitigation
- **Risk:** [What could go wrong]
  - Mitigation: [How to address]

### Future Enhancements
- Enhancement 1 (not in current scope)
- Enhancement 2 (dependency: X)

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies
- External dependency 1
- Internal dependency 2

## Next Steps
1. [Immediate next action]
2. [Following action]
```

### 7. Save Plan to Context

Offer to save the plan:

```markdown
I can save this plan to `.project-context/plans/[feature-name].md` so it's preserved across sessions. Would you like me to do that?
```

If yes, create the plan file and update progress.md with reference to the new plan.

## Question-Asking Best Practices

### DO:
- ✅ Ask specific, concrete questions
- ✅ Group related questions together
- ✅ Explain why you're asking (helps user understand importance)
- ✅ Provide context from what you already know
- ✅ Offer options when there are common choices
- ✅ Ask about priorities and trade-offs
- ✅ Clarify scope boundaries (what's in/out)

### DON'T:
- ❌ Guess or assume requirements
- ❌ Ask too many questions at once (max 4-5 per round)
- ❌ Ask questions you could answer from existing docs
- ❌ Ask vague questions like "what do you want?"
- ❌ Make decisions for the user on important trade-offs
- ❌ Skip asking about constraints (performance, security, etc.)

## Example Planning Sessions

### Example 1: Feature Planning

**User:** "I want to add dark mode to my app"

**Assistant uses AskUserQuestion:**
```
I need to understand the scope and technical approach for dark mode.

1. Should dark mode be:
   - System preference based (auto-switch with OS)
   - Manual toggle only
   - Both options available?

2. What's the scope:
   - Entire application
   - Specific sections only?

3. How should the preference be stored:
   - Local storage (browser-only)
   - User profile (persisted across devices)
   - No persistence (resets each session)?

4. Are there any design requirements:
   - Custom color palette
   - Follow existing design system
   - Accessibility requirements (WCAG AA/AAA)?

This will help me plan the implementation approach and identify which components need updates.
```

### Example 2: Project Planning

**User:** "Help me plan a task management app"

**Assistant uses AskUserQuestion:**
```
Let me understand the vision and constraints for this task management app.

1. Target users:
   - Personal use (individual productivity)
   - Team collaboration
   - Both?

2. Core MVP features (pick top 3-4):
   - Create/edit/delete tasks
   - Task organization (lists, tags, projects)
   - Due dates and reminders
   - Priority levels
   - Task assignments (if team)
   - Progress tracking
   - Comments/notes

3. Platform:
   - Web app only
   - Mobile app (iOS/Android)
   - Desktop app
   - Multiple platforms?

4. Data persistence:
   - Cloud-based (sync across devices)
   - Local storage only
   - Offline-first with sync?

5. Technical constraints:
   - Preferred tech stack (if any)
   - Budget constraints
   - Timeline expectations

This will help me create a realistic implementation plan with phases.
```

### Example 3: Implementation Planning

**User:** "How should I implement real-time notifications?"

**Assistant uses AskUserQuestion:**
```
Let me clarify the requirements for real-time notifications.

1. What triggers notifications:
   - User actions (mentions, assignments)
   - System events (deadlines, reminders)
   - External integrations
   - All of the above?

2. Notification delivery:
   - In-app only (while user is active)
   - Push notifications (mobile)
   - Email fallback
   - Multiple channels?

3. Scale expectations:
   - How many concurrent users?
   - How many notifications per user per day?
   - Do you need notification history/archiving?

4. Technical environment:
   - What's your current backend stack?
   - Are you already using WebSockets, Server-Sent Events, or polling?
   - Any infrastructure constraints (serverless, traditional server)?

This will help me recommend the right architecture (WebSockets vs SSE vs polling) and identify necessary infrastructure.
```

## Handling Uncertainty

When the user is uncertain about requirements:

### Technique 1: Offer Examples
```
If you're not sure, here are common approaches for [scenario]:

Option A: [Description]
- Pros: [benefits]
- Cons: [limitations]
- Good for: [use cases]

Option B: [Description]
- Pros: [benefits]
- Cons: [limitations]
- Good for: [use cases]

Which aligns better with your needs, or should we consider another approach?
```

### Technique 2: Start with MVP
```
Since some requirements are still uncertain, I recommend we plan in phases:

Phase 1 (MVP): [Minimal set of features]
- This gets you [core value] with minimal complexity
- We can validate [assumptions] before investing more

Phase 2: [Enhancements based on Phase 1 learnings]

Does this approach work for you, or would you prefer to define more upfront?
```

### Technique 3: Clarify Priorities
```
I hear multiple goals: [goal 1], [goal 2], [goal 3].

What's the priority order? This will help me design the architecture and plan phases accordingly.
```

## Integration with Project Context

### Before Planning
1. Check `.project-context/architecture.md` for current architecture
2. Check `.project-context/patterns.md` for established patterns
3. Check `.project-context/progress.md` for ongoing work that might conflict

### After Planning
1. Offer to save plan to `.project-context/plans/[name].md`
2. Update `.project-context/progress.md` to reference the plan
3. Update `.project-context/architecture.md` if architecture changes

### Plan File Structure
```markdown
# [Feature Name] Plan

**Status:** Planning | In Progress | Completed
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Owner:** [Name or team]

[Rest of plan content following the structure above]
```

## Common Planning Pitfalls to Avoid

1. **Over-planning** - Don't plan every detail upfront. Plan enough to start, iterate as you learn.

2. **Analysis paralysis** - If user can't decide, recommend MVP approach and defer decisions.

3. **Ignoring constraints** - Always ask about performance, security, scale, budget, timeline.

4. **Skipping trade-offs** - Make trade-offs explicit so user makes informed decisions.

5. **Assuming familiarity** - Don't assume user knows technical terms. Explain when needed.

6. **Planning in isolation** - Always check existing architecture and patterns first.

## Success Signals

You've done good planning when:
- ✅ User feels heard and understood
- ✅ All major unknowns have been clarified
- ✅ Plan is actionable with clear next steps
- ✅ Trade-offs and risks are explicit
- ✅ Scope is clearly defined (including what's NOT included)
- ✅ Plan fits within project architecture and patterns
- ✅ User has confidence in the approach

## Reference

For detailed template examples, see:
- `references/planning-templates.md` - Full plan templates
- `references/question-patterns.md` - Question frameworks for different scenarios
