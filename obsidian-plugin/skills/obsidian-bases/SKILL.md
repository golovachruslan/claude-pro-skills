---
name: obsidian-bases
description: Use when user asks to "create a base", "make a database view", "create a table view", "filter notes", "create cards view", "dynamic note list", "query notes", "create formula", or mentions Obsidian Bases, .base files, note databases, computed properties, or aggregating/filtering vault notes.
version: 1.0.0
---

# Obsidian Bases

Create and edit Obsidian Bases (`.base` files) - YAML-based files that define dynamic views of vault notes with filters, formulas, and multiple view types.

## File Format

Bases use the `.base` extension and contain valid YAML syntax.

```yaml
# Basic structure
filter: 'status == "active"'
views:
  - type: table
    name: Active Tasks
```

## Core Components

### Filter

Narrow which notes appear using filter expressions:

```yaml
# Simple filter
filter: 'status == "done"'

# Complex filter with AND/OR
filter:
  and:
    - 'type == "project"'
    - or:
        - 'status == "active"'
        - 'status == "in-progress"'
```

**Operators:**
- Equality: `==`, `!=`
- Comparison: `>`, `<`, `>=`, `<=`
- Logic: `&&`, `||`, `!`
- Contains: `contains(field, "value")`

### Views

Four view types available:

```yaml
views:
  - type: table    # Structured columns
  - type: cards    # Gallery/card layout
  - type: list     # Simple list
  - type: map      # Geographic (requires Maps plugin)
```

### Properties

Three property types:

1. **Note Properties** - Frontmatter fields: `status`, `tags`, `date`
2. **File Properties** - Metadata: `file.name`, `file.path`, `file.ctime`, `file.mtime`, `file.size`
3. **Formula Properties** - Computed values

## View Configuration

### Table View

```yaml
views:
  - type: table
    name: Project Tracker
    properties:
      - property: file.name
        name: Project
        width: 200
      - property: status
        name: Status
      - property: due
        name: Due Date
      - formula: "(due - now()).days"
        name: Days Left
    order:
      - property: due
        direction: asc
    groupby:
      - property: status
    limit: 50
```

### Cards View

```yaml
views:
  - type: cards
    name: Gallery
    properties:
      - property: file.name
      - property: cover
        name: Image
      - property: summary
    cardSize: medium
```

### List View

```yaml
views:
  - type: list
    name: Quick List
    properties:
      - property: file.name
      - property: status
```

### Map View

Requires the Maps plugin and latitude/longitude properties.

```yaml
views:
  - type: map
    name: Locations
    properties:
      - property: file.name
      - property: latitude
      - property: longitude
```

## Formula Syntax

Formulas compute dynamic values using expressions.

### Basic Formulas

```yaml
properties:
  # Days since creation
  - formula: "(now() - file.ctime).days.round(0)"
    name: Age (days)

  # Conditional status
  - formula: 'if(status == "done", "Complete", "Pending")'
    name: State

  # String manipulation
  - formula: "file.name.upper()"
    name: Title
```

### Date Operations

```yaml
# Days until due
- formula: "(due - now()).days.round(0)"
  name: Days Left

# Format date
- formula: 'date.format("MMM DD, YYYY")'
  name: Formatted

# Relative time
- formula: "file.mtime.fromNow()"
  name: Last Modified
```

**Important:** Duration types (from date subtraction) require accessing `.days`, `.hours`, etc. before applying numeric functions like `.round()`.

## Built-in Functions

### Global Functions

| Function | Description | Example |
|----------|-------------|---------|
| `now()` | Current datetime | `now()` |
| `date(str)` | Parse date string | `date("2024-01-15")` |
| `if(cond, then, else)` | Conditional | `if(x > 5, "high", "low")` |
| `min(a, b, ...)` | Minimum value | `min(1, 2, 3)` |
| `max(a, b, ...)` | Maximum value | `max(1, 2, 3)` |
| `link(path)` | Create link | `link("Notes/Index")` |
| `image(path)` | Display image | `image(cover)` |

### String Functions

