---
name: skills-improver
description: Analyzes conversation history to improve existing Claude Code skills and plugins based on user feedback. Use this skill when users mention issues with skills/plugins, request improvements to existing skills/plugins, or explicitly ask to improve/update skills or plugins based on the current conversation. Triggers include "improve skill", "improve plugin", "update skill based on feedback", "fix this skill", or similar improvement requests.
---

# Skills Improver

Analyzes conversation history to identify and apply improvements to existing Claude Code skills and plugins.

## Improvement Workflow

### Step 1: Analyze Conversation History

Review conversation to identify:
1. **Skills/Plugins Used**: Which were invoked
2. **User Feedback**: What worked or didn't
3. **Pain Points**: Issues, errors, frustrations
4. **Feature Requests**: Desired capabilities
5. **Usage Patterns**: Actual use vs. intended use

### Step 2: Determine Improvement Type

**Skills**: Update frontmatter, enhance body content, add/update resources, fix scripts, improve clarity.
**Plugins**: Update plugin.json, enhance commands, improve agent configs, fix validation.

### Step 3: Propose Specific Changes

Create a detailed proposal with:
- **Target**: Which skill/plugin
- **Rationale**: Why (reference specific conversation points)
- **Changes**: File-by-file modifications with before/after snippets

### Step 4: Request User Approval

Present proposal and wait for explicit approval before proceeding.

### Step 5: Implement Improvements

1. Read existing files
2. Apply changes with Edit/Write tools
3. Run validation scripts if applicable
4. Test modified scripts
5. Report what changed

### Step 6: Provide Summary

Report all changes made and suggest next steps (test, provide feedback, package).

## Scripts

### analyze_conversation.py
```bash
python scripts/analyze_conversation.py
```
Parses conversation history, identifies skills/plugins, extracts feedback, generates suggestions.

### apply_improvements.py
```bash
python scripts/apply_improvements.py <skill-path> <improvements.json>
```
Applies approved changes from JSON specification.

## References

- **Improvement type handling, patterns, best practices**: See `references/improvement-types.md`
- **Detailed improvement pattern examples**: See `references/improvement-patterns.md`
