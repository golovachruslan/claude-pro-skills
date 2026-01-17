---
name: agent-context:capture-context
description: Save conversation context with key points and learnings to .agent-context folder
---

# Capture Context Command

Invoke the capture-context skill to save the current conversation context for later use by another agent or for maintaining conversation history.

## Instructions

1. **Activate the capture-context skill** by invoking it through the Skill tool
2. **Follow the capture-context workflow**:
   - Ask user for context name (or auto-generate)
   - Analyze conversation for key points, learnings, technical details
   - Generate structured markdown content
   - Save to `.agent-context/` folder with timestamped filename
   - Confirm saved file location to user

## What This Command Does

This command captures the important context from your current conversation and saves it to a markdown file that can be:
- Shared with another agent to continue the work
- Referenced later for context about past discussions
- Used as documentation of decisions and learnings

## When to Use

Use this command when:
- You want to save important context from a conversation
- You're about to hand off work to another agent
- You want to preserve key learnings and decisions
- You need to document technical details discussed
- You want to create a checkpoint of your progress

## Expected Flow

1. You run `/agent-context:capture-context`
2. Claude asks for a descriptive name (optional)
3. Claude analyzes the conversation
4. Claude generates structured context file
5. Claude saves to `.agent-context/YYYY-MM-DD_name.md`
6. Claude confirms with file path and key points summary

## Example Usage

```
User: /capture-context

Claude: What name would you like for this context file?
(Press Enter or say "auto" to auto-generate based on conversation)

User: implement user authentication

Claude: I'll capture the context from our conversation...

Context saved to: .agent-context/2024-01-15_implement-user-authentication.md

Key points captured:
- Implemented JWT-based authentication
- Created login/logout endpoints in auth.py
- Added middleware for token validation
- Tests passing for auth flows

To share with another agent:
"Read .agent-context/2024-01-15_implement-user-authentication.md for context"
```

## Notes

- Files are saved with date prefix for easy sorting
- Duplicate names get numbered suffix (e.g., `-1`, `-2`)
- Context is structured for easy parsing by other agents
- Sensitive data (passwords, secrets) should be omitted
