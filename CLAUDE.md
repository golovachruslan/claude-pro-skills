# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin marketplace** that serves two purposes:
1. A marketplace for distributing Claude Code plugins (via `.claude-plugin/marketplace.json`)
2. A collection of foundational skills for creating and improving skills/plugins

**Repository**: https://github.com/golovachruslan/claude-pro-skills

## Architecture

The repository uses a **skill-centric ecosystem** with clear separation:

```
.claude/                    # Global foundational skills
├── commands/               # Slash commands that invoke skills
├── skills/                 # Core skills (skills-improver, skill-creator, plugin-creator)
└── references/             # Shared reference docs (specs, CI/CD, dev guide)

.claude-plugin/             # Marketplace configuration
└── marketplace.json        # Plugin registry

[plugin-name]/              # Distributable plugins (each with .claude-plugin/plugin.json)
├── skills/                 # Plugin skills
└── commands/               # Command wrappers
```

### Key Architectural Principles

1. **Skills are self-contained**: Each skill includes `SKILL.md` (frontmatter + instructions), optional `scripts/`, `references/`, and `assets/`
2. **Plugins are distributable packages**: Include `.claude-plugin/plugin.json` with marketplace metadata
3. **Self-improving ecosystem**: Skills can enhance other skills through the skills-improver workflow
4. **Progressive disclosure**: Metadata always loaded → SKILL.md body on trigger → references on-demand

## Common Development Commands

Validate a SKILL.md file:
```bash
python .claude/skills/skill-creator/scripts/quick_validate.py <skill-path>/SKILL.md
```

Analyze conversation for improvements:
```bash
python .claude/skills/skills-improver/scripts/analyze_conversation.py < conversation.txt
```

Improve skills/plugins from conversation history:
```bash
/improve-skills   # Improve skills
/improve-plugin   # Improve plugins
```

## References

For detailed specs and guides, see:
- **Skill/Plugin specs**: `.claude/references/skill-plugin-specs.md` — SKILL.md structure, plugin.json format, versioning
- **CI/CD workflows**: `.claude/references/ci-cd.md` — GitHub Actions configuration
- **Development guide**: `.claude/references/development-guide.md` — Creating skills/plugins, validation, improvement patterns

## Important Notes

- **No traditional build/test pipeline**: This is a skills/plugins repository, not a compiled application
- **Validation is via Python scripts**: Use the scripts in skill-creator for validation
- **Context-aware loading**: Only relevant references are loaded on-demand to save context
- **Improvement workflow always requires approval**: Changes are never applied without user consent