| Function | Description |
|----------|-------------|
| `.upper()` | Uppercase |
| `.lower()` | Lowercase |
| `.trim()` | Remove whitespace |
| `.contains(str)` | Check substring |
| `.startsWith(str)` | Check prefix |
| `.endsWith(str)` | Check suffix |
| `.replace(old, new)` | Replace text |
| `.split(sep)` | Split to list |
| `.slice(start, end)` | Substring |
| `.length` | Character count |

### Number Functions

| Function | Description |
|----------|-------------|
| `.round(decimals)` | Round to decimals |
| `.floor()` | Round down |
| `.ceil()` | Round up |
| `.abs()` | Absolute value |
| `.toFixed(decimals)` | Format decimals |

### List Functions

| Function | Description |
|----------|-------------|
| `.length` | Count items |
| `.first()` | First element |
| `.last()` | Last element |
| `.join(sep)` | Join to string |
| `.filter(expr)` | Filter items |
| `.map(expr)` | Transform items |
| `.sort()` | Sort ascending |
| `.unique()` | Remove duplicates |
| `.includes(item)` | Check membership |

### File Functions

| Function | Description |
|----------|-------------|
| `hasTag(tag)` | Check for tag |
| `hasLink(path)` | Check for link |
| `inFolder(path)` | Check folder |

## Summary Functions

Add aggregations to table columns:

```yaml
properties:
  - property: amount
    name: Amount
    summary: Sum
  - property: rating
    name: Rating
    summary: Average
```

**Available summaries:**
- **Math:** `Sum`, `Average`, `Min`, `Max`, `Range`
- **Stats:** `Median`, `Stddev`
- **Count:** `Count`, `Checked`, `Unique`, `Empty`, `Filled`
- **Date:** `Earliest`, `Latest`

## Complete Examples

### Project Tracker

```yaml
filter:
  and:
    - 'type == "project"'
    - 'status != "archived"'

views:
  - type: table
    name: Active Projects
    properties:
      - property: file.name
        name: Project
        width: 250
      - property: status
        name: Status
      - property: priority
        name: Priority
      - property: due
        name: Due Date
      - formula: "(due - now()).days.round(0)"
        name: Days Left
      - property: tags
        name: Tags
    order:
      - property: priority
        direction: desc
      - property: due
        direction: asc
    groupby:
      - property: status
```

### Reading List

```yaml
filter: 'type == "book"'

views:
  - type: cards
    name: Library
    properties:
      - property: file.name
      - property: cover
      - property: author
      - property: rating
      - formula: 'if(status == "read", "Completed", "To Read")'
        name: State
    cardSize: large

  - type: table
    name: List View
    properties:
      - property: file.name
        name: Title
      - property: author
        name: Author
      - property: rating
        name: Rating
        summary: Average
      - property: pages
        name: Pages
        summary: Sum
    order:
      - property: rating
        direction: desc
```

### Task Dashboard

```yaml
filter:
  and:
    - 'type == "task"'
    - 'status != "done"'

views:
  - type: table
    name: Open Tasks
    properties:
      - property: file.name
        name: Task
      - property: project
        name: Project
      - property: priority
        name: Priority
      - property: due
        name: Due
      - formula: 'if((due - now()).days < 0, "Overdue", if((due - now()).days < 3, "Soon", "OK"))'
        name: Urgency
    order:
      - property: due
        direction: asc
    groupby:
      - property: project
    limit: 100
```

## YAML Quoting Rules

Use quotes for:
- Strings with special characters: `'status == "done"'`
- Expressions with operators: `"(due - now()).days"`
- Strings starting with special YAML characters

Avoid quotes for:
- Simple property names: `property: status`
- Boolean/number values: `limit: 50`

## Tips

1. **Start simple** - Begin with a basic filter and one view
2. **Test filters** - Verify notes appear before adding complex formulas
3. **Use groupby** - Organize large result sets
4. **Add summaries** - Quick insights on numeric columns
5. **Multiple views** - Same data, different presentations

## References

For complete function reference, see `references/bases-functions.md`.
