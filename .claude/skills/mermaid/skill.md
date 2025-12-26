---
name: mermaid
description: This skill should be used when the user asks to "create a mermaid diagram", "draw a flowchart", "make a sequence diagram", "create an ER diagram", "draw a state diagram", "visualize data flow", "create a class diagram", or mentions Mermaid, diagrams, visual documentation, or chart creation. Provides conservative, renderer-compatible Mermaid templates with human-readable ASCII sidecars. (project)
license: MIT
version: 0.1.0
---

# Mermaid Diagrams Skill

This skill provides:
- Conservative Mermaid templates that render on older renderers (VS Code/Markdown previewers, Git platforms) and remain clear to humans
- Guidance on which diagram type to use for specific situations
- Compatibility tips and fallbacks when advanced Mermaid types are unavailable
- Human-readable ASCII/Unicode sidecars for each diagram

## Compatibility Rules

Apply these rules when creating Mermaid diagrams:

- Prefer `graph LR`/`graph TB` for flowcharts; some renderers fail on `flowchart` keyword
- Quote labels containing spaces/special characters: `A["Text (x|y) |"]`
- **Do not use literal `\n` inside labels** – Mermaid does not interpret these line breaks. Use `<br/>` for line breaks instead
- Advanced types like `quadrantChart`, `sankey-beta`, `requirementDiagram`, `gitGraph` may not be available. Use provided flowchart fallbacks
- Code fences must start at column 0 with language `mermaid`

## ASCII/Unicode Sidecar (Human-Readable Raw Markdown)

Always include an ASCII/Unicode sidecar immediately below each Mermaid block to optimize for quick human scanning in raw Markdown and robust parsing by agents.

**Requirements:**
- Include a monospace, text-only diagram right under the Mermaid block using fenced code with language `text`
- Keep Mermaid and sidecar in sync (same nodes/edges, same labels where feasible). If they diverge, treat Mermaid as the source of truth and update the sidecar
- Limit width to ~80 columns for readability in diffs and terminals
- Use simple line art characters (ASCII first; Unicode box-drawing optional when environment supports it)
- Add a one-line caption above the pair: `Diagram: <name> (<type>)`

**Recommended primitives:**
- Boxes: `[Name]`, `(Name)`, `+-----+\n| N |\n+-----+`
- Flows: `-->`, decisions as `{cond?}` lines, lists with `•` or `-`
- Sequence (text-based): `Actor -> Actor: message` with indented lifelines

Example (Flowchart):
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

Example (Text-based Sequence):
```mermaid
sequenceDiagram
  participant U as User
  participant W as WebApp
  U->>W: Open
  W-->>U: OK
```
```text
Diagram: Happy path (sequence)
  User -> WebApp : Open
  WebApp -> User : OK
```

## Working Templates (Renderer-Compatible)

### Flowchart
```mermaid
graph LR
  A["Start"] --> B{Auth?}
  B -->|Yes| C["Dashboard"]
  B -->|No|  D["Login"]
  C --> E["Settings"]
```

### Sequence
```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant W as WebApp
  participant API
  U->>W: Open
  W->>API: GET /status
  API-->>W: 200
  W-->>U: OK
```

### Class
```mermaid
classDiagram
  class User {
    +String id
    +String name
    +login(): bool
  }
  class Order {
    +String id
    +Decimal total
    +submit()
  }
  User "1" o-- "*" Order
```

### State (v2)
```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Loading : fetch
  Loading --> Ready : ok
  Loading --> Error : fail
  state Ready {
    [*] --> Viewing
    Viewing --> Editing : edit
    Editing --> Viewing : save
  }
  Error --> Idle : retry
```

### ER (Entity-Relationship)
```mermaid
erDiagram
  USER ||--o{ ORDER : places
  ORDER ||--|{ ORDER_LINE : contains
  PRODUCT ||--o{ ORDER_LINE : referenced
  USER {
    string id
    string email
  }
  PRODUCT {
    string id
    string name
    float price
  }
```

### Journey (User Journey)
```mermaid
journey
  title Checkout UX
  section Browse
    "See product": 5: User
    "Add to cart": 4: User
  section Payment
    "Enter card": 2: User
    "3DS confirm": 2: User
  section Result
    "Success page": 5: User
```

### Gantt
```mermaid
gantt
  title Release Plan
  dateFormat  YYYY-MM-DD
  section Dev
  Spec  :done,   des1, 2025-10-01,2025-10-05
  Impl  :active, des2, 2025-10-06,2025-10-20
  Tests :        des3, 2025-10-21, 7d
  section Release
  Freeze :milestone, m1, 2025-10-28, 0d
  Deploy :crit,    des4, 2025-10-29, 1d
```

### Pie (compatible syntax)
```mermaid
pie
  title Traffic by Source
  "Direct"  : 35
  "Organic" : 45
  "Ads"     : 20
```

## When to Use Which Diagram

Choose the appropriate diagram type based on the content:

- **Flowchart**: General flows, decisions, and data movement in specs and PRDs
- **Sequence**: Interactions over time between actors/services (APIs, requests, responses)
- **Class**: Domain models and static structure; useful for entity attributes and relations
- **State**: Lifecycle of an entity/component (idle → loading → ready/error, nested states)
- **ER**: Database/logical data model with cardinalities
- **Journey**: User experience across steps/sections (great for PRD acceptance flows)
- **Gantt**: Scheduling, releases, and dependencies by dates
- **Pie**: Simple composition/ratios; prefer tables when precision matters

## Additional Resources

### Reference Files

For advanced diagram types and troubleshooting, consult:
- **`references/fallbacks-and-troubleshooting.md`** - Fallback templates for unsupported diagram types (quadrant, requirement, sankey, gitGraph), troubleshooting guidance, complex examples, and best practices

Use fallback templates when advanced Mermaid types are unavailable in the target renderer.
