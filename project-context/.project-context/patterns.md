# Patterns & Learnings

## Code Patterns
- Skills invoke agents for heavy lifting; agents write results to files to avoid bloating orchestrator context
- Python scripts used for deterministic file operations (managing sections with HTML comment markers)
- `<!-- PROJECT-CONTEXT:START -->` / `<!-- PROJECT-CONTEXT:END -->` for managed CLAUDE.md sections

## Naming Conventions
- Skills: hyphen-case (`add-dependency`, `plan-verification`)
- Context files: lowercase noun (`brief.md`, `state.md`)
- Plans: stored under `.project-context/plans/`
- Deps cache: `.deps-cache/` at project root, flat copy (no `.git/`)

## Learnings
- Flat copy cache (no .git/) keeps deps lightweight and avoids nested git issues
- Merging fetch-deps into add-dependency command simplifies UX (fewer commands)
- Context files should be concise — LLM context window is precious

## Anti-Patterns
- Avoid LLM string manipulation for structured file edits — use Python scripts
- Don't store session-specific data in permanent context files

---
*Last updated: 2026-02-20*
