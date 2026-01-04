# Question Patterns for Planning

Structured question frameworks for different planning scenarios. Use these to systematically gather requirements through the AskUserQuestion tool.

## General Planning Framework

### The 5 W's + H Pattern

Always consider:
- **Who:** Who are the users? Who are the stakeholders?
- **What:** What problem are we solving? What are we building?
- **When:** When is this needed? What's the timeline?
- **Where:** Where does this fit in the architecture? Where will it be used?
- **Why:** Why is this needed? Why now?
- **How:** How should this work? How will we measure success?

## Scenario-Specific Question Patterns

### 1. New Feature Planning

#### Initial Discovery Questions
```
I need to understand the feature requirements and context.

1. What problem does this feature solve for users?
   - Who experiences this problem most?
   - How do they currently work around it?

2. What does success look like?
   - How will we know users find this valuable?
   - What metrics should we track?

3. What's the scope for the first version?
   - Must-have vs. nice-to-have features?
   - What can be deferred to later versions?

4. Are there any existing solutions you've seen that you like/dislike?
   - What works well in those solutions?
   - What would you do differently?

This will help me understand the core value proposition and appropriate scope.
```

#### Technical Requirements Questions
```
Now I need to understand the technical constraints and preferences.

1. Performance expectations:
   - How fast should this be? (e.g., "under 200ms response time")
   - How many users/requests should it handle?

2. Platform/browser requirements:
   - Which browsers/devices must be supported?
   - Any specific version requirements?

3. Integration needs:
   - Does this need to integrate with existing systems?
   - Are there external APIs or services involved?

4. Data requirements:
   - What data needs to be stored?
   - Any data retention or privacy requirements?

This will help me design the right technical approach.
```

#### Design & UX Questions
```
Let me clarify the user experience expectations.

1. User interface:
   - Do you have designs/mockups, or should I propose an approach?
   - Any specific UI patterns or components to follow?

2. User flow:
   - Walk me through how a user should interact with this
   - What's the ideal happy path?

3. Error handling:
   - What should happen if [error scenario]?
   - How should we communicate errors to users?

4. Accessibility:
   - Any specific accessibility requirements (WCAG AA/AAA)?
   - Keyboard navigation needed?

This will help me plan the user-facing implementation.
```

### 2. Project Planning

#### Vision & Goals Questions
```
Let me understand the project vision and objectives.

1. What's the main problem this project solves?
   - Who has this problem?
   - How significant is the problem?

2. What are the business/user goals?
   - What outcomes would make this successful?
   - How does this align with broader goals?

3. What's the timeline/urgency?
   - When is this needed?
   - Are there hard deadlines?

4. What resources are available?
   - Team size and skills?
   - Budget constraints?

This will help me create a realistic project plan.
```

#### Scope & Prioritization Questions
```
I need to understand the project scope and priorities.

1. What are the core features/capabilities?
   - What's the minimum viable version?
   - What features are most critical?

2. What's explicitly out of scope?
   - What are we NOT building?
   - What's deferred to future phases?

3. How should we prioritize:
   - Speed to market vs. feature completeness?
   - User experience vs. technical excellence?
   - New features vs. technical debt?

4. What are the must-haves vs. nice-to-haves?
   - What would you cut if timeline is tight?
   - What would you add if we had extra time?

This will help me structure the roadmap and phases.
```

#### Risk & Constraints Questions
```
Let me identify potential risks and constraints upfront.

1. Technical constraints:
   - Must use specific technologies/platforms?
   - Integration with legacy systems?
   - Performance/scale requirements?

2. Resource constraints:
   - Team availability?
   - Budget limitations?
   - Dependency on other teams?

3. Compliance/regulatory:
   - Any regulatory requirements (GDPR, HIPAA, etc.)?
   - Security/audit requirements?
   - Accessibility standards?

4. Known risks:
   - What keeps you up at night about this project?
   - What has gone wrong in similar projects before?

This will help me plan mitigation strategies.
```

### 3. Architecture/System Design Planning

#### System Requirements Questions
```
I need to understand the system requirements and constraints.

1. Scale expectations:
   - How many users (concurrent/total)?
   - Data volume expectations?
   - Growth projections?

2. Performance requirements:
   - Response time expectations?
   - Throughput requirements?
   - Any latency-sensitive operations?

3. Availability requirements:
   - Uptime expectations (99%, 99.9%, 99.99%)?
   - Acceptable downtime windows?
   - Disaster recovery needs?

4. Data requirements:
   - Data consistency needs (eventual vs. strong consistency)?
   - Data retention policies?
   - Backup/recovery requirements?

This will help me design the right architecture.
```

