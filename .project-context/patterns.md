# Patterns & Learnings

## Code Patterns
- Plugin manifests use `plugin.json` with name, version, description, author, keywords, and component paths (commands, skills, agents)
- Skills follow SKILL.md structure with YAML frontmatter (name, description, allowed-tools) + markdown body
- Marketplace registry mirrors each plugin's version and description — must stay in sync

## Naming Conventions
- Plugin names: kebab-case (e.g., `skills-improver`, `project-context`)
- Skill names: kebab-case in frontmatter, directory names match
- Plugin directories: `<name>-plugin/` for standalone plugins, or just `<name>/` (e.g., `project-context/`)

## Learnings
- Plugin cache can become stale/corrupted when version in cached path doesn't match version in file content
- Marketplace version must match source plugin.json version — mismatches cause loading errors
- Description length matters — keep under ~200 chars for clarity; long descriptions don't improve discoverability
- Keywords beyond ~12 provide diminishing returns

## Anti-Patterns
- Referencing non-existent directories in plugin.json (e.g., `"agents": "./agents"` when dir doesn't exist)
- Version bumps in source without updating marketplace.json

---
*Last updated: 2026-03-15*
