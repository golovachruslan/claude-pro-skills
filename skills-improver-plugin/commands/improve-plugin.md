---
name: skills-improver:improve-plugin
description: Analyze conversation history and improve existing plugins based on user feedback
---

# Improve Plugin Command

Invoke the skill-improver skill to analyze the current conversation and improve existing Claude Code plugins based on feedback and usage patterns.

## Instructions

1. **Activate the skill-improver skill** by invoking it through the Skill tool
2. **Focus on plugin improvements**:
   - Analyze conversation for plugin mentions and usage
   - Identify issues with plugin.json metadata
   - Check command files for improvements
   - Review documentation quality
   - Propose updates to keywords and descriptions

## What This Command Does

This command helps you improve Claude Code plugins based on actual usage patterns. It:
- Analyzes how plugins were mentioned or used in conversation
- Identifies metadata improvements (plugin.json)
- Proposes command file enhancements
- Suggests documentation updates
- Gets approval before making changes

## When to Use

Use this command when:
- A plugin didn't work as expected
- You want to improve plugin discoverability
- Plugin commands need better examples
- README or documentation is unclear
- You received feedback on a plugin's effectiveness
- Plugin keywords don't match how users search for it

## Expected Flow

1. You run `/skills-improver:improve-plugin`
2. Claude invokes the skill-improver skill
3. Claude analyzes the conversation for plugin usage and feedback
4. Claude presents proposed improvements and asks for approval
5. Upon approval, Claude implements the changes
6. Claude reports what was changed

## Example Usage

```
User: /improve-plugin

Claude: I'll analyze the conversation to identify plugin improvement opportunities...

[Analysis happens]

I found that the code-reviewer plugin was mentioned in this conversation. Based on
the feedback, I propose the following improvements:

## Proposed Improvements for code-reviewer

### Rationale
You mentioned the plugin should also handle TypeScript files, but the current
description only mentions JavaScript. The keywords also don't include TypeScript-
related terms.

### Changes

#### 1. .claude-plugin/plugin.json
**Change**: Add TypeScript to description and keywords
**Reason**: Improves discoverability for TypeScript users
**Before**:
{
  "description": "Reviews JavaScript code for best practices",
  "keywords": ["javascript", "review", "linting"]
}

**After**:
{
  "description": "Reviews JavaScript and TypeScript code for best practices",
  "keywords": ["javascript", "typescript", "review", "linting", "ts", "js"]
}

#### 2. README.md
**Change**: Add TypeScript examples
**Reason**: Shows TypeScript support clearly
[Details of changes...]

Do you approve these changes? Reply with:
- "yes" or "approve" to proceed
- "no" or "reject" to cancel
- "modify" to discuss adjustments
```

## Plugin-Specific Improvements

The skill-improver handles several types of plugin improvements:

### Metadata (plugin.json)
- Update version numbers
- Add missing keywords
- Improve description clarity
- Update repository links

### Commands
- Enhance command descriptions
- Add examples to command files
- Update model specifications
- Improve command documentation

### Documentation
- Update README.md with better examples
- Add troubleshooting sections
- Include usage screenshots or demos
- Document new features

### Structure
- Validate file organization
- Check for missing required files
- Ensure proper licensing
- Validate JSON syntax

## Notes

- This command only proposes changes - you must approve them
- Plugin version numbers are incremented appropriately
- Changes follow plugin best practices
- You can commit changes separately for easy rollback
- Validation runs automatically after changes
