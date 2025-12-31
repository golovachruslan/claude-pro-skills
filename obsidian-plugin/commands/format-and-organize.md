---
name: obsidian:format-and-organize
description: Complete note processing - format document (clean whitespace, tables, Mermaid) then organize content (extract ideas, improve links, structure)
argument-hint: "[file-path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# Format and Organize Obsidian Note

Complete note processing workflow that combines document formatting with content organization. First cleans up technical formatting issues (whitespace, tables, Mermaid diagrams), then analyzes and organizes the content (extracts ideas, improves links, fixes structure).

## Arguments

- **file-path** (optional): Path to the note to process. If not provided, will use current file from context or prompt user.

## Workflow

### Phase 1: Document Formatting

#### 1.1 Determine Target File

**If file-path provided**:
- Validate the path exists
- Ensure it's a .md file
- Read the file content

**If no file-path**:
- Check if there's a current file in context
- If not, ask user to specify file path
- Use AskUserQuestion to get file path

#### 1.2 Analyze Formatting Issues

Identify technical formatting problems:

**Common Issues**:
- Extra blank lines between paragraphs
- Inconsistent whitespace in Mermaid diagrams
- Blank lines within table rows
- Trailing whitespace
- Inconsistent heading spacing
- Multiple consecutive blank lines

Present analysis:
```
Document Formatting Analysis: {filename}

Found issues:
- 15 extra blank lines
- 3 Mermaid diagrams with inconsistent formatting
- 2 tables with blank line issues
- Trailing whitespace on 8 lines

Total size: 1,234 lines
```

#### 1.3 Apply Formatting

Use the formatting scripts from the Obsidian skill:

**Master Script** (Recommended):
```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/format-obsidian-doc.sh "{file-path}"
```

This runs all formatters in sequence:
1. Removes trailing whitespace
2. Cleans Mermaid diagrams
3. Fixes table formatting
4. Reduces multiple blank lines to maximum of 2

**Alternative - Individual Scripts** (if master script fails):

**Clean Mermaid diagrams**:
```bash
awk -f ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/clean-mermaid.awk "{file-path}" > temp.md && mv temp.md "{file-path}"
```

**Fix tables**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/fix-tables.py "{file-path}"
```

#### 1.4 Formatting Results

```
Formatting complete!

Changes applied:
✓ Removed 15 blank lines
✓ Cleaned 3 Mermaid diagrams
✓ Fixed 2 tables
✓ Removed trailing whitespace

File size: 1,234 lines → 1,219 lines (15 lines removed)
```

### Phase 2: Content Organization

#### 2.1 Load Vault Configuration

Check for vault configuration in `.claude/obsidian.local.md`:
- Load vault-path
- Check organization system (PARA, Zettelkasten, custom)
- Identify note structure conventions

#### 2.2 Analyze Note Content

Read and categorize the formatted note:

**Identify note type** (from frontmatter or content):
- Daily note (fleeting thoughts, mixed content)
- Project note (goals, milestones, progress)
- Area note (ongoing responsibilities)
- Resource note (reference material)
- MOC (map of content)
- Mixed/unorganized

**Content analysis**:
```
Content Organization Analysis: {filename}

Type: {detected-type}
Created: {date}
Tags: {tags}
Links: {link-count}
Size: {word-count} words

Content breakdown:
✓ {count} ideas worth extracting
✓ {count} unlinked concepts
✓ {count} potential permanent notes
✓ {count} external references
✓ {count} actionable items
✓ {count} orphaned sections
```

#### 2.3 Identify Organizational Opportunities

**Extraction Opportunities**:
- Valuable ideas buried in mixed content
- Meeting notes that should be separate
- Reference material to extract
- Concepts that deserve their own notes

**Linking Opportunities**:
- Unlinked mentions of existing notes
- Concepts that should be wikilinks
- Missing backlinks
- MOC connections

**Structural Improvements**:
- Missing or inconsistent frontmatter
- Poor heading organization
- Untagged content
- Missing dates or metadata

**Cleanup Needs**:
- Completed tasks to archive
- Obsolete information
- Duplicate content

**Present opportunities**:
```
Organization Opportunities:

