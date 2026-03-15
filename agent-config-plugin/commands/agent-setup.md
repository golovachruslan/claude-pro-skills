---
name: agent-config:agent-setup
description: Configure Claude Code plugin ecosystem for a project with setup.yaml, setup.sh, and SessionStart hook
---

# Agent Setup Command

Configure a Claude Code plugin ecosystem for any project so teammates get all plugins automatically.

## Instructions

1. **Activate the agent-setup skill** by invoking it through the Skill tool
2. **Follow the agent-setup workflow**:
   - Determine target directory
   - Interview user for marketplaces and plugins
   - Generate setup.yaml
   - Copy setup.sh to target
   - Add SessionStart hook to .claude/settings.json
   - Print summary with next steps

## When to Use

Use this command when:
- Setting up a new project with Claude Code plugins
- Configuring automatic plugin installation for a team
- Adding marketplace sources and plugins to a project
- Creating onboarding automation for Claude Code users
