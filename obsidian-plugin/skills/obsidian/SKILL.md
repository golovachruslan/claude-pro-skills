---
name: Obsidian Note Management
description: This skill should be used when the user asks to "create an Obsidian note", "make a new note", "add a note to vault", "organize notes", "create a MOC", "create daily note", "use PARA method", "add wikilinks", "create callouts", "add frontmatter", or mentions Obsidian-specific features like embeds, tags, or vault organization.
version: 0.2.0
---

# Obsidian Note Management

This skill provides guidance for creating and organizing notes in Obsidian vaults using proper Markdown formatting, Obsidian-specific syntax, and knowledge management best practices.

## Plugin Configuration

This plugin supports configuration via `.claude/obsidian.local.md`:

```yaml
---
vault-path: ~/Documents/Obsidian/MyVault  # Path to Obsidian vault
default-organization: PARA                # Organization system
templates-path: Templates                 # Templates directory
attachments-path: Attachments            # Media files directory
---
```

When using plugin commands, the `vault-path` setting determines where notes are created. If not configured, commands will prompt for the vault location.

## Core Principles

Follow these principles when working with Obsidian vaults:

- **Build connections** - Create links between related notes to strengthen the knowledge graph
- **Preserve link formats** - Maintain existing conventions (wikilinks vs standard Markdown)
- **Use tags strategically** - Apply tags sparingly and maintain consistency across the vault
- **Prefer links over folders** - Organize primarily through links and Maps of Content (MOCs) rather than deep folder hierarchies
- **Check for duplicates** - Search for existing related notes before creating new ones to avoid redundancy

## Note Creation Workflow

Follow these steps when creating notes:

1. **Clarify purpose and location** - Ask questions if the note's purpose or location is unclear
2. **Add YAML frontmatter** - Include relevant metadata (tags, date, status, type)
3. **Structure with headings** - Use appropriate heading levels for organization
4. **Link to related notes** - Connect to existing notes using wikilinks `[[Note Name]]`
5. **Follow vault organization** - Maintain consistency with existing structure
6. **Apply proper formatting** - Use Obsidian-specific Markdown syntax
7. **Highlight key information** - Use callouts for important content

## Essential Obsidian Features

### Internal Links (Wikilinks)

Obsidian uses wiki-style links for internal connections:

- Basic link: `[[Note Name]]`
- Link with alias: `[[Note Name|Display Text]]`
- Link to heading: `[[Note Name#Heading]]`
- Link to block: `[[Note Name^blockid]]`

### Embeds

Embed content from other notes or files:

- Embed note: `![[Note Name]]`
- Embed section: `![[Note Name#Heading]]`
- Embed image: `![[image.png]]` or `![[image.png|300]]` for sizing

### Callouts

Use callouts to highlight important information:

```markdown
> [!NOTE]
> Important information here.

> [!WARNING]
> Caution or warning.

> [!TIP]
> Helpful tip.
```

Available types: NOTE, TIP, IMPORTANT, WARNING, CAUTION, INFO, TODO, SUCCESS, QUESTION, FAILURE, DANGER, BUG, EXAMPLE, QUOTE

Collapse callouts using `-` (collapsed) or `+` (expanded):

```markdown
> [!NOTE]- Collapsed by default
> Content here.
```

### YAML Frontmatter

Add metadata at the top of notes using YAML:

```yaml
---
tags: [tag1, tag2]
date: 2025-12-07
status: draft|in-progress|complete|archived
type: note|project|area|resource|moc
aliases: [Alternative Name]
---
```

Common fields:
- **tags** - Categorization and filtering
- **date** - Creation or reference date
- **status** - Progress tracking
- **type** - Note classification (PARA method)
- **aliases** - Alternative names for linking

## Organization Systems

### PARA Method

Organize notes into four top-level categories:

1. **Projects** - Short-term efforts with specific goals and deadlines
2. **Areas** - Long-term responsibilities requiring ongoing attention
3. **Resources** - Topics of interest, reference materials, learning
4. **Archives** - Inactive items from Projects, Areas, or Resources

**Implementation:**
- Set `type: project|area|resource|archive` in frontmatter
- Create MOCs for each category
- Move completed projects to Archives
- Review Areas regularly for relevance

### Maps of Content (MOCs)

MOCs serve as flexible, curated indexes that link to related topics:

**Create MOCs for:**
- Topic areas (e.g., "Development MOC", "Marketing MOC")
- Projects with multiple related notes
- Learning paths and courses
- Collections of resources

**MOC Structure:**
```markdown
# Topic MOC

## Overview
Brief description of the topic area.

## Core Concepts
- [[Concept 1]]
- [[Concept 2]]
- [[Concept 3]]

## Projects
- [[Active Project 1]]
- [[Active Project 2]]

## Resources
- [[Resource 1]]
- [[Resource 2]]

## Related MOCs
- [[Related MOC 1]]
- [[Related MOC 2]]
```

### Daily Notes

