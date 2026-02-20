# Best Practices for Project Context

## Core Principles

1. **Concise** — Scannable bullet points, not encyclopedic prose. Link to detailed docs.
2. **Current** — Stale context is worse than no context. Update after significant changes.
3. **Honest** — Document what IS, not what should be. Include known issues and debt.
4. **Useful** — Write for someone new. Include "why" not just "what". Make it actionable.

## File-Specific Guidelines

| File | Update When | Don't |
|------|-------------|-------|
| `brief.md` | Scope/goals change (rarely) | Include implementation details |
| `architecture.md` | New components/flows added | Document every file/function |
| `state.md` | Every session start/end | Let it grow beyond ~50 lines |
| `progress.md` | Tasks complete/start | Track micro-tasks |
| `patterns.md` | New pattern established | Document obvious patterns |
| `dependencies.json` | Dependencies added/removed | List every import — just key boundaries |

## Staleness Indicators

| File | Stale If |
|------|----------|
| `brief.md` | >30 days + active development |
| `architecture.md` | >7 days + code structure changes |
| `state.md` | >1 day during active development |
| `progress.md` | >3 days during active development |
| `patterns.md` | >14 days + new patterns in code |
| `dependencies.json` | >30 days + new dependencies added |

## Mermaid Diagrams

- One concept per diagram
- Use clear labels (full words, not abbreviations)
- Group related nodes with subgraphs
- **Every diagram MUST have a text description below it**

## Managed Sections in CLAUDE.md / AGENTS.md

project-context uses HTML comment markers to delimit managed sections:
```markdown
<!-- PROJECT-CONTEXT:START -->
[Auto-managed content]
<!-- PROJECT-CONTEXT:END -->
```

- Content between markers is auto-updated by commands
- Content outside markers is never modified
- Safe to run init/update multiple times (idempotent)

## Monorepo / dependencies.json

### When to Use
- Monorepos with 2+ subprojects that share code, APIs, or types
- Any project that imports from or exports to a sibling project

### Guidelines

| Aspect | Guideline |
|--------|-----------|
| **Upstream/Downstream** | Declare both directions; `/add-dependency` offers reciprocal updates |
| **Paths** | Use relative paths from the project root (`../shared`, `../api`) |
| **Integration Points** | List key files at boundaries, not every import |
| **Impact Rules** | Focus on breaking-change scenarios only |
| **Staleness** | `dependencies.json` changes rarely (30-day threshold) — update when deps change |

### Reciprocal Declarations

If `api` lists `shared` as upstream, then `shared` should list `api` as downstream. The `/project-context:add-dependency` command handles this automatically by offering to update both sides.

### Context Resolution in Monorepos

When working in a subproject:
1. Read that subproject's `.project-context/` first
2. Check `dependencies.json` for upstream/downstream relationships
3. Only pull in a dependency's `brief.md` + `architecture.md` when touching integration boundaries
4. Never load a dependency's `state.md` or `progress.md` — that's their internal concern

### Monorepo Initialization

Each subproject gets its own `/project-context:init`. The root can also have a `.project-context/` for system-wide architecture and shared patterns.

## Common Mistakes

1. **Too much detail** → Link to docs, keep context high-level
2. **Never updating** → Build updates into workflow
3. **No diagrams** → Add Mermaid for every architectural flow
4. **Diagrams without descriptions** → Always add step-by-step text
5. **Optimistic progress** → Be honest about blockers
6. **Duplicating CLAUDE.md** → Reference context files, don't duplicate
7. **One-way dependency declarations** → Always declare both upstream and downstream
8. **Loading all dependency contexts** → Only load brief + architecture, not state/progress
