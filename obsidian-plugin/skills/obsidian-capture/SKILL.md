---
name: obsidian-capture
description: Capture Claude Code conversations to Obsidian vault. Use when user says "capture this conversation", "save chat to obsidian", "log this session", "export conversation", "save to vault", "capture insights", or wants to preserve Claude Code discussion as notes. Supports finding and updating related existing notes.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Claude Code Conversation Capture for Obsidian

This skill captures Claude Code conversations and saves them as structured Obsidian notes, with optional integration into existing vault notes.

## Configuration

Uses `.claude/obsidian.local.md` configuration:

```yaml
---
vault-path: ~/Documents/Obsidian/MyVault  # Path to Obsidian vault
captures-path: Captures/Claude           # Where to save captures
link-captures: true                      # Auto-link to related notes
---
```

## Capture Workflow

### Step 1: Analyze Conversation

Before capturing, analyze the current conversation to extract:

1. **Main Topics** - Primary subjects discussed
2. **Key Decisions** - Important decisions or conclusions reached
3. **Code Changes** - Files modified, features implemented, bugs fixed
4. **Insights** - Learnings, tips, or patterns discovered
5. **Action Items** - Follow-up tasks or TODOs identified

### Step 2: Generate Capture Note

Create a structured note with this template:

```markdown
---
date: {{date}}
type: claude-capture
topics: [{{topics}}]
status: captured
session-type: {{type}}
related: []
---

# Claude Session: {{title}}

## Summary
{{2-3 sentence summary of what was accomplished}}

## Topics Discussed
{{bulleted list of main topics}}

## Key Decisions
{{important decisions made during session}}

## Code Changes
{{list of files modified with brief description}}
- `path/to/file.ts` - Description of change

## Insights & Learnings
{{patterns, tips, or knowledge gained}}

## Action Items
- [ ] {{follow-up task 1}}
- [ ] {{follow-up task 2}}

## Conversation Highlights
> {{notable quotes or exchanges}}

## Related Notes
{{wikilinks to related vault notes}}
```

### Step 3: Find Related Notes

Search the vault for potentially related notes:

1. **By Topic Match** - Notes with matching tags or topics in frontmatter
2. **By Title Similarity** - Notes with similar titles or aliases
3. **By Content Match** - Notes mentioning same concepts, files, or projects
4. **By Project** - Notes in the same project folder or linked to same MOC

Use Glob and Grep to search vault:
```bash
# Find notes with matching tags
grep -r "tags:.*{{topic}}" {{vault-path}}

# Find notes mentioning files we worked on
grep -r "{{filename}}" {{vault-path}}
```

### Step 4: Propose Related Note Updates

For each related note found, propose updates:

**Always ask user confirmation before updating any note.**

Present updates like this:

```
Found 3 related notes that could be updated:

1. [[Project X Documentation]]
   - Add link to this capture in "Related Sessions" section
   - Add new insight about {{topic}}

2. [[Development Log]]
   - Append today's session summary

3. [[Feature Y Notes]]
   - Update status from "in-progress" to "complete"
   - Add implementation details discovered

Would you like me to update these notes? [Yes to all / Select which / No]
```

## Update Patterns

### Adding Session Reference

Add to a "Related Sessions" or "Development Log" section:

```markdown
## Related Sessions
- [[Claude Session - 2025-01-17 - Feature Implementation]] - Implemented X, fixed Y
```

### Updating Project Status

When a project or feature was completed:

```markdown
status: complete  # was: in-progress
completed: 2025-01-17
```

### Adding Insights

Append to existing insights section:

```markdown
## Insights
- Previous insight
- {{new insight from session}}  <!-- Added from [[Claude Session - 2025-01-17]] -->
```

### Linking Bidirectionally

In the capture note, add:
```markdown
## Related Notes
- [[Project X Documentation]] - Main project docs
- [[Feature Y Notes]] - Feature we worked on
```

In the related note, add:
```markdown
## Claude Sessions
- [[Claude Session - 2025-01-17 - Title]]
```

## Session Type Detection

Classify the session type based on conversation content:

| Type | Indicators |
|------|-----------|
| `bug-fix` | Error messages, debugging, "fix", "broken", "issue" |
| `feature` | "implement", "add", "create", "new feature" |
| `refactor` | "refactor", "improve", "clean up", "reorganize" |
| `exploration` | Questions, research, "how does", "what is" |
| `review` | "review", "check", "audit", code review discussion |
| `documentation` | "document", "readme", "explain", docstrings |
| `learning` | Explanations, tutorials, learning new concepts |

## File Naming Convention

Use this pattern for capture notes:

```
Claude Session - {{YYYY-MM-DD}} - {{Brief Title}}.md
```

Examples:
- `Claude Session - 2025-01-17 - API Authentication Fix.md`
- `Claude Session - 2025-01-17 - React Component Refactor.md`

## Quick Capture Mode

For rapid capture without full analysis:

1. Create minimal note with:
   - Date and session type
   - One-line summary
   - List of files touched
   - Link to process later

2. Tag with `#to-process` for later review

```yaml
---
date: 2025-01-17
type: claude-capture
status: quick-capture
tags: [to-process]
---

# Quick Capture - {{brief description}}

Files touched:
- `file1.ts`
- `file2.ts`

Summary: {{one line}}

> [!TODO] Process this capture
> Review and expand this quick capture into full session notes.
```

## Vault Organization, Integration & Best Practices

For vault structure, MOC templates, Dataview queries, daily notes integration, error handling, and best practices, see `references/vault-organization.md`.
