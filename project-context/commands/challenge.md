---
name: project-context:challenge
description: Challenge a plan or code change from adversarial perspectives to find weaknesses
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Challenge Plan or Code

Force critical evaluation of the current plan or code change using the `project-context:challenge-it` skill.

## Modes

Parse the arguments to determine mode:

- **No arguments** — Standard mode, auto-detect target from conversation
- **`plan`** — Challenge a plan specifically
- **`code`** — Challenge code/implementation specifically
- **`--quick`** — Quick mode, top 3 concerns only
- **`--brutal`** — Brutal mode, assume flawed + add domain critics
- **Quoted text** — Focus on specific aspect (e.g., `"focus on security"`)

Arguments can be combined: `/challenge code --quick`, `/challenge --brutal "security focus"`

## Workflow

1. **Parse mode** from arguments
2. **Check for `.project-context/`** — read architecture.md and patterns.md if available
3. **Identify target** — What's being challenged (from conversation or user specification)
4. **Apply Six Critics framework** — Analyze from all adversarial perspectives
5. **In brutal mode** — Add 2-3 domain-specific critics from `references/critic-frameworks.md`
6. **Synthesize** — Prioritize concerns by severity
7. **Offer to log** — If project-context available, offer to save to `.project-context/plans/challenge-*.md`
8. **Ask direction** — "Which of these should we address before proceeding?"

## If No Clear Target

If there's no clear plan or code to challenge in the conversation:

```
I don't see a clear plan or code change to challenge. Could you:
1. Share what you'd like me to critique
2. Reference a specific proposal from our conversation
3. Share a code diff or implementation plan
```

## Output

Use the output format from the challenge-it skill:
- Standard mode: All six perspectives + prioritized concerns + recommendation
- Quick mode: Top 3 concerns with actions
- Brutal mode: Six critics + domain critics, harsher analysis

Always end with: "Which of these should we address before proceeding?"
