# Obsidian Organization Systems & Workflows

## PARA Method

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

## Maps of Content (MOCs)

MOCs serve as flexible, curated indexes that link to related topics.

**Create MOCs for:** Topic areas, projects with multiple notes, learning paths, collections of resources.

**MOC Structure:**
```markdown
# Topic MOC

## Overview
Brief description of the topic area.

## Core Concepts
- [[Concept 1]]
- [[Concept 2]]

## Projects
- [[Active Project 1]]

## Resources
- [[Resource 1]]

## Related MOCs
- [[Related MOC 1]]
```

## Daily Notes

Use daily notes for: fleeting thoughts, meeting notes, task management, temporary information landing page.

**Refactor regularly:** Extract important content into permanent notes, link to related project/area notes, archive once processed.

## File Organization Best Practices

### Naming Conventions
- **Good**: `Project Planning - Q4 Goals.md`, `Customer Segmentation Strategy.md`
- **Avoid**: `Untitled.md`, `Notes.md`, `temp.md`

### Folder Structure
Keep hierarchies shallow (2-3 levels max):
```
Vault/
├── Projects/
├── Areas/
├── Resources/
├── Archives/
├── Templates/
└── Attachments/
```

### Tags Strategy
- Use lowercase: `#meeting` not `#Meeting`
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
```

Structure: Objective → Milestones (checkboxes) → Notes (wikilinks) → Resources → Log (dated entries).

### Creating a MOC

```yaml
---
tags: [moc]
type: resource
---
```

Structure: Overview → Core Notes → Subtopics → Projects → Resources.

### Creating from Daily Note

```yaml
---
date: 2025-12-07
tags: [daily]
---
```

Structure: Tasks (checkboxes) → Meetings (wikilinks to projects/actions) → Ideas → Notes.

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

### Content Organization
- One idea per note (atomic notes)
- Use headings to structure longer notes
- Extract large sections into separate notes
- Link back to parent notes and MOCs

### Graph View Optimization
- Use tags to color-code note types
- Create hub notes (MOCs) for major topics
- Avoid orphaned notes (notes with no links)

### Search and Discovery
- Use aliases for common search terms
- Tag notes for easy filtering
- Create index notes for important topics
- Use dataview queries for dynamic lists (if plugin installed)
