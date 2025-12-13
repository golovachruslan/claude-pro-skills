---
name: skills-improver
description: Analyzes conversation history to improve existing Claude Code skills and plugins based on user feedback. Use this skill when users mention issues with skills/plugins, request improvements to existing skills/plugins, or explicitly ask to improve/update skills or plugins based on the current conversation. Triggers include "improve skill", "improve plugin", "update skill based on feedback", "fix this skill", or similar improvement requests.
---

# Skills Improver

## Overview

Automatically analyzes conversation history to identify opportunities for improving existing Claude Code skills and plugins. This skill examines feedback, usage patterns, and explicit improvement requests from the conversation, then proposes specific updates to enhance skill/plugin effectiveness.

## When to Use This Skill

Use this skill when:
- User explicitly requests to improve a skill or plugin (e.g., "improve the skill we just used")
- User mentions issues, limitations, or desired enhancements for a skill/plugin
- User asks to update a skill/plugin based on conversation feedback
- User says "make this skill better" or similar improvement requests

## Improvement Workflow

### Step 1: Analyze Conversation History

Review the conversation to identify:
1. **Skills/Plugins Used**: Which skills or plugins were invoked during the conversation
2. **User Feedback**: Explicit feedback about what worked or didn't work
3. **Pain Points**: Issues, errors, or frustrations encountered
4. **Feature Requests**: Desired capabilities or enhancements mentioned
5. **Usage Patterns**: How the skill/plugin was actually used vs. intended use

**Analysis checklist:**
- [ ] Identify all skills/plugins mentioned or used
- [ ] Extract explicit feedback (positive and negative)
- [ ] Note any error messages or failures
- [ ] Identify requested features or capabilities
- [ ] Determine if skill description matches actual usage

### Step 2: Determine Improvement Type

Classify the improvement into categories:

**A. Skills Improvement**
- Update SKILL.md frontmatter (name, description, allowed-tools)
- Enhance skill body content (instructions, examples, workflows)
- Add/update bundled resources (scripts, references, assets)
- Fix errors in existing scripts
- Improve clarity or organization

**B. Plugin Improvement**
- Update plugin.json metadata
- Enhance command files
- Improve agent configurations
- Update documentation (README.md)
- Fix validation errors

### Step 3: Propose Specific Changes

Before making any changes, create a detailed proposal listing:

1. **Target**: Which skill/plugin will be modified
2. **Rationale**: Why these changes are needed (reference specific conversation points)
3. **Changes**: Specific modifications to files
   - List each file to be modified
   - Describe what will change
   - Show before/after snippets for critical changes

**Proposal format:**
```
## Proposed Improvements for [skill-name/plugin-name]

### Rationale
[Based on conversation feedback, explain why improvements are needed]

### Changes

#### 1. [File Path]
**Change**: [Description]
**Reason**: [Why this helps]
**Before**:
```
[current content snippet]
```
**After**:
```
[proposed content snippet]
```

#### 2. [Next File]
...
```

### Step 4: Request User Approval

Present the proposal and explicitly ask for permission:

```
I've analyzed the conversation and identified improvements for [skill/plugin name].
Here are the proposed changes:

[Show proposal]

Do you approve these changes? Reply with:
- "yes" or "approve" to proceed
- "no" or "reject" to cancel
- "modify" to discuss adjustments
```

**Wait for explicit approval before proceeding.**

### Step 5: Implement Improvements

After approval:

1. **Read existing files**: Use Read tool to get current content
2. **Apply changes**: Use Edit tool for modifications, Write for new files
3. **Validate**: Run validation scripts if applicable
4. **Test**: Verify syntax and structure
5. **Report**: Summarize what was changed

**Implementation checklist:**
- [ ] Read all files to be modified
- [ ] Apply edits with exact old_string/new_string matches
- [ ] Create any new files needed
- [ ] Run quick_validate.py for skills if available
- [ ] Test scripts if modified (run them)
- [ ] Document what changed

