---
name: challenge-it
description: "Force critical evaluation of plans or code changes from adversarial perspectives. Use when Claude accepts a proposal too readily, before committing to significant decisions, when something feels off but is hard to articulate, or when stress-testing an approach. Triggers: 'challenge this', 'critique', 'stress-test', 'play devil''s advocate', 'what could go wrong', 'poke holes in'. Integrates with project-context for codebase-aware analysis."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Challenge-It

Force critical evaluation by analyzing from multiple adversarial perspectives.

## When This Activates

- `/challenge` command
- Requests to "challenge", "critique", or "stress-test" a proposal
- When asked to "play devil's advocate" or "poke holes"
- Questions like "what could go wrong?" or "what am I missing?"
- Before committing to significant decisions

## Modes

**Context Detection (default):**
- Auto-detects whether challenging a plan or code based on conversation context
- User can override: `/challenge plan` or `/challenge code`
- User can provide focus: `/challenge "focus on security implications"`

**Depth Modes:**
- **Standard (default)** — All six perspectives, detailed analysis
- **Quick (`--quick`)** — Top 3 concerns only, faster iteration
- **Brutal (`--brutal`)** — Assume flawed + add domain-specific critics

## Integration with project-context

When `.project-context/` exists:

1. **Read architecture context** before challenging code changes
2. **Check established patterns** to validate architectural fit concerns
3. **Log challenges** to `.project-context/plans/challenge-*.md` for decision documentation
4. **Reference past decisions** that may be relevant

If `.project-context/` doesn't exist, skill works standalone.

## The Six Core Critics

| Critic | Focus | Key Questions |
|--------|-------|---------------|
| **Skeptic** | Assumptions & evidence | What are we assuming without validation? What if our premise is wrong? |
| **Pragmatist** | Cost vs value | Is this the simplest approach? What's the ongoing maintenance cost? Over-engineered? |
| **Chaos Engineer** | Failure modes | What could go wrong? Edge cases? Error handling? What breaks under load? |
| **Architect** | Design fit | Does this align with existing architecture? Coupling? SOLID violations? Pattern consistency? |
| **Root Cause** | Problem diagnosis | Solving symptom or cause? Is the problem correctly identified? Band-aid or real fix? |
| **Future Dev** | Maintainability | Will this make sense in 6 months? Readable? Testable? What context is needed to understand? |

## Workflow

### 1. Gather Context

**Check for project-context:**
```bash
ls .project-context/*.md 2>/dev/null
```

**If available, read relevant files:**
- `.project-context/architecture.md` — Tech stack, system design
- `.project-context/patterns.md` — Established patterns
- `.project-context/brief.md` — Project goals and constraints

**Identify what's being challenged:**
- Recent plan discussed in conversation
- Code diff or implementation
- Architecture decision
- User-specified target

### 2. State the Challenge

Clearly identify what's being evaluated:

```
## Challenging: [the thing being challenged]

**Context:** [Brief note on what informed this analysis]
```

### 3. Analyze from All Six Perspectives

For each critic:
- Apply the perspective to find genuine concerns
- Use project context to make concerns specific
- Reference actual patterns/code when relevant
- If no significant concerns from a perspective, state: "No critical concerns from this perspective"

### 4. Synthesize and Prioritize

Rank concerns by severity:
1. **Critical** — Blocks proceeding
2. **Important** — Should address before merge/commit
3. **Worth considering** — May defer with acknowledgment

### 5. Offer to Log (if project-context available)

Ask if user wants to log the challenge and resolution:
```
Would you like me to log this challenge to `.project-context/plans/challenge-[topic].md`?
```

### 6. Ask for Direction

End with: "Which of these should we address before proceeding?"

## Output Format

### Standard Output (Default)

