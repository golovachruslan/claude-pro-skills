---
name: obsidian:create-moc
description: Create a Map of Content (MOC) to organize related notes in your Obsidian vault
argument-hint: "[moc-name] [topic]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Create Map of Content (MOC)

Create a Map of Content (MOC) note to organize and link related notes in your Obsidian vault. MOCs serve as flexible, curated indexes that help navigate knowledge domains.

## Arguments

- **moc-name** (optional): Name of the MOC (e.g., "Development", "Marketing", "Python Learning")
- **topic** (optional): Topic or theme to organize notes around

If arguments are not provided, the command will run interactively.

## Workflow

### 1. Load Vault Configuration

Check for vault configuration in `.claude/obsidian.local.md`:

- If vault-path is configured, use it
- If not configured, ask user for vault path
- Store the vault path for this session

### 2. Gather MOC Information

If not provided via arguments:

**Question 1: MOC Name**
- Ask for descriptive MOC name
- Suggest format: "{Topic} MOC" or "{Area} Index"
- Validate it's not empty

**Question 2: MOC Purpose**
- Ask what topic/area this MOC will organize
- Examples: "All development-related notes", "Marketing campaigns and strategies", "Python programming concepts"

### 3. Discover Related Notes

Search the vault for notes related to the MOC topic:

**Search Strategy**:
1. Use Grep to search for keyword matches in note content and filenames
2. Look in relevant directories (Projects/, Areas/, Resources/)
3. Scan for tags that match the topic
4. Find notes with related wikilinks

**Categorize Discovered Notes**:
- Core concepts and foundational notes
- Project notes
- Resource and reference notes
- Related MOCs

Present discovered notes to user:
```
Found 15 related notes:
- [[Core Concept 1]]
- [[Core Concept 2]]
- [[Project: Implementation]]
...

Would you like to:
1. Include all (Recommended)
2. Let me select which to include
3. Skip auto-discovery
```

### 4. Structure the MOC

Organize discovered notes into logical sections:

**Standard MOC Structure**:
```markdown
---
tags: [moc]
type: resource
topic: {topic}
---

# {MOC Name} MOC

{Brief description of what this MOC organizes}

## Overview
{1-2 sentence summary of the topic area}

## Core Concepts
{Foundational notes and key ideas}
- [[Concept 1]]
- [[Concept 2]]

## Subtopics
{Specific areas within the broader topic}
- [[Subtopic 1]]
- [[Subtopic 2]]

## Projects
{Active and completed projects related to this topic}
- [[Project 1]]
- [[Project 2]]

## Resources
{Reference materials, guides, documentation}
- [[Resource 1]]
- [[Resource 2]]

## Related MOCs
{Links to other MOCs that connect to this topic}
- [[Related MOC 1]]

## Unorganized
{Temporary section for notes that don't fit elsewhere - review and reorganize}
-
```

### 5. Interactive Refinement

Offer user options:

**Customize Sections**:
- Add custom sections based on topic
- Remove unused sections
- Reorder sections

**Examples of custom sections**:
- For development: "Design Patterns", "Best Practices", "Tools & Libraries"
- For projects: "Planning", "Active", "Completed", "On Hold"
- For learning: "Beginner", "Intermediate", "Advanced", "Practice Projects"

**Question**:
```
The MOC has 4 sections (Core Concepts, Subtopics, Projects, Resources).
Would you like to:
1. Use standard sections (Recommended)
2. Customize sections
3. Add more sections
```

### 6. Write MOC File

Determine location:
- PARA method: Resources/ or root
- Custom: Ask user preference

Write the MOC:
```
Created MOC: ~/Vault/Resources/{MOC Name} MOC.md

Linked notes:
- 5 core concepts
- 3 subtopics
- 4 projects
- 3 resources
```

### 7. Update Related Notes

Suggest adding backlinks to the MOC:

```
Consider adding these links to related notes:
- Add "[[{MOC Name} MOC]]" to [[Core Concept 1]]
- Add "[[{MOC Name} MOC]]" to [[Project 1]]

Would you like me to add these backlinks? (yes/no)
```

If yes, use Edit tool to add backlinks to appropriate sections.

### 8. Suggest Next Steps

Recommend:
- Review and refine section organization
- Add descriptions for each linked note
- Create additional MOCs for subtopics
- Link to parent or related MOCs
- Update regularly as vault grows

## Examples

### Interactive Mode
```
/obsidian:create-moc
> MOC name? "Development"
> What topic? "Software development concepts and projects"
> Found 15 related notes. Include all? [Yes]
> Created: ~/Vault/Resources/Development MOC.md
```

### Quick MOC
```
/obsidian:create-moc "Python Learning"
> Searching for Python-related notes...
> Found 12 notes
> Created: ~/Vault/Resources/Python Learning MOC.md
```

### Topic-Specific
```
/obsidian:create-moc "Marketing Campaigns" "marketing strategy"
> Created: ~/Vault/Areas/Marketing Campaigns MOC.md
```

## Advanced Features

### Auto-Discovery Patterns

Search for notes using multiple criteria:

**Filename matching**:
- Notes containing topic keywords
- Notes in related directories

**Content matching**:
- Full-text search for topic mentions
- Tag-based discovery (#topic)

**Link analysis**:
- Notes that link to each other (clusters)
- Frequently referenced notes

### Smart Categorization

Automatically categorize discovered notes:

**By type** (using frontmatter):
- type: project → Projects section
- type: resource → Resources section
- tags: [concept] → Core Concepts section

**By recency**:
- Recent notes → highlight as new additions
- Old notes → might need review or archival

**By link density**:
- Highly linked → Core Concepts
- Few links → Unorganized section

## Error Handling

- **No vault configured**: Prompt to create `.claude/obsidian.local.md`
- **MOC already exists**: Ask to overwrite or append
- **No related notes found**: Create empty MOC template, suggest manual curation
- **Invalid search results**: Fall back to empty template

## Tips

- Use descriptive MOC names that indicate scope
- Start with broad MOCs, create specialized ones as vault grows
- Review and update MOCs regularly
- Link MOCs to each other for meta-organization
- Keep MOCs focused - split if they grow too large (>50 links)
- Add brief descriptions for linked notes
- Use MOCs as entry points for topic exploration
- Consider creating a "Home MOC" that links to all other MOCs

## Related Commands

- `/obsidian:create-note` - Create individual notes to link in MOC
- `/obsidian:organize-daily-notes` - Extract notes from daily notes to add to MOCs