### Step 6: Provide Summary

After implementation, provide:

```
✅ Successfully improved [skill-name/plugin-name]

Changes made:
1. [File]: [What changed]
2. [File]: [What changed]
...

The skill/plugin is now updated and ready to use.
Next steps:
- Test the improved skill/plugin
- Provide additional feedback if needed
- Consider packaging the skill if it's ready for distribution
```

## Handling Different Improvement Types

### Improving Skill Descriptions

If the skill description doesn't match actual usage:

1. Review how the skill was actually used in conversation
2. Check if trigger keywords match user requests
3. Update description to include:
   - Clear statement of what the skill does
   - Specific "when to use" scenarios
   - File types or contexts that should trigger it

**Example update:**
```yaml
# Before:
description: Helps with data analysis

# After:
description: Analyzes CSV and Excel data files with pandas. Use when users request data analysis, statistics, visualization, or data cleaning on tabular data files (.csv, .xlsx, .xls).
```

### Improving Skill Content

If skill instructions were unclear or incomplete:

1. Add missing steps from how the task was actually completed
2. Include concrete examples from the conversation
3. Add error handling guidance if errors occurred
4. Reorganize sections for better clarity

### Fixing Skill Scripts

If scripts had errors or needed modifications:

1. Read the script to understand current implementation
2. Apply fixes based on errors encountered
3. Test the script by running it
4. Update any documentation referencing the script

### Improving Plugin Metadata

If plugin.json needs updates:

1. Update version number (increment appropriately)
2. Add missing keywords from how users found/used it
3. Improve description clarity
4. Update repository or license if needed

## Common Improvement Patterns

### Pattern 1: Adding Missing Triggers

**Scenario**: User requested the skill but used different keywords than expected.

**Action**: Update description to include alternative trigger phrases.

```yaml
# Add to description:
description: "... Use when users say 'analyze this data', 'process this CSV', 'generate statistics', or similar data analysis requests."
```

### Pattern 2: Adding Examples

**Scenario**: User was unsure how to use the skill.

**Action**: Add concrete examples from the conversation to SKILL.md.

```markdown
## Examples

### Example 1: [Based on actual usage]
User request: "[actual request from conversation]"
Output: [what was produced]
```

### Pattern 3: Fixing Tool Limitations

**Scenario**: Skill needed additional tools to complete tasks.

**Action**: Update allowed-tools in frontmatter.

```yaml
# Before:
allowed-tools:
- Read
- Write

# After:
allowed-tools:
- Read
- Write
- Bash
- Grep
```

### Pattern 4: Splitting Large Skills

**Scenario**: SKILL.md is too long or covers too many domains.

**Action**: Move detailed content to references/ files.

```markdown
## Advanced Topics

For detailed information on specific areas:
- **Data visualization**: See [references/visualization.md](references/visualization.md)
- **API integration**: See [references/api.md](references/api.md)
```

## Best Practices

1. **Be Conservative**: Only change what's needed based on feedback
2. **Preserve Working Code**: Don't refactor scripts that work correctly
3. **Maintain Consistency**: Keep formatting and style consistent with existing content
4. **Test Changes**: Validate that improvements don't break existing functionality
5. **Document Rationale**: Clearly explain why each change is made
6. **Version Control**: User should commit changes separately for easy rollback

## Scripts

This skill includes helper scripts:

### analyze_conversation.py

Analyzes conversation context to extract feedback and improvement opportunities.

**Usage**:
```bash
python scripts/analyze_conversation.py
```

The script will:
- Parse conversation history (passed as input)
- Identify skills/plugins mentioned
- Extract feedback and issues
- Generate improvement suggestions

### apply_improvements.py

Applies approved improvements to skill/plugin files.

**Usage**:
```bash
python scripts/apply_improvements.py <skill-path> <improvements.json>
```

Where improvements.json contains the approved changes.

## References

See [references/improvement-patterns.md](references/improvement-patterns.md) for detailed examples of common improvement patterns and their implementations.
