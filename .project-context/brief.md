# Project Brief

## Overview
Claude Pro Skills — a Claude Code plugin marketplace and collection of foundational skills. Serves as both a distribution registry (via `.claude-plugin/marketplace.json`) and a repository of reusable skills for creating, improving, and packaging plugins.

## Goals
- Provide a marketplace for distributing Claude Code plugins
- Offer foundational skills (skill-creator, skills-improver, plugin-creator) that bootstrap the ecosystem
- Enable self-improving workflows where skills enhance other skills

## Scope
### In Scope
- Plugin packaging and marketplace distribution
- Skill creation, validation, and improvement workflows
- CI/CD via GitHub Actions (PR reviews, interactive Claude Code execution)
- Plugin types: commands, skills, agents, hooks, MCP servers

### Out of Scope
- Runtime hosting or server-side infrastructure
- End-user application code (this is a tools/skills repo)
- Traditional build/test pipelines (validation is script-based)

---
*Last updated: 2026-03-15*
