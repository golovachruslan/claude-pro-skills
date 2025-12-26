---
name: organize-note
description: Analyze and organize any Obsidian note - extract content to permanent notes, create links, and improve vault structure
argument-hint: "[file-path]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Organize Obsidian Note

Analyze any Obsidian note and help organize its content by extracting valuable information into permanent notes, creating proper links, improving structure, and maintaining vault organization.

## Arguments

- **file-path** (optional): Path to the note to organize. If not provided, will use current file from context or prompt user.

## Workflow

### 1. Load Vault Configuration

Check for vault configuration in `.claude/obsidian.local.md`:

- Load vault-path
- Check organization system (PARA, Zettelkasten, custom)
- Identify note structure conventions

### 2. Locate and Read Note

Find the note to organize:

**If file-path provided**:
- Validate path exists
- Ensure it's a .md file in the vault
- Read the file content

**If no file-path**:
- Check for current file in context
- If not available, ask user to specify note
- Use Grep/Glob to help find notes

### 3. Analyze Note Content

Read and categorize the note's content:

**Identify note type** (from frontmatter or content):
- Daily note (fleeting thoughts, mixed content)
- Project note (goals, milestones, progress)
- Area note (ongoing responsibilities)
- Resource note (reference material)
- MOC (map of content)
- Mixed/unorganized

**Content analysis**:
```
Note Analysis: {filename}

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

### 4. Identify Organizational Opportunities

Analyze what could be improved:

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
- Formatting issues

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

### 5. Interactive Organization

Use AskUserQuestion to guide organization:

**Question 1: What to focus on?**
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

### 6. Extract Content (if requested)

For each item to extract:

**Create Permanent Notes**:
```markdown
---
tags: [extracted-topic, from-note]
date: 2025-12-25
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

### 7. Improve Links

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

### 8. Fix Structure

**Frontmatter Improvements**:
```yaml
# Current frontmatter
---
tags: [dev]
---

# Suggested improvements
---
tags: [development, architecture, resource]
date: 2025-12-25
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

### 9. Clean Up Content

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

**Format for Consistency**:
- Apply Obsidian formatting standards
- Clean up whitespace
- Fix broken links
- Update dates

### 10. Summary and Recommendations

Present what was accomplished:

```
Organization Complete!

Changes Applied:
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
- Review extracted notes for further development
- Consider creating MOC for this topic area
- Schedule weekly note organization
- Link to [[Your Weekly Review]] workflow
```

## Examples

### Organize Current Note
```
/obsidian:organize-note
> Analyzing current note...
> Found 3 extraction opportunities
> Extract all? [Yes]
> ✓ Complete!
```

### Organize Specific Note
```
/obsidian:organize-note "Projects/Website Redesign.md"
> Note type: Project
> Suggestions: Add milestones to frontmatter, link to Resources
> Apply changes? [Yes]
```

### Daily Note Organization
```
/obsidian:organize-note "2025-12-25.md"
> Daily note detected
> Extract 2 ideas to permanent notes? [Yes]
> Link 3 meetings to project notes? [Yes]
> Archive completed tasks? [Yes]
```

### Cleanup Old Note
```
/obsidian:organize-note "Old Notes/Legacy Project.md"
> Note is 6 months old
> Suggestions: Archive or update status
> Extract still-relevant content? [Yes]
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

## Advanced Features

### Batch Organization

Process multiple notes:
```
Organize notes:
1. Current note only
2. All notes in current directory
3. All daily notes this week
4. All notes tagged #needs-organization
5. Custom selection
```

### Pattern Detection

Identify organizational patterns:
- Notes that are too long (should be split)
- Notes with too few links (need more connections)
- Notes without frontmatter
- Orphaned notes (no incoming links)
- Hub notes (highly connected - consider MOC)

### Smart Suggestions

Context-aware recommendations:
- **Daily notes**: Extract to permanent, archive old
- **Project notes**: Update status, add milestones
- **Resource notes**: Improve tags, link to MOCs
- **MOCs**: Add new related notes, organize sections

## Error Handling

- **Note not found**: Help find note or offer to create
- **No vault configured**: Prompt for vault path
- **Invalid note structure**: Offer to fix/restructure
- **Broken links**: Identify and suggest fixes
- **Circular references**: Warn and suggest cleanup

## Tips

- Organize notes regularly (weekly recommended)
- Extract ideas while they're fresh
- Create bidirectional links
- Maintain consistent frontmatter
- Use MOCs to organize extracted content
- Don't over-organize - some mess is creative
- Archive rather than delete old content
- Review extracted notes for further development
- Consider note size - split if too large (>2000 words)
- Build connections through links, not folders

## Related Commands

- `/obsidian:create-note` - Create new notes from extractions
- `/obsidian:create-moc` - Organize extracted notes with MOCs
- `/obsidian:format-document` - Clean up formatting before organizing
