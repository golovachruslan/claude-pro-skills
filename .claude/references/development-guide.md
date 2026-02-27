# Development Guide

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
