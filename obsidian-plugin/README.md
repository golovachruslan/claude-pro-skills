# Obsidian Plugin for Claude Code

Comprehensive Obsidian note management with PARA method, Maps of Content, and formatting tools.

## Overview

This plugin helps you create and organize notes in Obsidian vaults using proper Markdown formatting, Obsidian-specific syntax (wikilinks, embeds, callouts), and knowledge management best practices.

## Features

- **Smart Note Creation**: Interactive note creation with templates for different note types (projects, areas, resources, MOCs, daily notes)
- **PARA Method Support**: Built-in support for Projects, Areas, Resources, and Archives organization
- **Maps of Content**: Easily create and manage MOCs to organize knowledge
- **Document Formatting**: Clean up imported documents with automated formatting scripts
- **Daily Note Processing**: Extract permanent notes from daily notes and maintain your vault
- **Best Practices**: Guidance on linking strategies, frontmatter, tags, and vault organization

## Installation

### From Marketplace

```bash
/plugin install obsidian@claude-pro-skills
```

### Local Development

```bash
cd /path/to/obsidian-plugin
cc --plugin-dir .
```

## Configuration

Create `.claude/obsidian.local.md` in your project:

```yaml
---
vault-path: ~/Documents/Obsidian/MyVault
default-organization: PARA
templates-path: Templates
attachments-path: Attachments
---

# Obsidian Plugin Settings

Additional notes about your Obsidian configuration...
```

### Settings

- **vault-path** (required): Absolute path to your Obsidian vault
- **default-organization** (optional): Organization system (PARA, Zettelkasten, custom)
- **templates-path** (optional): Relative path to templates directory (default: Templates)
- **attachments-path** (optional): Relative path for media files (default: Attachments)

## Commands

### `/obsidian:create-note`

Create a new note with proper structure and frontmatter.

**Usage**:
```bash
/obsidian:create-note                    # Interactive mode
/obsidian:create-note "Project Name"     # Quick project note
/obsidian:create-note "Topic" area       # Create area note
```

**Note types**: project, area, resource, moc, daily

### `/obsidian:create-moc`

Create a Map of Content to organize related notes.

**Usage**:
```bash
/obsidian:create-moc                     # Interactive mode
/obsidian:create-moc "Development"       # Create Development MOC
```

Auto-discovers related notes in your vault and suggests links.

### `/obsidian:format-document`

Format and clean up Obsidian documents (removes extra whitespace, fixes tables, cleans Mermaid diagrams).

**Usage**:
```bash
/obsidian:format-document                # Format current file
/obsidian:format-document path/to/file.md
```

### `/obsidian:organize-note`

Analyze and organize any Obsidian note - extract content, create links, and improve structure.

**Usage**:
```bash
/obsidian:organize-note                  # Organize current note
/obsidian:organize-note "path/to/note.md"
/obsidian:organize-note "2025-12-25.md"  # Works with daily notes too
```

## Skill

The plugin includes an **Obsidian Note Management** skill that automatically activates when you:

- Ask to create Obsidian notes
- Mention PARA method, MOCs, or daily notes
- Request help with wikilinks, embeds, or callouts
- Work with Obsidian-specific features

The skill provides comprehensive guidance on:

- Obsidian Markdown syntax (wikilinks, embeds, callouts, frontmatter)
- PARA method and other organization systems
- Maps of Content creation and management
- Linking strategies and vault organization
- Tags, frontmatter, and metadata best practices

## Examples

### Create a Project Note

```bash
/obsidian:create-note "Website Redesign" project
```

Creates:
```markdown
---
tags: [project, active]
date: 2025-12-25
status: in-progress
type: project
---

# Website Redesign

## Objective


## Milestones
- [ ]

## Notes


## Resources

```

### Create a Development MOC

```bash
/obsidian:create-moc "Development"
```

Scans vault for development-related notes and creates organized MOC with links.

### Format Imported Document

```bash
/obsidian:format-document "Imported Notes.md"
```

Cleans up formatting, fixes tables, removes extra whitespace.

## Formatting Scripts

The plugin includes utility scripts for document cleanup:

- **format-obsidian-doc.sh**: Complete formatting pipeline
- **clean-mermaid.awk**: Remove blank lines from Mermaid diagrams
- **fix-tables.py**: Clean up table formatting

These run automatically with `/obsidian:format-document`.

## Best Practices

### Linking Strategy
- Create bidirectional links between related notes
- Use descriptive aliases for context
- Link liberally to strengthen knowledge graph

### Frontmatter
- Add frontmatter to all notes for consistency
- Use standard field names across vault
- Update status and dates regularly

### Organization
- One idea per note (atomic notes)
- Use headings to structure longer notes
- Create MOCs for major topics
- Process daily notes regularly

## Troubleshooting

### "Vault path not configured"

Create `.claude/obsidian.local.md` with your vault path:

```yaml
---
vault-path: /absolute/path/to/vault
---
```

### Commands not appearing

Ensure plugin is enabled:

```bash
/plugin list
/plugin enable obsidian
```

### Formatting scripts not working

Check that scripts have execute permissions:

```bash
chmod +x obsidian-plugin/skills/obsidian/scripts/*.sh
```

## Contributing

Contributions welcome! Please:

1. Follow existing code patterns
2. Test commands thoroughly
3. Update documentation
4. Add examples for new features

## License

MIT License - See LICENSE file for details

## Support

- Issues: https://github.com/golovachruslan/claude-pro-skills/issues
- Documentation: https://github.com/golovachruslan/claude-pro-skills

## Changelog

### 1.0.0 (2025-12-25)

- Initial release
- Four commands for note management:
  - `/obsidian:create-note` - Create notes with proper structure and frontmatter
  - `/obsidian:create-moc` - Create Maps of Content to organize notes
  - `/obsidian:format-document` - Clean up and format Obsidian documents
  - `/obsidian:organize-note` - Analyze and organize any note (including daily notes)
- Comprehensive Obsidian Note Management skill
- PARA method support
- Knowledge management best practices
- Document formatting utilities (Mermaid, tables, whitespace)
