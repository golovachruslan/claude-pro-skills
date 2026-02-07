---
name: project-context:challenge
description: Challenge a plan or code change from adversarial perspectives to find weaknesses
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Task
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
- **`--team`** — Force Agent Teams mode, each critic as a separate teammate
- **`--solo`** — Skip Agent Teams even if enabled, use subagents or sequential
- **`--strategy teams|subagents|sequential`** — Explicit strategy selection
- **Quoted text** — Focus on specific aspect (e.g., `"focus on security"`)

Arguments can be combined: `/challenge code --quick`, `/challenge --brutal --solo "security focus"`

## Execution Strategy

Resolve from flags first, then auto-detect:

1. **`--solo`** → skip Agent Teams, use subagents or sequential
2. **`--team`** → force Agent Teams (shorthand for `--strategy teams`)
3. **`--strategy X`** → use specified strategy
4. **No flags** → auto-detect: Agent Teams (if enabled + brutal mode) > Task subagents > Sequential

### Agent Teams Mode (`--team` / `--strategy teams` / auto in brutal mode)

When Agent Teams are available (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), launch critics as independent teammates for deeper, truly parallel analysis:

- **Each critic perspective** runs as a separate teammate with its own context window
- **Critics can message each other** to cross-reference concerns and challenge each other's findings
- **Team lead** (this session) synthesizes all critic reports into a unified assessment
- **Richer analysis** — each critic has full context budget for deep investigation

**Teammate assignment:**
```
Teammate 1: Skeptic        — challenges assumptions, demands evidence
Teammate 2: Pragmatist     — evaluates cost vs value, complexity
Teammate 3: Chaos Engineer — probes failure modes, edge cases
Teammate 4: Architect      — checks design fit, patterns, SOLID
Teammate 5: Root Cause     — diagnoses problem correctness
Teammate 6: Future Dev     — assesses maintainability, readability

Team lead: synthesizes reports, resolves conflicting concerns, prioritizes
```

In brutal mode, add 2-3 domain-specific critic teammates from `references/domain-critics/`.

### Task Subagents Mode (`--solo` / `--strategy subagents` / default)

When Agent Teams are not available or `--solo` is specified, use subagents for parallel critic analysis:
- Launch 2-3 Task subagents with different critic groupings
- Each subagent analyzes from 2-3 perspectives
- Main session synthesizes results

### Sequential Mode (`--strategy sequential` / fallback)

Analyze from all perspectives sequentially in the main session.

## Workflow

1. **Parse mode and flags** from arguments
2. **Check for `.project-context/`** — read architecture.md and patterns.md if available
3. **Identify target** — What's being challenged (from conversation or user specification)
4. **Select execution strategy** — resolve from flags, then auto-detect
5. **Apply Six Critics framework** — Analyze from all adversarial perspectives
6. **In brutal mode** — Add 2-3 domain-specific critics from `references/critic-frameworks.md`
7. **Synthesize** — Prioritize concerns by severity (team lead merges critic reports)
8. **Offer to log** — If project-context available, offer to save to `.project-context/plans/challenge-*.md`
9. **Ask direction** — "Which of these should we address before proceeding?"

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
- Team mode: Each critic's independent report + synthesized assessment

Always end with: "Which of these should we address before proceeding?"
