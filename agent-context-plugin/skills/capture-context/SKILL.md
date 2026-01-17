---
name: capture-context
description: Saves agent conversation context to .agent-context folder for sharing with other agents. Use when users want to save conversation summary, capture key learnings, export conversation context, create handoff document for another agent, or preserve important discussion points. Triggers include "save context", "capture conversation", "create handoff", "save learnings", "export context".
---

# Capture Context

Saves structured conversation context to `.agent-context/` folder for later use by other agents or for maintaining conversation history.

## Workflow

### Step 1: Request Context Name

Ask the user for a short descriptive name for this context file:

```
What name would you like for this context file? (Press Enter to auto-generate)
```

If user provides a name, use it. If not, generate a descriptive name based on the main topics discussed.

### Step 2: Analyze Conversation

Review the conversation to extract:

1. **Main Topic**: Primary subject of discussion
2. **Key Points**: Important decisions, findings, or conclusions (3-7 points)
3. **Learnings**: Insights gained during the conversation
4. **Technical Details**: Code snippets, file paths, configurations mentioned
5. **Action Items**: Pending tasks or next steps
6. **Context for Next Agent**: What another agent needs to know to continue

### Step 3: Generate Context File

Create a structured markdown file with the following format:

```markdown
# Context: [Topic Summary]

> Captured: [YYYY-MM-DD HH:MM]
> Session: [Brief description]

## Summary

[2-3 sentence overview of the conversation]

## Key Points

- [Point 1]
- [Point 2]
- [Point 3]
...

## Learnings

- [Learning 1]
- [Learning 2]
...

## Technical Details

### Files Modified/Referenced
- `path/to/file1` - [what was done]
- `path/to/file2` - [what was done]

### Code Snippets
[Include any important code discussed]

### Commands Used
[Include any important commands]

## Action Items

- [ ] [Pending task 1]
- [ ] [Pending task 2]
...

## Context for Next Agent

[What the next agent needs to know to continue this work effectively. Include any assumptions, constraints, or important background information.]
```

### Step 4: Save Context File

1. Create `.agent-context/` directory if it doesn't exist
2. Generate filename: `YYYY-MM-DD_[short-summary].md`
   - Date: Current date
   - Short summary: Kebab-case summary (max 50 chars)
   - Example: `2024-01-15_implement-user-auth.md`
3. Save the file using the script

### Step 5: Confirm to User

Report the saved file:

```
Context saved to: .agent-context/[filename]

Key points captured:
- [List 3-5 key points]

This file can be shared with another agent using:
"Read .agent-context/[filename] for context about [topic]"
```

## Script Usage

Use the save_context.py script to save context:

```bash
python scripts/save_context.py --name "short-name" --content "markdown content"
```

The script will:
- Create `.agent-context/` directory if needed
- Generate timestamped filename
- Save the markdown content
- Return the full path of saved file

## Best Practices

1. **Be Concise**: Focus on actionable information, not conversation history
2. **Prioritize**: Put most important points first
3. **Be Specific**: Include exact file paths, command snippets, error messages
4. **Think Forward**: Write for the next agent - what do they need to succeed?
5. **Include Failures**: Document what didn't work and why
6. **No Sensitive Data**: Avoid including secrets, passwords, or credentials
