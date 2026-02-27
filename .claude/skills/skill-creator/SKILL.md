---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## Core Principles

**Concise is Key**: The context window is a public good. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this?" Prefer concise examples over verbose explanations.

**Set Appropriate Degrees of Freedom**: Match specificity to the task's fragility — narrow bridge with cliffs needs guardrails (low freedom), open field allows many routes (high freedom).

## Skill Structure

```
skill-name/
├── SKILL.md (required) — frontmatter (name, description) + markdown instructions
├── scripts/              — Executable code for deterministic tasks
├── references/           — Documentation loaded into context as-needed
└── assets/               — Files used in output (templates, icons, etc.)
```

For detailed anatomy of each component, see `references/skill-anatomy.md`.

For progressive disclosure patterns (how to split content across files), see `references/progressive-disclosure.md`.

## Skill Creation Process

1. **Understand** the skill with concrete examples
2. **Plan** reusable contents (scripts, references, assets)
3. **Initialize** the skill (run `scripts/init_skill.py <name> --path <dir>`)
4. **Edit** the skill (implement resources, write SKILL.md)
5. **Package** the skill (run `scripts/package_skill.py <path>`)
6. **Iterate** based on real usage

For detailed guidance on each step, see `references/creation-steps.md`.

### Key Rules for SKILL.md

- **Frontmatter**: Only `name` and `description`. Description is the primary trigger — include all "when to use" info here, not in the body
- **Body**: Keep under 500 lines. Move detailed content to `references/`
- **Writing style**: Always use imperative/infinitive form
- **No extraneous files**: No README.md, CHANGELOG.md, etc.

### Design Pattern References

- **Multi-step processes**: See `references/workflows.md`
- **Output formats**: See `references/output-patterns.md`
- **Skill anatomy details**: See `references/skill-anatomy.md`
- **Progressive disclosure**: See `references/progressive-disclosure.md`
- **Step-by-step creation guide**: See `references/creation-steps.md`