#### Technology Stack Questions
```
Let me clarify technology preferences and constraints.

1. Existing stack:
   - What technologies are you currently using?
   - Any strong preferences or mandates?

2. Team expertise:
   - What languages/frameworks is the team proficient in?
   - Willingness to adopt new technologies?

3. Infrastructure:
   - Cloud provider? (AWS, GCP, Azure)
   - Existing infrastructure to integrate with?
   - Serverless vs. traditional servers?

4. Third-party services:
   - Any existing vendor relationships?
   - Budget for third-party services?
   - Preference for build vs. buy?

This will help me choose appropriate technologies.
```

#### Integration Questions
```
I need to understand integration requirements.

1. What systems need to integrate with this?
   - Internal systems?
   - External APIs?
   - Data sources?

2. How should integration work:
   - Real-time vs. batch?
   - Synchronous vs. asynchronous?
   - Direct API calls vs. message queues?

3. Data exchange:
   - What data needs to be shared?
   - Data formats (JSON, XML, protobuf)?
   - Authentication/authorization?

4. Error handling:
   - What happens if integrated system is down?
   - Retry strategies?
   - Fallback mechanisms?

This will help me plan integration architecture.
```

### 4. Refactoring Planning

#### Current State Questions
```
Let me understand the current state and pain points.

1. What's not working well currently?
   - Specific pain points?
   - How often do these cause issues?

2. Impact of current issues:
   - How does this affect development velocity?
   - How does this affect users/performance?
   - Any incidents caused by this?

3. Previous attempts:
   - Has this been attempted before?
   - What prevented success?

4. Metrics:
   - How do we measure the problem currently?
   - What metrics would show improvement?

This will help me understand the refactoring motivation.
```

#### Refactoring Approach Questions
```
I need to clarify the refactoring strategy.

1. Risk tolerance:
   - Can we afford downtime?
   - How critical is this system?
   - What's the blast radius if something goes wrong?

2. Timeline:
   - When must this be complete?
   - Can we do incremental refactoring or need big bang?

3. Backward compatibility:
   - Must maintain existing APIs/contracts?
   - Any clients that can't be updated immediately?

4. Testing:
   - What test coverage exists currently?
   - Can we add tests before refactoring?

This will help me plan the safest refactoring approach.
```

### 5. Performance Optimization Planning

#### Performance Problem Questions
```
Let me understand the performance issues.

1. What's slow?
   - Specific operations/pages?
   - Consistent or intermittent?
   - When did this start?

2. How slow is it?
   - Current metrics (response time, load time)?
   - What's acceptable?
   - What's the target improvement?

3. User impact:
   - How many users affected?
   - What's the business impact?

4. Investigation so far:
   - Any profiling done?
   - Suspected bottlenecks?
   - Recent changes that might have caused this?

This will help me focus the optimization effort.
```

#### Optimization Constraints Questions
```
I need to understand constraints on the optimization approach.

1. Scope of changes:
   - Can we change the architecture?
   - Can we change the database schema?
   - Must maintain backward compatibility?

2. Resource availability:
   - Can we add servers/resources?
   - Budget for infrastructure?
   - Can we use caching services (Redis, etc.)?

3. Timeline:
   - When is the fix needed?
   - Can we do quick wins first, then deeper optimization?

4. Acceptable trade-offs:
   - Speed vs. consistency?
   - Performance vs. code complexity?
   - Cost vs. performance?

This will help me prioritize optimization strategies.
```

### 6. API Design Planning

#### API Requirements Questions
```
Let me understand the API requirements.

1. API consumers:
   - Who will use this API? (internal teams, external partners, public)
   - What programming languages will they use?

2. Use cases:
   - What are the primary use cases?
   - What operations are needed?
   - Expected call volume/patterns?

3. Data model:
   - What resources/entities are exposed?
   - Relationships between entities?

4. API style preference:
   - REST, GraphQL, gRPC, or other?
   - Any existing APIs to match in style?

This will help me design the right API.
```

#### API Design Details Questions
```
I need to clarify API design details.

1. Authentication & authorization:
   - How should clients authenticate? (API keys, OAuth, JWT)
   - What authorization model? (RBAC, ABAC)

2. Versioning:
   - How should we handle API versioning?
   - Breaking change tolerance?

3. Rate limiting:
   - Should we rate limit?
   - What limits are appropriate?

4. Response format:
   - Pagination approach?
   - Error format?
   - Envelope vs. raw responses?

5. Documentation:
   - OpenAPI/Swagger?
   - Code examples needed?
   - Interactive API explorer?

This will help me design a robust API.
```

### 7. Database Design Planning

#### Data Requirements Questions
```
Let me understand the data requirements.

1. Data entities:
   - What are the main entities/concepts?
   - Relationships between entities?

2. Data volume:
   - How much data initially?
   - Growth expectations?
   - Data retention needs?

3. Access patterns:
   - Most common queries?
   - Read-heavy or write-heavy?
   - Real-time or analytical queries?

4. Data characteristics:
   - Structured or unstructured?
   - Schema stability (frequent changes)?

This will help me choose the right database approach.
```