Use daily notes for:
- Capturing fleeting thoughts and ideas
- Meeting notes and daily logs
- Task management and to-dos
- Temporary landing page for information

**Refactor daily notes regularly:**
- Extract important content into permanent notes
- Link to related project or area notes
- Archive or delete once processed

## File Organization Best Practices

### Naming Conventions

Use clear, descriptive file names:
- **Good**: `Project Planning - Q4 Goals.md`, `Customer Segmentation Strategy.md`
- **Avoid**: `Untitled.md`, `Notes.md`, `temp.md`

### Folder Structure

Keep folder hierarchies shallow (2-3 levels max):

```
Vault/
├── Projects/
├── Areas/
├── Resources/
├── Archives/
├── Templates/
└── Attachments/
```

Rely on links and MOCs for navigation rather than deep nesting.

### Tags Strategy

Apply tags consistently:
- Use lowercase for consistency: `#meeting` not `#Meeting`
- Create tag hierarchy: `#project/active`, `#project/archived`
- Limit to 3-5 tags per note
- Document tag system in a "Tag Index" note

## Common Workflows

### Creating a Project Note

```yaml
---
tags: [project, active]
date: 2025-12-07
status: in-progress
type: project
due: 2025-12-31
---

# Project Name

## Objective
Clear statement of project goal.

## Milestones
- [ ] Milestone 1
- [ ] Milestone 2
- [ ] Milestone 3

## Notes
- [[Related Note 1]]
- [[Related Note 2]]

## Resources
- [[Resource 1]]
- External links

## Log
### 2025-12-07
Initial planning and setup.
```

### Creating a MOC

```yaml
---
tags: [moc]
type: resource
---

# Topic MOC

Map of content linking to all notes about this topic.

## Core Notes
- [[Central Concept]]
- [[Key Theory]]

## Subtopics
- [[Subtopic 1]]
- [[Subtopic 2]]

## Projects
- [[Related Project]]

## Resources
- [[Reference Material]]
```

### Creating from Daily Note

```yaml
---
date: 2025-12-07
tags: [daily]
---

# Daily Note - 2025-12-07

## Tasks
- [x] Completed task
- [ ] Pending task

## Meetings
### Team Standup
- Discussed [[Project X]]
- Action item: [[Follow-up Task]]

## Ideas
Random thought to explore later: [[Idea for Feature Y]]

## Notes
Quick reference to [[Important Concept]]
```

## Additional Resources

### Reference Files

For comprehensive syntax details, consult:
- **`references/syntax-reference.md`** - Complete Obsidian Markdown syntax guide including text styling, links, embeds, callouts, tables, diagrams, mathematical expressions, and advanced features

### Example Files

Working examples in `examples/`:
- **`examples/note-template.md`** - Basic note template demonstrating structure, frontmatter, headings, callouts, and wikilinks

Reference these when creating new notes or guiding users on proper note structure.

### Formatting Scripts

Utility scripts in `scripts/` for efficient document cleanup:

**Master Script:**
- **`scripts/format-obsidian-doc.sh <file.md>`** - Complete formatting pipeline (removes whitespace, cleans Mermaid diagrams, fixes tables)

**Individual Operations:**
- **`scripts/clean-mermaid.awk`** - Remove blank lines from Mermaid diagrams only
- **`scripts/fix-tables.py`** - Remove blank lines between table rows only

**Usage Example:**
```bash
# Format entire document
./scripts/format-obsidian-doc.sh "Projects/uCollect/uCollect BE.md"

# Or use individual scripts
awk -f scripts/clean-mermaid.awk input.md > output.md
python3 scripts/fix-tables.py document.md
```

Use these scripts when cleaning up imported documents, fixing formatting issues, or standardizing vault documentation.

## Tips and Best Practices

### Linking Strategy
- Create bidirectional links between related notes
- Use descriptive aliases when link text needs context
- Link liberally - more connections strengthen the graph
- Review unlinked mentions periodically

### Frontmatter Usage
- Add frontmatter to all notes for consistency
- Use standard field names across the vault
- Keep custom fields minimal and purposeful
- Update status and dates regularly

### Content Organization
- One idea per note (atomic notes)
- Use headings to structure longer notes
- Extract large sections into separate notes
- Link back to parent notes and MOCs

### Graph View Optimization
- Use tags to color-code note types
- Create hub notes (MOCs) for major topics
- Avoid orphaned notes (notes with no links)
- Regularly review and strengthen connections

### Search and Discovery
- Use aliases for common search terms
- Tag notes for easy filtering
- Create index notes for important topics
- Use dataview queries for dynamic lists (if plugin installed)

## Key Reminders

When working with Obsidian vaults:

- Always use `.md` extension for notes
- Preserve existing wikilink format: `[[Note Name]]` not `[Note Name](note-name.md)`
- Place files in appropriate directories based on vault organization
- Add YAML frontmatter for metadata
- Link to related notes to build knowledge graph
- Use callouts for highlighting important information
- Follow PARA or existing organizational system
- Check for existing notes before creating duplicates