Extraction (3):
  1. "Event Sourcing Pattern" → Create new resource note
  2. "Team Meeting 12/20" → Extract to separate meeting note
  3. "API Documentation" → Move to Resources/

Linking (5):
  - Add [[Architecture MOC]] link
  - Link "microservices" → [[Microservices Architecture]]
  - Create backlink from [[Project X]]

Structure (2):
  - Add missing frontmatter fields (tags, type, date)
  - Reorganize sections with better headings

Cleanup (1):
  - Archive completed tasks from last month
```

#### 2.4 Interactive Organization

Use AskUserQuestion to guide organization:

**Question 1: What to improve?**
```
What would you like to improve?
1. Extract valuable content to permanent notes (Recommended)
2. Improve links and connections
3. Fix structure and frontmatter
4. Clean up and archive old content
5. All of the above
6. Custom selection
```

**Question 2: Extraction priority**
```
Found 3 items to extract. Process:
1. All items (Recommended)
2. Select individually
3. Skip extraction, just improve current note
```

#### 2.5 Extract Content (if requested)

For each item to extract:

**Create Permanent Notes**:
```markdown
---
tags: [extracted-topic, from-note]
date: 2025-12-31
source: [[{original-note-name}]]
type: resource
---

# {Extracted Topic}

## Context
Extracted from [[{original-note-name}]] on {date}.

## Content
{Extracted and expanded content}

## Related Notes
- [[Related 1]]
- [[Related 2]]

## Next Steps
- [ ] Develop further
- [ ] Connect to MOCs
```

**Update Source Note**:
Replace extracted content with link:
```markdown
## {Section}
See: [[Extracted Topic Note]] - Moved to permanent note
```

Or keep summary:
```markdown
## {Section}
Brief summary here. Details in [[Extracted Topic Note]].
```

#### 2.6 Improve Links

**Add Missing Wikilinks**:
- Scan content for mentions of existing notes
- Convert to wikilinks: `microservices` → `[[Microservices Architecture]]`
- Use Grep to verify target notes exist

**Create Backlinks**:
- Identify notes that should link here
- Suggest adding backlinks to related notes
- Update MOCs with this note

**Link to MOCs**:
```
This note relates to:
- [[Development MOC]]
- [[Architecture Patterns MOC]]

Add links to these MOCs? [Yes/No]
```

#### 2.7 Fix Structure

**Frontmatter Improvements**:
```yaml
# Current frontmatter
---
tags: [dev]
---

# Suggested improvements
---
tags: [development, architecture, resource]
date: 2025-12-31
type: resource
status: active
---
```

**Heading Organization**:
- Ensure logical heading hierarchy (H1 → H2 → H3)
- Add missing section headings
- Reorganize content into clear sections
- Use callouts for important information

**Apply PARA/Organization System**:
- Move note to correct directory if misplaced
- Update type in frontmatter
- Ensure naming follows conventions

#### 2.8 Clean Up Content

**Archive Completed Items**:
```markdown
## Tasks
~~- [x] Completed task from last month~~ [Archived]
- [ ] Current active task
```

**Remove Obsolete Content**:
- Old information no longer relevant
- Duplicate sections
- Temporary notes that were processed

### Phase 3: Final Summary

Present complete results:

```
Complete Processing Finished!

Phase 1 - Formatting:
✓ Removed 15 blank lines
✓ Cleaned 3 Mermaid diagrams
✓ Fixed 2 tables
✓ File size: 1,234 → 1,219 lines

Phase 2 - Organization:
✓ Extracted 3 permanent notes
✓ Added 5 wikilinks
✓ Updated frontmatter with proper tags
✓ Reorganized into 4 clear sections
✓ Archived 6 completed tasks
✓ Updated 2 MOCs with new links

New Notes Created:
  1. [[Event Sourcing Pattern]]
  2. [[Team Meeting 2025-12-20]]
  3. [[API Documentation Standards]]

