# Handling Different Improvement Types

## Improving Skill Descriptions

If the skill description doesn't match actual usage:

1. Review how the skill was actually used in conversation
2. Check if trigger keywords match user requests
3. Update description to include clear statement, "when to use" scenarios, file types/contexts

**Example:**
```yaml
# Before:
description: Helps with data analysis

# After:
description: Analyzes CSV and Excel data files with pandas. Use when users request data analysis, statistics, visualization, or data cleaning on tabular data files (.csv, .xlsx, .xls).
```

## Improving Skill Content

If skill instructions were unclear or incomplete:

1. Add missing steps from how the task was actually completed
2. Include concrete examples from the conversation
3. Add error handling guidance if errors occurred
4. Reorganize sections for better clarity

## Fixing Skill Scripts

If scripts had errors or needed modifications:

1. Read the script to understand current implementation
2. Apply fixes based on errors encountered
3. Test the script by running it
4. Update any documentation referencing the script

## Improving Plugin Metadata

If plugin.json needs updates:

1. Update version number (increment appropriately)
2. Add missing keywords from how users found/used it
3. Improve description clarity
4. Update repository or license if needed

## Common Improvement Patterns

### Pattern 1: Adding Missing Triggers

**Scenario**: User requested the skill but used different keywords than expected.
**Action**: Update description to include alternative trigger phrases.

### Pattern 2: Adding Examples

**Scenario**: User was unsure how to use the skill.
**Action**: Add concrete examples from the conversation to SKILL.md.

### Pattern 3: Fixing Tool Limitations

**Scenario**: Skill needed additional tools to complete tasks.
**Action**: Update allowed-tools in frontmatter.

### Pattern 4: Splitting Large Skills

**Scenario**: SKILL.md is too long or covers too many domains.
**Action**: Move detailed content to references/ files.

## Best Practices

1. **Be Conservative**: Only change what's needed based on feedback
2. **Preserve Working Code**: Don't refactor scripts that work correctly
3. **Maintain Consistency**: Keep formatting and style consistent
4. **Test Changes**: Validate that improvements don't break functionality
5. **Document Rationale**: Clearly explain why each change is made
6. **Version Control**: User should commit changes separately for easy rollback
