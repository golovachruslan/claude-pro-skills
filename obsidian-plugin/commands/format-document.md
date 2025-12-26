---
name: format-document
description: Format and clean up Obsidian documents (removes extra whitespace, fixes tables, cleans Mermaid diagrams)
argument-hint: "[file-path]"
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

# Format Obsidian Document

Clean up and format Obsidian Markdown documents using automated formatting scripts. Removes extra whitespace, fixes table formatting, cleans Mermaid diagrams, and applies Obsidian best practices.

## Arguments

- **file-path** (optional): Path to the Markdown file to format. If not provided, will attempt to use the current file from context.

## Workflow

### 1. Determine Target File

**If file-path provided**:
- Validate the path exists
- Ensure it's a .md file
- Read the file content

**If no file-path**:
- Check if there's a current file in context
- If not, ask user to specify file path
- Use AskUserQuestion to get file path

### 2. Analyze Document

Read the file and identify formatting issues:

**Common Issues to Check**:
- Extra blank lines between paragraphs
- Inconsistent whitespace in Mermaid diagrams
- Blank lines within table rows
- Trailing whitespace
- Inconsistent heading spacing
- Multiple consecutive blank lines

Present analysis to user:
```
Document analysis for: {filename}

Found issues:
- 15 extra blank lines
- 3 Mermaid diagrams with inconsistent formatting
- 2 tables with blank line issues
- Trailing whitespace on 8 lines

Total size: 1,234 lines
```

### 3. Backup Original (Optional)

Ask user if they want to create a backup:
```
Create backup before formatting?
1. Yes - Create {filename}.backup
2. No - Format in place (Recommended)
```

If yes, use Write to create backup file.

### 4. Apply Formatting

Use the formatting scripts from the Obsidian skill:

**Master Script** (Recommended):
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/format-obsidian-doc.sh "{file-path}"
```

This script runs all formatters in sequence:
1. Removes trailing whitespace
2. Cleans Mermaid diagrams
3. Fixes table formatting
4. Reduces multiple blank lines to maximum of 2

**Alternative - Individual Scripts**:

If master script fails, run individual operations:

**Clean Mermaid diagrams**:
```bash
awk -f ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/clean-mermaid.awk "{file-path}" > temp.md && mv temp.md "{file-path}"
```

**Fix tables**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/fix-tables.py "{file-path}"
```

### 5. Show Results

Read the formatted file and compare to original:

**Present changes**:
```
Formatting complete!

Changes applied:
✓ Removed 15 blank lines
✓ Cleaned 3 Mermaid diagrams
✓ Fixed 2 tables
✓ Removed trailing whitespace

File size: 1,234 lines → 1,219 lines (15 lines removed)
```

### 6. Verification

Verify formatting was successful:

**Check for**:
- File still exists and is readable
- Content structure preserved
- No data loss
- Obsidian-specific syntax intact

**Quality checks**:
```
Verification:
✓ File is valid Markdown
✓ Wikilinks preserved: [[Note]] format intact
✓ Frontmatter preserved
✓ Code blocks preserved
✓ All tables readable
```

If verification fails, restore from backup (if created) and report error.

### 7. Suggest Next Steps

Recommend:
- Review the changes in Obsidian
- Check that links still work
- Verify rendered output looks correct
- Consider running on related documents

## Formatting Rules

### Whitespace Removal

**Remove**:
- Trailing spaces at end of lines
- More than 2 consecutive blank lines
- Blank lines at start/end of file

**Preserve**:
- Single blank lines between sections
- Blank lines before/after code blocks
- Indentation in code blocks
- Blank lines in lists (if intentional)

### Mermaid Diagram Cleanup

**Clean**:
```mermaid
graph LR

A --> B

B --> C
```

**Becomes**:
```mermaid
graph LR
A --> B
B --> C
```

Removes unnecessary blank lines inside Mermaid blocks while preserving diagram structure.

### Table Formatting

**Fix**:
```markdown
| Column 1 | Column 2 |
|----------|----------|

| Row 1    | Data 1   |

| Row 2    | Data 2   |
```

**Becomes**:
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Row 1    | Data 1   |
| Row 2    | Data 2   |
```

Removes blank lines between table rows while preserving table structure.

## Examples

### Format Current File
```
/obsidian:format-document
> Formatting current file: Project Notes.md
> Removed 12 blank lines, fixed 1 table
> Complete!
```

### Format Specific File
```
/obsidian:format-document "Projects/Website Redesign.md"
> Formatting: Website Redesign.md
> Cleaned 2 Mermaid diagrams, removed trailing whitespace
> Complete!
```

### Batch Format (Advanced)
```
/obsidian:format-document
> Which file? "Resources/*.md"
> Found 15 files. Format all? [Yes]
> Formatting 15 files...
> Complete! Processed 15 files, cleaned 45 issues total.
```

## Error Handling

- **File not found**: Prompt for correct path or list available .md files
- **Not a Markdown file**: Warn user and ask for confirmation to proceed
- **Script execution fails**: Fall back to manual formatting with Read/Edit tools
- **Permissions error**: Check file permissions and suggest fix
- **Backup creation fails**: Warn user and ask if they want to proceed anyway

## Advanced Options

### Preview Changes

Show a preview before applying:
```
Preview mode:

Before (lines 45-50):
| Column 1 | Column 2 |
|----------|----------|

| Row 1    | Data 1   |

After:
| Column 1 | Column 2 |
|----------|----------|
| Row 1    | Data 1   |

Apply changes? [Yes/No]
```

### Selective Formatting

Ask user which formatters to apply:
```
Select formatting operations:
1. All (Recommended)
2. Whitespace only
3. Mermaid diagrams only
4. Tables only
5. Custom selection
```

### Format Options

Support additional options:
- `--backup`: Always create backup
- `--preview`: Show changes before applying
- `--tables-only`: Only fix tables
- `--mermaid-only`: Only clean Mermaid diagrams

## Script Locations

The formatting scripts are located in the Obsidian skill directory:

```
${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/
├── format-obsidian-doc.sh    # Master formatting script
├── clean-mermaid.awk          # Mermaid diagram cleaner
├── fix-tables.py              # Table formatter
└── README.md                  # Script documentation
```

Use `${CLAUDE_PLUGIN_ROOT}` to reference scripts portably across installations.

## Safety Features

1. **Pre-flight checks**: Verify file exists and is writable
2. **Backup option**: Create backup before formatting
3. **Verification**: Check formatted file is valid
4. **Rollback**: Restore from backup if formatting fails
5. **Dry-run mode**: Preview changes without applying

## Tips

- Run formatting after importing documents from other sources
- Use before committing notes to version control
- Format regularly to maintain clean, readable notes
- Check the formatted output in Obsidian to verify rendering
- Consider formatting entire directories for consistency
- Formatting is safe - it doesn't change content, only whitespace

## Related Commands

- `/obsidian:create-note` - Create properly formatted notes from the start
- `/obsidian:organize-daily-notes` - Clean up daily notes before archiving
