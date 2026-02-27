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

## Modes

**Context Detection (default):** Auto-detects whether challenging a plan or code. User can override: `/challenge plan` or `/challenge code` or `/challenge "focus on security"`.

**Depth Modes:**
- **Standard (default)** — All six perspectives, detailed analysis
- **Quick (`--quick`)** — Top 3 concerns only, faster iteration
- **Brutal (`--brutal`)** — Assume flawed + add domain-specific critics

## Integration with project-context

When `.project-context/` exists:
1. Read architecture context before challenging code changes
2. Check established patterns to validate architectural fit
3. Log challenges to `.project-context/plans/challenge-*.md`
4. Reference past decisions that may be relevant

## The Six Core Critics

| Critic | Focus | Key Questions |
|--------|-------|---------------|
| **Skeptic** | Assumptions & evidence | What are we assuming without validation? What if our premise is wrong? |
| **Pragmatist** | Cost vs value | Is this the simplest approach? What's the ongoing maintenance cost? |
| **Chaos Engineer** | Failure modes | What could go wrong? Edge cases? What breaks under load? |
| **Architect** | Design fit | Does this align with existing architecture? Coupling? Pattern consistency? |
| **Root Cause** | Problem diagnosis | Solving symptom or cause? Is the problem correctly identified? |
| **Future Dev** | Maintainability | Will this make sense in 6 months? Readable? Testable? |

## Workflow

1. **Gather Context** — Check `.project-context/*.md` if available, identify what's being challenged
2. **State the Challenge** — Clearly identify what's being evaluated with context note
3. **Analyze from All Six Perspectives** — Apply each critic, use project context for specificity, state "No critical concerns" if perspective finds nothing
4. **Synthesize and Prioritize** — Rank: Critical (blocks proceeding) → Important (address before merge) → Worth considering (may defer)
5. **Offer to Log** — If project-context available, offer to log challenge and resolution
6. **Ask for Direction** — End with: "Which of these should we address before proceeding?"

## Critical Rules

- **Be genuinely adversarial.** Don't softball. Look hard before saying nothing's wrong.
- **Challenge the idea, not the person.**
- **Be specific and actionable.** Each concern should point to something testable or changeable.
- **Use project context.** Reference actual architecture, patterns, and past decisions when available.
- **Prioritize ruthlessly.** Critical issues first. Nice-to-haves last or cut in quick mode.

## References

- **Output format templates**: See `references/output-formats.md` — standard, quick, brutal, and challenge log formats
- **Examples**: See `references/examples.md` — plan challenge, quick mode, focused critique, edge cases
- **Domain-specific critics (brutal mode)**: See `references/critic-frameworks.md` and `references/domain-critics/`
