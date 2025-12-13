# Skill Improver Plugin

Automatically analyze conversation history and improve your Claude Code skills and plugins based on user feedback and real usage patterns.

## Overview

The Skill Improver Plugin provides a complete workflow for iteratively enhancing your Claude Code skills and plugins. It analyzes conversations to identify improvement opportunities, proposes specific changes with clear rationale, and implements approved improvements systematically.

## Features

### 🔍 Conversation Analysis
- Automatically identifies skills and plugins mentioned or used in conversations
- Extracts user feedback (positive and negative)
- Detects errors, pain points, and frustrations
- Identifies feature requests and enhancement suggestions
- Analyzes usage patterns vs. intended behavior

### 📝 Smart Improvement Proposals
- Proposes specific, actionable changes with detailed rationale
- Shows before/after comparisons for critical changes
- Categorizes improvements by type (description, content, scripts, metadata)
- Prioritizes changes by impact and urgency

### ✅ Safe Implementation
- **Always requests user approval** before making changes
- Validates all modifications using built-in validation scripts
- Tests scripts after modification
- Maintains consistent formatting and style
- Provides detailed summaries of changes made

### 🛠️ Comprehensive Improvement Types

**For Skills:**
- Update skill descriptions for better discoverability
- Enhance skill content with examples and documentation
- Fix errors in skill scripts
- Reorganize skill structure for clarity
- Add troubleshooting guides

**For Plugins:**
- Update plugin.json metadata and keywords
- Enhance command files and descriptions
- Improve README documentation
- Fix validation errors
- Update version numbers appropriately

## Installation

1. Download or clone this plugin
2. Place it in your Claude Code plugins directory
3. Reload Claude Code to activate the plugin

## Components

### Commands

#### `/improve-skills`
Analyzes conversation history to improve existing Claude Code skills.

**When to use:**
- After using a skill that had issues or limitations
- When a skill didn't trigger as expected
- To add examples based on actual usage
- After receiving feedback on a skill's effectiveness

**Example:**
```
/improve-skills
```

#### `/improve-plugin`
Analyzes conversation history to improve existing Claude Code plugins.

**When to use:**
- When a plugin didn't work as expected
- To improve plugin discoverability
- When plugin commands need better examples
- After receiving feedback on a plugin

**Example:**
```
/improve-plugin
```

### Skills

#### skill-improver
The core skill that powers the improvement workflow. Automatically invoked by the commands above.

**Capabilities:**
- Conversation history analysis
- Feedback extraction and categorization
- Improvement proposal generation
- Systematic change implementation
- Validation and testing

### Scripts

#### analyze_conversation.py
Automated script that extracts improvement opportunities from conversation text.

**Usage:**
```bash
python scripts/analyze_conversation.py < conversation.txt
```

**Output:**
- List of skills/plugins mentioned
- Categorized insights (feedback, errors, feature requests)
- Prioritized improvement suggestions

#### apply_improvements.py
Applies approved improvements to skill/plugin files from a JSON specification.

**Usage:**
```bash
python scripts/apply_improvements.py <skill-path> <improvements.json>
```

## Usage Workflow

### Basic Workflow

1. **Use a skill or plugin** in your conversation
2. **Notice opportunities for improvement** (errors, missing features, unclear docs)
3. **Run the command:**
   - `/improve-skills` for skills
   - `/improve-plugin` for plugins
4. **Review the proposal** that Claude presents
5. **Approve or modify** the proposed changes
6. **Changes are implemented** automatically
7. **Receive a summary** of what was changed

### Example Session

```
User: I tried to use the data-analyzer skill but it didn't trigger when I said
      "help me with this spreadsheet"

User: /improve-skills

Claude: I'll analyze the conversation to identify skill improvement opportunities...

I found that the data-analyzer skill should have triggered but didn't. Based on
the conversation, I propose the following improvements:

## Proposed Improvements for data-analyzer

### Rationale
The skill description mentions "data files" but doesn't explicitly include
"spreadsheet" as a trigger keyword. Users commonly refer to CSV/Excel files
as spreadsheets.

### Changes

#### 1. .claude/skills/data-analyzer/SKILL.md
**Change**: Update description to include spreadsheet terminology
**Reason**: Improves trigger coverage for common user phrases
**Before**:
description: Analyzes data files with pandas for analysis and visualization.

**After**:
description: Analyzes data files, spreadsheets, CSV, and Excel files with pandas
for analysis and visualization. Use when users request help with spreadsheets,
data analysis, or ask to "analyze data", "process spreadsheet", or similar tasks.

Do you approve these changes? Reply with:
- "yes" or "approve" to proceed
- "no" or "reject" to cancel
- "modify" to discuss adjustments

User: yes

Claude: ✅ Successfully improved data-analyzer

Changes made:
1. SKILL.md: Updated description with broader trigger keywords

The skill is now updated and ready to use.
```

