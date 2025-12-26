---
name: mermaid
description: Create Mermaid diagrams with renderer-compatible syntax and human-readable ASCII sidecars. Use when user asks to create diagrams, flowcharts, sequence diagrams, ER diagrams, state diagrams, class diagrams, visualize data flow, or mentions Mermaid, visual documentation, or chart creation.
---

# Mermaid Diagrams

Create renderer-compatible Mermaid diagrams with ASCII sidecars for human readability.

## Compatibility Rules

Apply these rules to ensure diagrams render on all platforms (VS Code, GitHub, GitLab, Obsidian):

1. **Use `graph` not `flowchart`**: `graph LR` or `graph TB` (some renderers fail on `flowchart`)
2. **Quote labels**: `A["Text with spaces"]` not `A[Text with spaces]`
3. **Line breaks**: Use `<br/>` not `\n` (Mermaid doesn't interpret `\n`)
4. **Code fence**: Must start at column 0 with language `mermaid`
5. **Advanced types**: quadrantChart, sankey-beta, requirementDiagram, gitGraph may not render - use fallbacks

## ASCII Sidecar Requirement

Always include a text sidecar below each Mermaid block for human readability:

```mermaid
graph LR
  A["Start"] --> B{Auth?}
  B -->|Yes| C["Dashboard"]
  B -->|No|  D["Login"]
```
```text
Diagram: Auth flow (flowchart)
  [Start] --> {Auth?}
      {Auth?} -- Yes --> [Dashboard]
      {Auth?} -- No  --> [Login]
```

**Sidecar rules:**
- Use fenced code with language `text`
- Add caption: `Diagram: <name> (<type>)`
- Keep in sync with Mermaid (Mermaid is source of truth)
- Limit to ~80 columns
- Use: `[Box]`, `{Decision?}`, `-->`, `-- label -->`

## Diagram Type Selection

| Type | Keyword | Use For |
|------|---------|---------|
| **Flowchart** | `graph LR/TB` | Flows, decisions, data movement |
| **Sequence** | `sequenceDiagram` | Actor/service interactions over time |
| **Class** | `classDiagram` | Domain models, entity attributes |
| **State** | `stateDiagram-v2` | Lifecycle, component states |
| **ER** | `erDiagram` | Database schema, cardinalities |
| **Journey** | `journey` | User experience steps |
| **Gantt** | `gantt` | Scheduling, releases |
| **Pie** | `pie` | Simple ratios (prefer tables for precision) |

## References

Load these files as needed:

- **`references/templates.md`** - Complete templates for all 8 diagram types with examples and syntax reference
- **`references/fallbacks-and-troubleshooting.md`** - Fallback templates for unsupported types (quadrant, sankey, requirement, gitGraph), troubleshooting, complex examples
