# Mermaid Plugin for Claude Code

Create renderer-compatible Mermaid diagrams with human-readable ASCII sidecars.

## Overview

This plugin provides a skill for creating Mermaid diagrams that work across different renderers (VS Code, GitHub, GitLab, Obsidian) while maintaining human readability through ASCII sidecar diagrams.

## Features

- **Renderer-compatible templates**: Conservative Mermaid syntax that works on older renderers
- **ASCII sidecars**: Human-readable text diagrams alongside Mermaid code
- **Multiple diagram types**: Flowcharts, sequence, class, state, ER, journey, Gantt, and pie
- **Fallback templates**: Alternatives for unsupported diagram types (quadrant, sankey, requirement, gitGraph)
- **Troubleshooting guidance**: Solutions for common rendering issues

## Installation

### From Marketplace

```bash
/plugin install mermaid@claude-pro-skills
```

### Local Development

```bash
cd /path/to/mermaid-plugin
cc --plugin-dir .
```

## Usage

The skill activates automatically when you:

- Ask to "create a mermaid diagram"
- Request "draw a flowchart" or "make a sequence diagram"
- Mention "ER diagram", "state diagram", "class diagram"
- Say "visualize data flow" or "create a chart"
- Work with Mermaid or visual documentation

### Example Requests

```
"Create a flowchart for the authentication process"
"Draw a sequence diagram for the API call flow"
"Make an ER diagram for the user and orders tables"
"Visualize the state machine for the checkout process"
```

## Supported Diagram Types

| Type | Keyword | Use Case |
|------|---------|----------|
| **Flowchart** | `graph LR/TB` | General flows, decisions, data movement |
| **Sequence** | `sequenceDiagram` | Interactions between actors/services |
| **Class** | `classDiagram` | Domain models, entity attributes |
| **State** | `stateDiagram-v2` | Lifecycle, component states |
| **ER** | `erDiagram` | Database models, cardinalities |
| **Journey** | `journey` | User experience flows |
| **Gantt** | `gantt` | Scheduling, releases, dependencies |
| **Pie** | `pie` | Simple composition/ratios |

## Compatibility Rules

The skill applies these rules for maximum compatibility:

1. **Prefer `graph` over `flowchart`** - Some renderers fail on the `flowchart` keyword
2. **Quote labels with special characters** - `A["Text (x|y)"]` instead of `A[Text]`
3. **Use `<br/>` for line breaks** - Not `\n` which isn't interpreted
4. **Use fallback templates** - For advanced types like quadrant, sankey, requirement, gitGraph

## ASCII Sidecar Format

Every Mermaid diagram includes an ASCII sidecar for human readability:

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

## References

The skill includes additional resources in `skills/mermaid/references/`:

- **fallbacks-and-troubleshooting.md** - Fallback templates for unsupported types, troubleshooting, complex examples, best practices

## Troubleshooting

### Diagram Fails to Render

1. Replace `flowchart` with `graph`
2. Quote node texts: `A["Label"]`
3. Test in [Mermaid Live Editor](https://mermaid.live)
4. Use fallback templates for advanced types

### Common Syntax Errors

- Line breaks: Use `<br/>` not `\n`
- Special characters: Quote labels with parentheses, pipes
- Code fence: Must start at column 0

## License

MIT License - See LICENSE file for details

## Support

- Issues: https://github.com/golovachruslan/claude-pro-skills/issues
- Documentation: https://github.com/golovachruslan/claude-pro-skills

## Changelog

### 1.0.0 (2025-12-26)

- Initial release
- Mermaid diagrams skill with renderer-compatible templates
- Support for 8 diagram types (flowchart, sequence, class, state, ER, journey, Gantt, pie)
- ASCII sidecar generation for human readability
- Fallback templates for unsupported diagram types
- Comprehensive troubleshooting guidance