Recommendations:
- Review extracted notes in Obsidian
- Verify all links work correctly
- Consider creating MOC for this topic area
- Schedule weekly note processing
```

## Examples

### Process Current Note
```
/obsidian:format-and-organize
> Phase 1: Formatting...
> ✓ Cleaned 12 formatting issues
> Phase 2: Organizing...
> Found 3 extraction opportunities
> Extract all? [Yes]
> ✓ Complete!
```

### Process Specific Note
```
/obsidian:format-and-organize "Projects/Website Redesign.md"
> Formatting: Website Redesign.md
> ✓ Cleaned 2 Mermaid diagrams
> Organizing: Project note detected
> Suggestions: Add milestones, link to Resources
> Apply changes? [Yes]
```

### Process Daily Note
```
/obsidian:format-and-organize "2025-12-31.md"
> Formatting complete (6 issues fixed)
> Daily note detected
> Extract 2 ideas to permanent notes? [Yes]
> Link 3 meetings to project notes? [Yes]
> Archive completed tasks? [Yes]
```

### Quick Format Only
```
/obsidian:format-and-organize "Quick Note.md"
> Formatting: 3 issues fixed
> No organization opportunities found
> Note is well-structured!
```

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

## Content Extraction Strategies

### Idea Development

**From fleeting → Permanent**:
- Expand single sentences into full notes
- Add context and background
- Connect to related concepts
- Create actionable next steps

### Meeting Notes

**Separate meeting content**:
- Extract to dedicated meeting note
- Include attendees, decisions, actions
- Link to related projects
- Create follow-up tasks

### Reference Material

**Extract to resources**:
- Move documentation to Resources/
- Create proper structure
- Add tags and categorization
- Link from relevant projects

### Project Updates

**Project log entries**:
- Extract progress to project notes
- Document decisions in project file
- Update project status
- Link related resources

## Advanced Options

### Workflow Customization

Ask user which phases to run:
```
Processing options:
1. Full process (Format + Organize) - Recommended
2. Format only
3. Organize only (skip formatting)
4. Format only if issues found, then organize
5. Custom workflow
```

### Batch Processing

Process multiple notes:
```
Process notes:
1. Current note only
2. All notes in current directory
3. All daily notes this week
4. All notes tagged #needs-processing
5. Custom selection
```

### Preview Mode

Show changes before applying:
```
Preview mode enabled

Formatting changes:
- Remove 15 blank lines
- Clean 3 Mermaid diagrams

Organization changes:
- Extract 3 notes
- Add 5 links
- Update frontmatter

Apply all changes? [Yes/No/Selective]
```

## Error Handling

- **File not found**: Prompt for correct path or list available .md files
- **Not a Markdown file**: Warn user and ask for confirmation
- **Script execution fails**: Fall back to manual formatting with Read/Edit tools
- **No vault configured**: Prompt for vault path in `.claude/obsidian.local.md`
- **Broken links**: Identify and suggest fixes
- **Permissions error**: Check file permissions and suggest fix

## Safety Features

1. **Pre-flight checks**: Verify file exists and is writable
2. **Backup option**: Offer backup before processing
3. **Phase separation**: Can stop after formatting if desired
4. **Verification**: Check processed file is valid
5. **Rollback**: Restore from backup if processing fails

## Tips

- Run on new notes after creation for best practices
- Use on daily notes before archiving
- Process imported documents from external sources
- Run weekly on active project notes
- Combine with version control for safety
- Review extracted notes for further development
- Check rendered output in Obsidian after processing
- Don't over-organize - some creative mess is okay
- Build connections through links, not folders
- Archive rather than delete old content

## Related Commands

- `/obsidian:create-note` - Create properly formatted and organized notes from start
- `/obsidian:create-moc` - Create MOCs to organize extracted content
- `/obsidian:format-document` - Format only (no organization)
- `/obsidian:organize-note` - Organize only (no formatting)

## Script Locations

Formatting scripts are located in:
```
${CLAUDE_PLUGIN_ROOT}/skills/obsidian/scripts/
├── format-obsidian-doc.sh    # Master formatting script
├── clean-mermaid.awk          # Mermaid diagram cleaner
├── fix-tables.py              # Table formatter
└── README.md                  # Script documentation
```

Use `${CLAUDE_PLUGIN_ROOT}` to reference scripts portably across installations.