#### Database Technology Questions
```
I need to clarify database technology choices.

1. Database type preference:
   - Relational (PostgreSQL, MySQL)?
   - NoSQL (MongoDB, DynamoDB)?
   - Graph (Neo4j)?
   - Time-series (InfluxDB)?

2. Consistency requirements:
   - Strong consistency needed?
   - Eventual consistency acceptable?

3. Transactions:
   - Multi-record transactions needed?
   - ACID requirements?

4. Infrastructure:
   - Managed service (RDS, Aurora) or self-hosted?
   - Backup/recovery requirements?
   - Geographic distribution needs?

This will help me recommend the right database.
```

### 8. Security Feature Planning

#### Security Requirements Questions
```
Let me understand the security requirements.

1. What are we protecting:
   - User data (PII, financial data)?
   - Business data (proprietary information)?
   - System integrity?

2. Threat model:
   - Who are potential attackers?
   - What are they trying to do?
   - What's most valuable to protect?

3. Compliance:
   - Any regulatory requirements (GDPR, HIPAA, PCI-DSS)?
   - Industry standards to follow?
   - Audit requirements?

4. Current security posture:
   - Existing security measures?
   - Known vulnerabilities?
   - Previous security incidents?

This will help me design appropriate security measures.
```

#### Security Implementation Questions
```
I need to clarify security implementation details.

1. Authentication:
   - Password-based, OAuth, SSO, MFA?
   - Session management approach?

2. Authorization:
   - Role-based access control (RBAC)?
   - Attribute-based access control (ABAC)?
   - Permission granularity?

3. Data protection:
   - Encryption at rest?
   - Encryption in transit?
   - Key management?

4. Monitoring & response:
   - Security event logging?
   - Intrusion detection?
   - Incident response plan?

This will help me implement comprehensive security.
```

## Question Sequencing Strategies

### Funnel Approach
Start broad, then narrow:
1. **High-level vision** - What are we trying to achieve?
2. **Key requirements** - What must this do?
3. **Constraints** - What limitations exist?
4. **Details** - Specific implementation preferences

### Iterative Approach
Ask initial questions, analyze responses, then ask follow-ups:
1. **Round 1:** Core requirements (4-5 questions)
2. **Analyze:** Identify gaps and ambiguities
3. **Round 2:** Follow-up questions on unclear areas
4. **Repeat:** Until sufficient clarity

### Priority Approach
Start with highest-impact unknowns:
1. **Blockers first** - Questions that could invalidate the approach
2. **Architecture next** - Questions that affect major decisions
3. **Details last** - Questions about implementation specifics

### Persona-Based Approach
Tailor questions to user's expertise:

**For technical users:**
- Use technical terminology
- Ask about architecture, patterns, trade-offs
- Assume technical knowledge

**For non-technical users:**
- Use plain language
- Ask about outcomes, not implementation
- Offer options with explanations

## Multi-Round Question Examples

### Round 1: Initial Discovery
```
I need to understand the core requirements for [feature].

1. What problem does this solve, and for whom?
2. What does success look like?
3. Are there any hard constraints (timeline, budget, technology)?
4. Have you seen similar solutions you like?

This will help me determine the right approach.
```

### Round 2: Follow-up Based on Responses

If they mentioned **multiple user types:**
```
You mentioned [user type A] and [user type B] will use this.

1. Do they have different needs/workflows?
2. Should the experience differ for each, or unified?
3. Which user type should we prioritize for MVP?

This will help me design for the right audience.
```

If they mentioned **integration requirements:**
```
You mentioned integration with [system].

1. What data needs to flow between systems?
2. Real-time sync or batch updates?
3. Is the API documented? Any known limitations?
4. Who owns that system (for coordination)?

This will help me plan the integration approach.
```

If they mentioned **performance concerns:**
```
You mentioned performance is important.

1. What's the expected load (users, requests)?
2. What response time is acceptable vs. ideal?
3. Are there specific operations that must be fast?
4. Any budget for infrastructure (caching, CDN)?

This will help me design for adequate performance.
```

## Question Anti-Patterns

### ❌ Don't Do This

**Vague questions:**
```
What do you want this to do?
```
*Too open-ended, doesn't guide the user*

**Leading questions:**
```
You want this to use React, right?
```
*Biases the answer, limits exploration*

**Too many questions:**
```
[15 questions in one message]
```
*Overwhelming, user won't answer all thoroughly*

**Technical jargon to non-technical users:**
```
Do you need idempotency for the API endpoints?
```
*User may not understand, will guess*

**Questions answerable from docs:**
```
What framework is the codebase using?
```
*Could read package.json or README instead*

### ✅ Do This Instead

