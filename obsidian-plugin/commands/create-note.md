---
name: obsidian:create-note
description: Create a new Obsidian note with proper structure, frontmatter, and organization
argument-hint: "[note-name] [type:project|area|resource|moc|daily]"
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
---

# Create Obsidian Note

Create a new note in the Obsidian vault with proper structure, YAML frontmatter, and organization following best practices.

## Arguments

- **note-name** (optional): Name of the note to create
- **type** (optional): Type of note - `project`, `area`, `resource`, `moc`, or `daily`

If arguments are not provided, the command will run interactively.

## Workflow

### 1. Load Vault Configuration

First, check for vault configuration in `.claude/obsidian.local.md`:

- If vault-path is configured, use it
- If not configured, ask user for vault path using AskUserQuestion
- Store the vault path for this session

### 2. Gather Note Information

If not provided via arguments, ask user:

**Question 1: Note Type**
- Use AskUserQuestion with options:
  - "Project - Short-term effort with specific goal and deadline"
  - "Area - Long-term responsibility requiring ongoing attention"
  - "Resource - Topic of interest, reference material, or learning"
  - "MOC - Map of Content to organize related notes"
  - "Daily - Daily note for capturing fleeting thoughts"

**Question 2: Note Name** (if not provided as argument)
- Ask for descriptive note name
- Validate it's not empty
- Check for existing note with same name (use Grep to search vault)

### 3. Determine Note Location

Based on vault organization and note type:

- **PARA method**: Projects/, Areas/, Resources/, or Archives/
- **Flat structure**: Root of vault
- **Custom**: Ask user or use configured default

Check vault structure (use Glob to list directories) and follow existing organization.

### 4. Create Note Content

Generate note content based on type:

**Project Note Template**:
```markdown
---
tags: [project, active]
date: YYYY-MM-DD
status: in-progress
type: project
due: YYYY-MM-DD
---

# {Note Name}

## Objective
Clear statement of project goal.

## Milestones
- [ ] Milestone 1
- [ ] Milestone 2

## Notes
- [[Related Note]]

## Resources


## Log
### YYYY-MM-DD
Initial planning and setup.
```

**Area Note Template**:
```markdown
---
tags: [area]
date: YYYY-MM-DD
status: active
type: area
---

# {Note Name}

## Purpose
Why this area matters and what it encompasses.

## Standards
Key principles and quality standards for this area.

## Current Projects
- [[Project 1]]

## Resources
- [[Resource 1]]

## Review
### YYYY-MM-DD
Regular review notes.
```

**Resource Note Template**:
```markdown
---
tags: [resource]
date: YYYY-MM-DD
type: resource
source:
---

# {Note Name}

## Overview
Brief description of the resource.

## Key Points
-

## Related Notes
- [[Related Topic]]

## References
```

**MOC Template**:
```markdown
---
tags: [moc]
type: resource
---

# {Note Name} MOC

Map of content linking to all notes about this topic.

## Core Concepts
- [[Concept 1]]

## Subtopics
- [[Subtopic 1]]

## Projects
- [[Related Project]]

## Resources
- [[Reference Material]]
```

**Daily Note Template**:
```markdown
---
date: YYYY-MM-DD
tags: [daily]
---

# Daily Note - YYYY-MM-DD

## Tasks
- [ ]

## Meetings


## Ideas


## Notes
```

### 5. Write Note File

- Construct full file path: `{vault-path}/{directory}/{note-name}.md`
- Use Write tool to create the file
- Confirm to user with file location

### 6. Suggest Next Steps

Recommend:
- Links to create or add
- Related notes to connect
- MOC to update
- Tags to consider

## Examples

### Interactive Mode
```
/obsidian:create-note
> What type of note? [Project]
> Note name? "Website Redesign"
> Created: ~/Vault/Projects/Website Redesign.md
```

### Quick Project
```
/obsidian:create-note "Q4 Planning" project
> Created: ~/Vault/Projects/Q4 Planning.md
```

### Resource Note
```
/obsidian:create-note "API Design Patterns" resource
> Created: ~/Vault/Resources/API Design Patterns.md
```

## Error Handling

- **No vault configured**: Prompt user to create `.claude/obsidian.local.md` with vault-path
- **Note already exists**: Ask if user wants to overwrite or create with different name
- **Invalid directory**: Create directory if following PARA, otherwise ask user
- **Invalid type**: Show valid options and ask again

## Tips

- Always check for existing notes with similar names
- Suggest linking to related notes after creation
- Maintain consistent frontmatter across vault
- Follow existing organizational patterns
- Use current date in YYYY-MM-DD format
