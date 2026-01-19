# Domain-Specific Critic Frameworks

Extended perspectives for `--brutal` mode. These critics activate based on the context being challenged.

## When to Add Domain Critics

In brutal mode, add 2-3 domain-specific critics based on:
- The nature of what's being challenged
- Project context (tech stack, domain, constraints)
- User-specified focus areas

## Domain Critics

### Security Critic

**Activates when:** Authentication, authorization, API endpoints, data handling, external integrations, user input processing.

**Focus:** Attack vectors, vulnerabilities, compliance

**Questions:**
- What attack vectors does this introduce or expand?
- How could a malicious actor exploit this?
- What's the blast radius if compromised?
- Are secrets properly managed?
- Input validation and sanitization?
- Output encoding (XSS prevention)?
- SQL injection / command injection risks?
- Authentication/authorization gaps?
- Sensitive data exposure in logs, errors, URLs?
- OWASP Top 10 violations?

**Format:**
```markdown
### Security Critic
Attack surface analysis:
- [Vulnerability 1]
- [Vulnerability 2]

Compliance concerns:
- [Issue 1]

**Severity:** [Critical/High/Medium/Low]
```

---

### Performance Critic

**Activates when:** Database operations, API endpoints, loops, data processing, caching discussions, scale requirements mentioned.

**Focus:** Speed, resource usage, scalability bottlenecks

**Questions:**
- What's the time complexity? O(n), O(n²), worse?
- Database query efficiency? N+1 problems?
- Memory allocation patterns?
- Network round trips?
- Blocking operations in async code?
- Resource leaks (connections, file handles)?
- How does this behave at 10x, 100x current load?
- Are there hot paths that will be called frequently?
- Caching opportunities or cache invalidation risks?
- Index usage in database queries?

**Format:**
```markdown
### Performance Critic
Bottleneck analysis:
- [Bottleneck 1] — Impact: [description]
- [Bottleneck 2] — Impact: [description]

Scale concerns (at 10x load):
- [Issue]

**Optimization priority:** [High/Medium/Low]
```

---

### UX Critic

**Activates when:** UI changes, user flows, error messages, notifications, onboarding, accessibility.

**Focus:** User experience, accessibility, clarity

**Questions:**
- What's the user's mental model? Does this match?
- Error states and feedback — clear and actionable?
- Loading states — does user know what's happening?
- Edge cases in the UI (empty states, long text, etc.)?
- Accessibility (WCAG compliance)?
- Keyboard navigation?
- Screen reader compatibility?
- Color contrast and visual hierarchy?
- Mobile/responsive considerations?
- Cognitive load — is this overwhelming?
- Recovery paths when things go wrong?

**Format:**
```markdown
### UX Critic
User experience concerns:
- [Issue 1]
- [Issue 2]

Accessibility gaps:
- [Issue]

**User impact:** [High/Medium/Low]
```

---

### Data Critic

**Activates when:** Database schema changes, data migrations, analytics, reporting, data pipelines, ML features.

**Focus:** Data integrity, consistency, compliance

**Questions:**
- Data validation at boundaries?
- Referential integrity maintained?
- What happens to existing data during migration?
- Rollback strategy for data changes?
- PII handling and GDPR/CCPA compliance?
- Data retention policies?
- Backup and recovery implications?
- Audit trail requirements?
- Data consistency across services?
- Analytics/reporting impact?
- Data quality monitoring?

**Format:**
```markdown
### Data Critic
Integrity concerns:
- [Issue 1]

Compliance considerations:
- [Issue]

Migration risks:
- [Risk]

**Data risk level:** [High/Medium/Low]
```

---

### Operations Critic

**Activates when:** Deployment changes, infrastructure, monitoring, logging, CI/CD, scaling, reliability.

**Focus:** Deployability, observability, reliability

**Questions:**
- How do we deploy this safely? Feature flags? Canary?
- Rollback plan if something goes wrong?
- What metrics and alerts are needed?
- Logging sufficient for debugging production issues?
- Health checks and readiness probes?
- Resource requirements (CPU, memory, storage)?
- Dependencies on external services — failure handling?
- Configuration management?
- Secret rotation?
- Disaster recovery implications?
- On-call impact?

**Format:**
```markdown
### Operations Critic
Deployment concerns:
- [Issue 1]

Observability gaps:
- [Issue]

Reliability risks:
- [Risk]

**Ops complexity:** [High/Medium/Low]
```