```markdown
## Challenging: [proposal/plan/code being challenged]

**Context:** [What informed this analysis — architecture docs, patterns, etc.]

### Skeptic
[Challenge from assumptions/evidence perspective]
- Specific concern 1
- Specific concern 2

### Pragmatist
[Challenge from cost/value perspective]
- Specific concern 1
- Specific concern 2

### Chaos Engineer
[Challenge from failure modes perspective]
- Specific concern 1
- Specific concern 2

### Architect
[Challenge from design fit perspective — informed by project-context if available]
- Specific concern 1
- Specific concern 2

### Root Cause
[Challenge from problem diagnosis perspective]
- Specific concern 1
- Specific concern 2

### Future Dev
[Challenge from maintainability perspective]
- Specific concern 1
- Specific concern 2

---

**Key Concerns (Prioritized):**
1. [Critical — what blocks proceeding]
2. [Important — should address before merge/commit]
3. [Worth considering — may defer]

**Recommendation:** [Proceed / Address concerns first / Reconsider approach]

Which of these should we address before proceeding?
```

### Quick Output (`--quick`)

```markdown
## Challenging: [thing]

**Top Concerns:**

1. **[Most critical concern]** (Perspective: [Critic])
   - Why it matters
   - Suggested action

2. **[Second concern]** (Perspective: [Critic])
   - Why it matters
   - Suggested action

3. **[Third concern]** (Perspective: [Critic])
   - Why it matters
   - Suggested action

Address these before proceeding?
```

### Brutal Output (`--brutal`)

Same as standard but:
- Add 2-3 domain-specific critics based on context (see `references/critic-frameworks.md`)
- Assume flawed: "Find what's wrong" mandate for each perspective
- Harsher language, no benefit of the doubt
- Explicitly state: "This analysis assumes the approach has flaws we need to find"

## Critical Rules

**Be genuinely adversarial.** Don't softball. If a perspective finds nothing wrong, say so — but look hard first.

**Challenge the idea, not the person.** Focus on weaknesses in the approach, not who proposed it.

**Be specific and actionable.** Each concern should point to something that can be investigated, tested, or changed. Vague concerns are useless.

**Use project context.** When available, reference actual architecture, patterns, and past decisions. "This violates our established repository pattern in `src/repos/`" is better than "This might not fit the architecture."

**Acknowledge strengths briefly.** If something is well-designed, note it in one line before diving into concerns. Don't dwell on positives — that's not why we're here.

**Prioritize ruthlessly.** Not all concerns are equal. Critical issues come first. Nice-to-haves go last or get cut in quick mode.

**Log decisions.** When project-context is available, offer to log the challenge and resolution for future reference.

## Challenge Log Format

When logging to `.project-context/plans/challenge-*.md`:

```markdown
# Challenge: [Topic]

**Date:** YYYY-MM-DD
**Status:** Reviewing | Addressed | Accepted as-is | Rejected
**Target:** [What was challenged — plan, code, decision]

## Summary
[1-2 sentence description of what was challenged]

## Key Concerns Raised
1. **[Concern]** (Critic: [Perspective])
   - [Detail]
2. **[Concern]** (Critic: [Perspective])
   - [Detail]

## Resolution
[How concerns were addressed, or why they were accepted as-is]

## Outcome
[What was decided and why]
```

## Examples

### Example 1: Challenging a Plan (with project-context)

**User:** "I'm planning to add Redis caching. /challenge"

**Output:**

