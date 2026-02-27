---
name: Obsidian Note Management
description: This skill should be used when the user asks to "create an Obsidian note", "make a new note", "add a note to vault", "organize notes", "create a MOC", "create daily note", "use PARA method", "add wikilinks", "create callouts", "add frontmatter", or mentions Obsidian-specific features like embeds, tags, or vault organization.
version: 0.2.0
---

# Obsidian Note Management

Guidance for creating and organizing notes in Obsidian vaults using proper Markdown formatting, Obsidian-specific syntax, and knowledge management best practices.

## Plugin Configuration

Supports configuration via `.claude/obsidian.local.md`:

```yaml
---
vault-path: ~/Documents/Obsidian/MyVault
default-organization: PARA
templates-path: Templates
attachments-path: Attachments
---
```

## Core Principles

- **Build connections** - Create links between related notes to strengthen the knowledge graph
- **Preserve link formats** - Maintain existing conventions (wikilinks vs standard Markdown)
- **Use tags strategically** - Apply sparingly and consistently
- **Prefer links over folders** - Organize through links and MOCs rather than deep hierarchies
- **Check for duplicates** - Search for existing notes before creating new ones

## Note Creation Workflow

1. Clarify purpose and location
2. Add YAML frontmatter (tags, date, status, type)
3. Structure with headings
4. Link to related notes with `[[Note Name]]`
5. Follow vault organization
6. Apply proper formatting
7. Highlight key info with callouts

## Essential Obsidian Features

### Internal Links (Wikilinks)

- Basic: `[[Note Name]]`
- With alias: `[[Note Name|Display Text]]`
- To heading: `[[Note Name#Heading]]`
- To block: `[[Note Name^blockid]]`

### Embeds

- Note: `![[Note Name]]`
- Section: `![[Note Name#Heading]]`
- Image: `![[image.png]]` or `![[image.png|300]]`

### Callouts

```markdown
> [!NOTE]
> Important information here.
```

Types: NOTE, TIP, IMPORTANT, WARNING, CAUTION, INFO, TODO, SUCCESS, QUESTION, FAILURE, DANGER, BUG, EXAMPLE, QUOTE. Collapse with `-`/`+`.

### YAML Frontmatter

```yaml
---
tags: [tag1, tag2]
date: 2025-12-07
status: draft|in-progress|complete|archived
type: note|project|area|resource|moc
aliases: [Alternative Name]
---
```

## Key Reminders

- Always use `.md` extension
- Preserve existing wikilink format: `[[Note Name]]` not `[Note Name](note-name.md)`
- Place files in appropriate directories based on vault organization
- One idea per note (atomic notes)

## References

- **Organization systems, workflows, templates, best practices**: See `references/organization-and-workflows.md` — PARA method, MOCs, daily notes, project/MOC/daily templates, linking and tagging strategies
- **Syntax reference**: See `references/syntax-reference.md` — Complete Obsidian Markdown syntax
- **Formatting scripts**: `scripts/format-obsidian-doc.sh`, `scripts/clean-mermaid.awk`, `scripts/fix-tables.py`
