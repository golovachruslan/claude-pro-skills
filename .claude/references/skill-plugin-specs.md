# Skill & Plugin Specifications

Detailed specs for SKILL.md and plugin.json structures. Referenced from CLAUDE.md.

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

## Marketplace Distribution Checklist

Ensure plugin.json includes:
- Clear, user-friendly description (not technical jargon)
- Comprehensive keywords for discoverability
- Proper version number (semantic versioning)
- Categories that match plugin purpose
- Complete component references
