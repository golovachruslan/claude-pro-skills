---
name: improve-skills
description: Analyze conversation history and improve existing skills based on user feedback
---

# Improve Skills Command

Invoke the skills-improver skill to analyze the current conversation and improve existing Claude Code skills based on feedback and usage patterns.

## Instructions

1. **Activate the skills-improver skill** by invoking it through the Skill tool
2. **Follow the skills-improver workflow**:
   - Analyze conversation history for skills mentioned or used
   - Identify feedback, issues, and improvement opportunities
   - Propose specific changes with rationale
   - Request user approval before implementing
   - Apply approved improvements
   - Validate and test changes

## What This Command Does

This command helps you iteratively improve your Claude Code skills based on real usage. It:
- Extracts insights from conversation history
- Identifies which skills were used and how
- Proposes improvements to skill descriptions, content, or scripts
- Gets your approval before making changes
- Implements improvements systematically

## When to Use

Use this command when:
- You've been using a skill and noticed issues or limitations
- A skill didn't trigger when it should have
- You want to add examples based on actual usage
- You received feedback on a skill's effectiveness
- You want to update skill documentation

## Expected Flow

1. You run `/improve-skills`
2. Claude invokes the skills-improver skill
3. Claude analyzes the conversation for skill usage and feedback
4. Claude presents proposed improvements and asks for approval
5. Upon approval, Claude implements the changes
6. Claude reports what was changed

## Example Usage

```
User: /improve-skills

Claude: I'll analyze the conversation to identify skill improvement opportunities...

[Analysis happens]

I found that the data-analyzer skill was used in this conversation. Based on the
conversation, I propose the following improvements:

## Proposed Improvements for data-analyzer

### Rationale
The skill triggered successfully but the description doesn't mention CSV files
explicitly, which is what you used. Adding CSV to the description will improve
discoverability.

### Changes

#### 1. .claude/skills/data-analyzer/SKILL.md
**Change**: Update description to include CSV file type
**Reason**: Makes trigger keywords more explicit
**Before**:
description: Analyzes data files with pandas...

**After**:
description: Analyzes CSV, Excel, and data files with pandas...

Do you approve these changes? Reply with:
- "yes" or "approve" to proceed
- "no" or "reject" to cancel
- "modify" to discuss adjustments
```

## Notes

- This command only proposes changes - you must approve them
- Changes are applied using the Edit tool with proper validation
- Scripts are tested if modified
- You can commit changes separately for easy rollback