---

### Testing Critic

**Activates when:** New features, refactoring, bug fixes, integration points, complex logic.

**Focus:** Testability, coverage, confidence

**Questions:**
- How will this be tested?
- Unit test coverage for new code?
- Integration test coverage for boundaries?
- Edge cases covered in tests?
- Test data management?
- Mocking strategy — are we testing real behavior?
- Performance/load testing needed?
- Security testing requirements?
- Regression risk assessment?
- Manual testing required? QA checklist?
- Feature flag testing scenarios?

**Format:**
```markdown
### Testing Critic
Testability concerns:
- [Issue 1]

Coverage gaps:
- [Gap]

Confidence assessment:
- [Assessment]

**Test priority:** [High/Medium/Low]
```

---

### Cost Critic

**Activates when:** Cloud resources, third-party services, API usage, data storage, scaling decisions.

**Focus:** Financial impact, resource efficiency

**Questions:**
- Cloud resource cost implications?
- Third-party API costs (per-request pricing)?
- Data storage costs (especially at scale)?
- Egress/bandwidth costs?
- License implications?
- Compute optimization opportunities?
- Reserved vs. on-demand tradeoffs?
- Cost monitoring and alerts in place?
- ROI of this change?
- Hidden costs (support, maintenance, training)?

**Format:**
```markdown
### Cost Critic
Direct costs:
- [Cost 1]

Hidden costs:
- [Cost]

Scale implications:
- [Implication]

**Cost risk:** [High/Medium/Low]
```

---

### API Critic

**Activates when:** API design, endpoint changes, contract changes, versioning, integrations.

**Focus:** Contract stability, usability, compatibility

**Questions:**
- Is this a breaking change?
- Versioning strategy?
- Backward compatibility maintained?
- API contract documented?
- Error responses consistent and useful?
- Rate limiting considered?
- Authentication/authorization correct?
- Idempotency for unsafe operations?
- Pagination for list endpoints?
- Response size and performance?
- SDK/client impact?

**Format:**
```markdown
### API Critic
Contract concerns:
- [Issue 1]

Compatibility risks:
- [Risk]

Consumer impact:
- [Impact]

**API stability risk:** [High/Medium/Low]
```

---

### Concurrency Critic

**Activates when:** Async code, parallel processing, shared state, database transactions, distributed systems.

**Focus:** Race conditions, deadlocks, consistency

**Questions:**
- Race conditions possible?
- Shared mutable state?
- Locking strategy correct?
- Deadlock potential?
- Transaction isolation level appropriate?
- Optimistic vs. pessimistic locking?
- Eventual consistency implications?
- Ordering guarantees needed?
- Idempotency for retries?
- Thread safety?
- Event ordering in async flows?

**Format:**
```markdown
### Concurrency Critic
Race condition risks:
- [Risk 1]

Consistency concerns:
- [Concern]

Synchronization issues:
- [Issue]

**Concurrency risk:** [High/Medium/Low]
```

---

## Selection Matrix

Use this matrix to select domain critics based on challenge context:

| Challenge Type | Primary Domain Critics |
|----------------|------------------------|
| API endpoint | Security, API, Performance |
| Database schema | Data, Performance, Operations |
| UI feature | UX, Testing, Performance |
| Authentication | Security, Data, Testing |
| Infrastructure | Operations, Cost, Security |
| Integration | API, Security, Operations |
| Data pipeline | Data, Performance, Cost |
| Refactoring | Testing, Performance, Future Dev |
| Scaling | Performance, Cost, Operations |
| User flow | UX, Testing, Accessibility |

## Brutal Mode Guidelines

When using `--brutal` mode:

1. **Assume flawed** — Start with the premise that something is wrong
2. **Add 2-3 domain critics** — Select based on context
3. **No benefit of the doubt** — If something could go wrong, it will
4. **Specific failures** — Describe exactly how it will break
5. **Worst-case scenarios** — Consider Murphy's Law
6. **Question everything** — Even "obvious" decisions

**Brutal mode opener:**
```markdown
## Challenging: [target]

**Mode:** Brutal — This analysis assumes the approach has flaws we need to find.

**Domain critics activated:** [Critic 1], [Critic 2], [Critic 3]

[Standard six critics with harsher lens...]

[Domain-specific critics...]
```
