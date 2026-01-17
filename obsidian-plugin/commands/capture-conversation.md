---
name: capture-conversation
description: Capture the current Claude Code conversation to Obsidian vault as structured notes
---

# Capture Conversation to Obsidian

Invoke the `obsidian-capture` skill to capture this conversation.

## Workflow

1. **Analyze** the current conversation for topics, decisions, and code changes
2. **Generate** a structured capture note with proper frontmatter
3. **Search** the vault for related notes
4. **Ask for confirmation** before updating any existing notes
5. **Create** the capture note and apply approved updates

## Quick Mode

For rapid capture without full analysis, add `--quick`:
- Creates minimal note with date, type, and files touched
- Tags with `#to-process` for later review
- Skips related note search

## Options

- Full capture (default): Complete analysis with related note integration
- Quick capture: Minimal note for later processing
- Custom title: Override auto-generated title