**Specific, actionable questions:**
```
Should users be able to edit their posts after publishing, or only before?
```
*Clear, concrete, easy to answer*

**Open exploration:**
```
What frontend framework would you prefer, if any? (e.g., React, Vue, Svelte, vanilla JS)
```
*Offers guidance without bias*

**Focused question sets:**
```
Let me start with 4 key questions about scope...
[4 well-structured questions]
```
*Manageable, user can answer thoughtfully*

**Plain language with context:**
```
If a request fails partway through, should it automatically retry, or should the user retry manually?
```
*No jargon, explains the concept*

**Context-aware questions:**
```
I see you're using Express in the backend. Should this new API follow the same routing pattern, or is this a chance to try a different approach?
```
*Shows you did homework, asks informed question*

## Contextual Question Helpers

### When Requirements Are Vague

**Offer examples:**
```
To clarify the scope, here are some examples of what this could include:
- Option A: [Simple version]
- Option B: [Medium version]
- Option C: [Complex version]

Which aligns closest with your vision, or is it something else?
```

### When User Is Uncertain

**Provide decision framework:**
```
I understand you're not sure about [decision]. Here's how to think about it:

If [condition A], then [approach A] is better because [reason].
If [condition B], then [approach B] is better because [reason].

Which condition applies to your situation?
```

### When Technical Trade-offs Exist

**Explain trade-offs clearly:**
```
There's a trade-off between [option A] and [option B]:

**Option A** (e.g., client-side rendering):
- Pros: [faster navigation, better UX]
- Cons: [slower initial load, SEO challenges]
- Best for: [interactive apps with logged-in users]

**Option B** (e.g., server-side rendering):
- Pros: [faster initial load, better SEO]
- Cons: [more server load, more complex caching]
- Best for: [content-heavy sites, public-facing pages]

Which aligns better with your priorities?
```

### When Scope Needs Bounding

**Suggest MVP approach:**
```
This could be quite large in scope. To get value quickly, I recommend phasing it:

**Phase 1 (MVP):** [Core features that deliver immediate value]
**Phase 2:** [Enhancements once MVP is validated]
**Phase 3:** [Advanced features]

Does this phasing make sense, or should we adjust?
```

## Questions by Project Type

### Greenfield Project
Focus on: Vision, constraints, technical choices
```
1. What's the core problem this solves?
2. Who are the target users?
3. Any constraints (timeline, budget, technology)?
4. Team size and expertise?
5. Preferred tech stack, if any?
```

### Enhancement to Existing System
Focus on: Current state, integration, compatibility
```
1. What's not working well currently?
2. What must remain backward compatible?
3. What existing patterns should this follow?
4. What dependencies exist?
5. Can we refactor, or must we extend?
```

### Migration/Rewrite
Focus on: Current pain points, migration path, risk
```
1. What problems with the current system are we solving?
2. What must work exactly the same?
3. What can we improve/change?
4. Migration strategy (big bang vs. incremental)?
5. What's the risk tolerance?
```

### Bug Fix
Focus on: Root cause, scope, regression prevention
```
1. What's the exact behavior (expected vs. actual)?
2. How to reproduce reliably?
3. When did this start?
4. What changed recently?
5. How widespread is the impact?
```

## Using Questions to Uncover Hidden Requirements

### Surface performance requirements:
```
You mentioned [feature]. A couple of follow-ups:

1. How many [items] do you expect users to have?
   - If it's thousands, we'll need pagination/virtualization
2. Should this work on slow connections/mobile?
   - Affects how we handle loading states
```

### Surface security requirements:
```
You mentioned [user data]. Let me clarify:

1. Is any of this data sensitive (PII, financial)?
   - Affects encryption, access control needs
2. Who should be able to see/edit this data?
   - Affects authorization model
```

### Surface accessibility requirements:
```
You mentioned [UI feature]. Accessibility questions:

1. Must this work with screen readers?
2. Is keyboard navigation required?
3. Any specific WCAG level to target?
```

### Surface scalability requirements:
```
You mentioned [feature]. Scale considerations:

1. Expected user base (now and in 1-2 years)?
2. Geographic distribution (single region or global)?
3. Any spike patterns (viral potential, seasonal)?
```

## Summary: Question-Asking Principles

1. **Start broad, then narrow** - Vision → requirements → details
2. **Ask in rounds** - Don't overwhelm with 20 questions at once
3. **Explain why you're asking** - Helps user understand importance
4. **Offer options when helpful** - Guides without biasing
5. **Use plain language** - Adjust to user's technical level
6. **Build on previous answers** - Show you're listening
7. **Make trade-offs explicit** - Help user make informed decisions
8. **Validate assumptions** - Don't guess, ask
9. **Know when to stop asking** - Enough to start, not perfect knowledge
10. **Summarize understanding** - "So to clarify, you want [X]?" - Confirm before planning