## Improvement Patterns

The plugin includes comprehensive reference documentation with patterns for:

### Description Improvements
- Broadening trigger coverage with synonyms
- Adding context clues for better targeting
- Specifying supported file types explicitly

### Content Enhancements
- Adding concrete examples from real usage
- Including error troubleshooting sections
- Creating decision trees for complex workflows

### Script Fixes
- Adding input validation with clear errors
- Implementing progress feedback for long operations
- Making scripts more configurable

### Metadata Updates
- Adding missing keywords for discoverability
- Improving descriptions for clarity
- Incrementing versions appropriately

### Structural Reorganization
- Splitting long SKILL.md files into references
- Organizing by domain or framework
- Adding quick reference sections

See `skills/skill-improver/references/improvement-patterns.md` for detailed examples.

## Best Practices

1. **Run improvement commands after active usage** - Fresh context about what worked or didn't
2. **Be specific in feedback** - Mention what was confusing, missing, or didn't work
3. **Review proposals carefully** - Ensure changes match your intent
4. **Commit changes separately** - Makes it easy to rollback if needed
5. **Test after improvements** - Try using the improved skill/plugin to verify changes
6. **Iterate** - Run improvement commands multiple times as you learn more

## Configuration

No configuration required! The plugin works out of the box.

Optional: You can customize the improvement patterns by editing:
- `skills/skill-improver/references/improvement-patterns.md`

## Technical Details

### Requirements
- Claude Code (latest version)
- Python 3.7+ (for analysis scripts)
- PyYAML (for skill validation)

### File Structure
```
skill-improver-plugin/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── commands/
│   ├── improve-skills.md     # Skill improvement command
│   └── improve-plugin.md     # Plugin improvement command
├── skills/
│   └── skill-improver/
│       ├── SKILL.md          # Main skill instructions
│       ├── scripts/
│       │   ├── analyze_conversation.py
│       │   └── apply_improvements.py
│       └── references/
│           └── improvement-patterns.md
├── README.md                 # This file
└── LICENSE                   # MIT License
```

## Contributing

Improvements and feedback welcome! If you encounter issues or have suggestions:

1. Use the `/improve-plugin` command to improve this very plugin!
2. Submit issues or PRs to the repository
3. Share your improvement patterns with the community

## License

MIT License - see LICENSE file for details

## Support

For questions, issues, or feedback:
- Create an issue in the GitHub repository
- Use `/improve-plugin` to suggest improvements to this plugin

## Changelog

### v1.0.0 (2025-12-13)
- Initial release
- Conversation analysis with feedback extraction
- Skill and plugin improvement workflows
- Automated improvement application
- Comprehensive improvement pattern library
- `/improve-skills` and `/improve-plugin` commands

## Examples

### Example 1: Improving Trigger Keywords

**Scenario:** Skill doesn't trigger when users use alternative phrasing

**Before:**
```yaml
description: Processes Excel files with pandas
```

**After improvement:**
```yaml
description: Processes Excel, CSV, and spreadsheet files (.xlsx, .xls, .csv) with
pandas. Use when users say "analyze spreadsheet", "process data file", "open Excel",
or similar data analysis requests.
```

### Example 2: Adding Error Handling Documentation

**Scenario:** Users encounter common errors without guidance

**Before:** No troubleshooting section

**After improvement:** Added comprehensive troubleshooting section with:
- Common error messages
- Root causes
- Step-by-step solutions
- Examples

### Example 3: Improving Plugin Discoverability

**Scenario:** Plugin hard to find in searches

**Before:**
```json
{
  "keywords": ["code", "review"]
}
```

**After improvement:**
```json
{
  "keywords": ["code", "review", "linting", "quality", "analysis",
               "best-practices", "javascript", "typescript", "python"]
}
```

## Related Plugins

- **skill-creator** - Create new skills from scratch
- **plugin-creator** - Create new plugins with proper structure

## Acknowledgments

Built with the Claude Agent SDK and designed to work seamlessly with Claude Code's skill and plugin systems.
