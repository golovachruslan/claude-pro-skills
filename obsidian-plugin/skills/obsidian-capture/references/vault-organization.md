# Vault Organization for Captures

## Recommended Structure

```
Vault/
├── Captures/
│   └── Claude/
│       ├── 2025-01/
│       │   └── Claude Session - 2025-01-17 - Title.md
│       └── Claude Sessions MOC.md
├── Projects/
│   └── Project X/
│       └── ... (link to captures)
└── ...
```

## Claude Sessions MOC

Maintain a Map of Content for sessions:

```markdown
---
type: moc
tags: [claude, sessions]
---

# Claude Sessions MOC

## Recent Sessions
- [[Claude Session - 2025-01-17 - Latest]]

## By Project
### Project X
- [[Session 1]]
- [[Session 2]]

## By Type
### Bug Fixes
- [[Bug fix session]]

### Features
- [[Feature session]]
```

## Daily Notes Integration

If using daily notes, add a section:

```markdown
## Claude Sessions
- [[Claude Session - 2025-01-17 - Title]] - Brief summary
```

## Dataview Queries

For vaults using Dataview plugin:

```dataview
TABLE session-type, topics
FROM "Captures/Claude"
WHERE type = "claude-capture"
SORT date DESC
LIMIT 10
```

## Error Handling

### Vault Not Found
If vault path is not configured or invalid:
- Prompt user for vault path
- Offer to save to current directory as fallback

### No Related Notes
If no related notes found:
- Create capture note standalone
- Suggest creating related notes for topics discussed

### Update Conflicts
If a related note has been modified:
- Show diff of proposed changes
- Let user choose to merge, skip, or manually edit

## Best Practices

1. **Capture promptly** - Details fade, capture while fresh
2. **Be selective** - Not every session needs capturing, focus on valuable ones
3. **Link liberally** - More connections strengthen the knowledge graph
4. **Review periodically** - Process quick captures, archive old sessions
5. **Confirm updates** - Always verify before modifying existing notes
