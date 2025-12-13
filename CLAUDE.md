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
│   ├── improve-skills.md   # /improve-skills command
│   └── improve-plugin.md   # /improve-plugin command
└── skills/                 # Core skills available globally
    ├── skills-improver/    # Analyze and improve existing skills/plugins
    ├── skill-creator/      # Create new skills
    └── plugin-creator/     # Scaffold complete plugins

.claude-plugin/             # Marketplace configuration
└── marketplace.json        # Plugin registry

skills-improver-plugin/     # Distributable plugin example
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata
├── commands/               # Command wrappers
├── skills/                 # Plugin skills
└── README.md
```

### Key Architectural Principles

1. **Skills are self-contained**: Each skill in `.claude/skills/` includes:
   - `SKILL.md` - Main skill definition (frontmatter + instructions)
   - `scripts/` - Executable Python scripts for automation
   - `references/` - Detailed documentation loaded as-needed
   - `assets/` - Templates/output files (not loaded into context)

2. **Plugins are distributable packages**: Complete plugins in separate directories include `.claude-plugin/plugin.json` with marketplace metadata.

3. **Self-improving ecosystem**: Skills can enhance other skills through the skills-improver workflow.

## Core Skills

### skills-improver
**Purpose**: Analyzes conversation history to identify and apply improvements to skills/plugins.

**Workflow**: Analyze → Propose → Approve → Implement → Validate

**Key files**:
- `.claude/skills/skills-improver/scripts/analyze_conversation.py` - Pattern-based conversation analysis
- `.claude/skills/skills-improver/scripts/apply_improvements.py` - Applies approved changes
- `.claude/skills/skills-improver/references/improvement-patterns.md` - Detailed improvement examples

### skill-creator
**Purpose**: Guide for creating new skills with proper structure.

**Key files**:
- `.claude/skills/skill-creator/scripts/init_skill.py` - Initialize new skill
- `.claude/skills/skill-creator/scripts/package_skill.py` - Package skill for distribution
- `.claude/skills/skill-creator/scripts/quick_validate.py` - Validate SKILL.md structure

### plugin-creator
**Purpose**: Scaffolds complete Claude Code plugins ready for marketplace distribution.

## Common Development Commands

### Validation

Validate a SKILL.md file structure:
```bash
python .claude/skills/skill-creator/scripts/quick_validate.py <skill-path>/SKILL.md
```

This checks:
- YAML frontmatter syntax
- Required fields (`name`, `description`)
- Naming conventions (hyphen-case)
- Field lengths and formats

### Conversation Analysis

Analyze conversation for improvement opportunities:
```bash
python .claude/skills/skills-improver/scripts/analyze_conversation.py < conversation.txt
```

Returns JSON with:
- Identified skills/plugins mentioned
- User feedback and feature requests
- Errors encountered
- Improvement suggestions

### Marketplace Operations

Add this marketplace to Claude Code:
```bash
/plugin marketplace add golovachruslan/claude-pro-skills
```

Install a plugin from marketplace:
```bash
/plugin install skills-improver@claude-pro-skills
```

### Improvement Workflow

Use slash commands to improve skills/plugins based on conversation history:
```bash
/improve-skills   # Improve skills
/improve-plugin   # Improve plugins
```

## SKILL.md Structure

All skills must follow this structure:

```markdown
---
name: skill-name-in-hyphen-case
description: Clear description with trigger conditions (1-1024 chars)
allowed-tools:  # Optional
  - Read
  - Write
license: MIT  # Optional
---

# Skill Instructions

[Markdown content with workflows, examples, edge cases]
```

**Important constraints**:
- **name**: hyphen-case, 1-64 characters
- **description**: Should specify WHEN to use the skill ("Use when users want to...")
- **Body**: Only loaded AFTER skill triggers - keep concise to save context
- **References**: Move detailed docs to `references/` subdirectory
- **Scripts**: Move executable code to `scripts/` for reliability

## Plugin Structure

Plugins require `.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "User-friendly description of what plugin does",
  "author": "Author Name",
  "repository": "https://github.com/user/repo",
  "keywords": ["keyword1", "keyword2"],
  "categories": ["productivity", "development"],
  "components": {
    "commands": ["commands/command-name.md"],
    "skills": ["skills/skill-name"]
  }
}
```

**Version guidelines**:
- Patch (1.0.0 → 1.0.1): Bug fixes, small improvements
- Minor (1.0.0 → 1.1.0): New features, enhancements
- Major (1.0.0 → 2.0.0): Breaking changes, rewrites

## CI/CD & Automation

### GitHub Workflows

**`.github/workflows/claude.yml`** - Interactive Claude Code execution:
- Triggers on issue comments, PR reviews, issue creation
- Requires "@claude" mention in comments
- Executes custom prompts via `anthropics/claude-code-action@v1`

**`.github/workflows/claude-code-review.yml`** - Automated PR reviews:
- Triggers on PR open/synchronize
- Evaluates: code quality, bugs, performance, security, test coverage
- Posts review comments via gh CLI
- References CLAUDE.md for style guidance

## Working Efficiently in This Repository

### Creating new skills
Invoke the `skill-creator` skill - it will guide through initialization, structure, and validation.

### Creating new plugins
Invoke the `plugin-creator` skill for marketplace-ready plugin scaffolding.

### Improving existing skills/plugins
Use `/improve-skills` or `/improve-plugin` commands to analyze conversation history and propose improvements.

### Validation workflow
1. Create/modify skill using skill-creator
2. Run `quick_validate.py` to verify SKILL.md structure
3. Test skill invocation in Claude Code
4. Use `/improve-skills` to iterate based on usage feedback
5. Commit changes - GitHub Actions will auto-review PRs

### Understanding improvement patterns
Read `.claude/skills/skills-improver/references/improvement-patterns.md` for detailed examples of:
- Description improvements (trigger coverage, context clues)
- Content enhancements (examples, error handling, decision trees)
- Script fixes (validation, progress feedback, configurability)
- Metadata updates (keywords, versioning)
- Structural reorganization (splitting files, domain organization)

### Marketplace distribution
Ensure plugin.json includes:
- Clear, user-friendly description (not technical jargon)
- Comprehensive keywords for discoverability
- Proper version number (semantic versioning)
- Categories that match plugin purpose
- Complete component references

## Important Notes

- **No traditional build/test pipeline**: This is a skills/plugins repository, not a compiled application
- **Validation is via Python scripts**: Use the scripts in skill-creator for validation
- **Self-documenting**: Skills contain their own documentation in SKILL.md files
- **Context-aware loading**: Only relevant references are loaded on-demand to save context
- **Improvement workflow always requires approval**: Changes are never applied without user consent
