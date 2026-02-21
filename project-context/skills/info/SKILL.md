---
name: info
description: "Answer questions about the current project's codebase, architecture, dependencies, patterns, and implementation details. Use when users ask questions like 'how does X work?', 'where is Y implemented?', 'what does this project do?', 'what dependencies do we use?', 'explain the auth flow', 'how are tests organized?', or any question about the project. Triggers: project questions, codebase questions, 'how does', 'where is', 'what is', 'explain', 'show me', 'find where', 'why does', architecture questions, implementation questions."
---

# Info Skill

Research and answer questions about the current project by combining structured context files with live codebase exploration.

## Workflow

### 1. Gather Context Layer (project-context files)

Check for `.project-context/` files first — they provide high-level project knowledge:

```bash
ls .project-context/*.md 2>/dev/null
```

If found, read files relevant to the question:

| Question About | Read |
|---------------|------|
| Project purpose, goals | `brief.md` |
| Tech stack, system design | `architecture.md` |
| Current status, blockers | `state.md` |
| What's done / in progress | `progress.md` |
| Code conventions, learnings | `patterns.md` |

Also check for `CLAUDE.md`, `README.md`, or similar project docs at the repo root — these often contain build commands, architecture notes, and conventions.

If no context files exist, skip to step 2. Do NOT suggest initialization — focus on answering the question.

### 2. Research the Codebase

Use targeted codebase exploration to find the answer. Choose strategy based on question type:

**"Where is X?"** — Find files/symbols
- Glob for file patterns matching the concept
- Grep for class/function/variable names
- Report file paths with line numbers

**"How does X work?"** — Trace execution flow
- Find the entry point (Grep for function/class name)
- Read the implementation
- Follow key dependencies one level deep
- Summarize the flow

**"What does this project do?"** — High-level overview
- Read project root files (package.json, Cargo.toml, pyproject.toml, go.mod, etc.)
- Scan directory structure
- Read main entry points
- Combine with context files if available

**"Why does X?"** — Understand rationale
- Read the relevant code
- Check git log for the file/function (`git log --oneline -10 -- <file>`)
- Look for comments, docs, or ADRs explaining the decision

**General / complex questions** — Use parallel research
- Launch an Explore subagent via Task tool for broad research
- Combine findings with context files

### 3. Synthesize the Answer

- **Lead with the direct answer** — don't bury it under context
- **Cite specific files and line numbers** — use `file_path:line_number` format
- **Include short code snippets** when they clarify the answer
- **Note gaps** — if something is unclear or undocumented, say so
- **Keep it concise** — answer the question, don't dump everything found

### 4. Suggest Follow-ups (only when natural)

If the research revealed related useful information:
- Mention it briefly ("Related: the caching layer at `src/cache.ts` also touches this")
- Do NOT suggest running commands or initializing things unless directly relevant