```markdown
## Challenging: Add Redis caching layer to improve API response times

**Context:** Reviewed `.project-context/architecture.md` — current stack is Express + PostgreSQL. No caching infrastructure exists. Team size: 3 developers per `brief.md`.

### Skeptic
What evidence shows caching will help?
- No profiling data referenced in the proposal
- Have we confirmed slow responses are from repeated computations vs. DB queries vs. network?
- Adding cache without measurements is optimizing blind

### Pragmatist
Redis adds significant operational complexity for a 3-person team:
- New service to deploy, monitor, scale
- Cache invalidation logic to maintain
- Simpler alternatives exist:
  - In-memory LRU cache (no new infrastructure)
  - HTTP cache headers (leverage existing CDN)
  - Database query optimization

### Chaos Engineer
Cache failure modes are notoriously subtle:
- Stale data after writes — what's the business impact?
- Cache stampede after restart — cold cache + traffic spike
- No cache warming strategy mentioned
- Degradation behavior when Redis is down?

### Architect
Per `architecture.md`, project follows "minimal infrastructure" principle:
- Redis would be first external stateful service besides PostgreSQL
- No existing team expertise in Redis operations
- Alternative: PostgreSQL materialized views align with existing stack

### Root Cause
Caching treats a symptom, not the cause:
- What queries are slow? Missing indexes?
- N+1 query patterns in the API layer?
- Caching may mask problems that compound as data grows

### Future Dev
Cache-related bugs are hard to debug:
- "Works locally" because cache state differs
- How will new devs understand what's cached?
- Invalidation logic becomes tribal knowledge

---

**Key Concerns (Prioritized):**
1. No profiling data — guessing at root cause
2. May be masking real issues (query optimization, N+1s)
3. Operational complexity high for team size

**Recommendation:** Address concerns first — profile API, check queries, then decide if caching needed.

Which of these should we address before proceeding?
```

### Example 2: Quick Mode

**User:** "/challenge --quick"

**Context:** Reviewing a PR with retry logic.

**Output:**

```markdown
## Challenging: Retry logic with exponential backoff in HttpClient

**Top Concerns:**

1. **No maximum retry limit visible** (Chaos Engineer)
   - Could retry indefinitely on persistent failures
   - Causes resource exhaustion, blocks other requests
   - **Action:** Add `maxRetries` parameter with sensible default (3-5)

2. **Duplicates existing pattern** (Architect)
   - Similar retry logic exists in `src/clients/external_api.py:45-62`
   - Violates DRY, creates maintenance burden
   - **Action:** Extract to shared `RetryPolicy` utility

3. **Magic numbers without context** (Future Dev)
   - `backoff_multiplier=2`, `base_delay_ms=100` are hardcoded
   - Future devs won't know why these values
   - **Action:** Extract to config or add comments explaining choices

Address these before merging?
```

### Example 3: User-Specified Focus

**User:** "/challenge 'focus on security implications'"

**Output:**

```markdown
## Challenging: Webhook endpoint for third-party integrations

**Focus:** Security implications (user-specified)

### Skeptic (Security Lens)
- How do we verify webhook payloads are from legitimate sources?
- No mention of signature verification (HMAC, etc.)
- What data is exposed in webhook payloads? PII? Credentials?

### Chaos Engineer (Security Lens)
- Webhook endpoints are common DDoS vectors
- Rate limiting strategy?
- Replay attacks — are webhooks idempotent?

### Architect (Security Lens)
- Where does webhook secret storage live?
- Webhook logs may contain sensitive data — retention policy?

### Future Dev (Security Lens)
- How do developers test webhooks locally without exposing secrets?
- Documentation for secure webhook setup?

---

**Key Concerns (Prioritized):**
1. No payload signature verification — anyone can send fake webhooks
2. No rate limiting — trivial DDoS target
3. Secret storage approach undefined

**Recommendation:** Address security concerns first — this is attack surface expansion.

Which of these should we address before proceeding?
```

## Edge Cases

### No Clear Target
If unclear what to challenge:
```
I don't see a clear plan or code change to challenge. Could you:
1. Share what you'd like me to critique
2. Reference a specific proposal from our conversation
3. Share a code diff or implementation plan
```

### Already Well-Designed
If genuinely well-designed after thorough analysis:
```
After analyzing from all six perspectives, this approach is solid:

**Strengths noted:**
- [Strength 1]
- [Strength 2]

**Minor considerations (not blocking):**
- [Minor point]

**Recommendation:** Proceed — no significant concerns found.
```

### User Disagrees with Concerns
If user pushes back on a concern:
```
I understand. Let me clarify my reasoning:

[Explain the concern more specifically]

If you've already considered this and have mitigations in place, that addresses my concern.
Would you like me to document this in the challenge log as "accepted with mitigation"?
```

## Reference

For domain-specific critics (brutal mode), see:
- `references/critic-frameworks.md` — Extended perspectives for Security, Performance, UX, Data, etc.
