---
name: obsidian-canvas
description: Use when user asks to "create a canvas", "make a mind map", "visual diagram", "canvas from notes", "organize visually", "create canvas layout", or mentions Obsidian Canvas, JSON Canvas, visual organization of information, or converting text/notes into spatial visual format.
version: 1.0.0
---

# Obsidian Canvas Creator

Transform text content into structured Obsidian Canvas files (`.canvas`) with support for MindMap and freeform layouts following the JSON Canvas Spec 1.0.

## Core Workflow

### 1. Analyze Content

Read and understand the input content:
- Identify main topics and hierarchical relationships
- Extract key points, facts, and supporting details
- Note any existing structure (headings, lists, sections)

### 2. Determine Layout Type

**MindMap Layout:**
- Radial structure from center
- Parent-child relationships
- Clear hierarchy
- Best for: brainstorming, topic exploration, hierarchical content

**Freeform Layout:**
- Custom positioning
- Flexible relationships
- Multiple connection types
- Best for: complex networks, non-hierarchical content, custom arrangements

### 3. Plan Structure

**For MindMap:**
1. Identify central concept (root node)
2. Map primary branches (main topics)
3. Organize secondary branches (subtopics)
4. Position leaf nodes (details)

**For Freeform:**
1. Group related concepts
2. Identify connection patterns
3. Plan spatial zones
4. Consider visual flow

### 4. Generate Canvas JSON

Canvas files contain two top-level arrays:

```json
{
  "nodes": [...],
  "edges": [...]
}
```

## Node Types

### Text Node
```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 260,
  "height": 120,
  "text": "Content with **Markdown** support"
}
```

### File Node
```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 300,
  "y": 0,
  "width": 400,
  "height": 400,
  "file": "path/to/note.md",
  "subpath": "#Heading"
}
```

### Link Node
```json
{
  "id": "b2c3d4e5f6789012",
  "type": "link",
  "x": 600,
  "y": 0,
  "width": 400,
  "height": 300,
  "url": "https://example.com"
}
```

### Group Node
```json
{
  "id": "c3d4e5f678901234",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 500,
  "height": 400,
  "label": "Category Name",
  "background": "4",
  "backgroundStyle": "cover"
}
```

## Edge Structure

```json
{
  "id": "d4e5f67890123456",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "a1b2c3d4e5f67890",
  "fromSide": "right",
  "toSide": "left",
  "fromEnd": "none",
  "toEnd": "arrow",
  "color": "5",
  "label": "relates to"
}
```

**Side values:** `top`, `right`, `bottom`, `left`
**End values:** `none`, `arrow`

## Node Sizing Guidelines

| Text Length | Dimensions |
|-------------|------------|
| Short (<30 chars) | 220 × 100 px |
| Medium (30-60 chars) | 260 × 120 px |
| Long (60-100 chars) | 320 × 140 px |
| Very long (>100 chars) | 320 × 180 px |

## Color System

**Preset Colors (1-6):**
- `"1"` - Red (warnings, important)
- `"2"` - Orange (action items)
- `"3"` - Yellow (questions, notes)
- `"4"` - Green (positive, completed)
- `"5"` - Cyan (information, details)
- `"6"` - Purple (concepts, abstract)

**Custom Colors:** Use hex format `"#4A90E2"`

## Layout Spacing

- **Minimum horizontal:** 320px between node centers
- **Minimum vertical:** 200px between node centers
- Coordinates can be negative (infinite canvas)
- `x` increases rightward, `y` increases downward

## MindMap Layout Algorithm

1. Place root node at center (0, 0)
2. Distribute primary nodes radially around center
3. Calculate angle per primary: `360° / count`
4. Position at radius: 400px from center
5. Secondary nodes extend outward from their parent
6. Tertiary nodes continue the branch direction

## Critical Rules

### ID Generation
- 16-character lowercase hexadecimal strings
- Must be unique across all nodes and edges
- Example: `"6f0ad84f44ce9c17"`

### Newline Handling
- In JSON, newlines must use `\n` escape sequence
- Using literal `\\n` produces visible `\n` characters

### Quote Escaping
- Escape double quotes in text: `\"`
- For Chinese text, use: `『』` for double, `「」` for single

### Z-Index Order
Output nodes in this order (first = bottom layer):
1. Groups
2. Subgroups
3. Text/File/Link nodes

## Validation Checklist

Before outputting the canvas:
- [ ] All nodes have unique 16-char hex IDs
- [ ] No coordinate overlaps (distance > node dimensions + spacing)
- [ ] All edge `fromNode`/`toNode` reference valid node IDs
- [ ] Groups have labels
- [ ] Colors use consistent format (hex or preset numbers)
- [ ] JSON is properly escaped
- [ ] Only `nodes` and `edges` arrays at top level

## Example: Simple MindMap

Request: "Create a mind map about web development"

```json
{
  "nodes": [
    {"id": "0000000000000001", "type": "text", "x": 0, "y": 0, "width": 260, "height": 100, "text": "Web Development", "color": "6"},
    {"id": "0000000000000002", "type": "text", "x": -400, "y": -150, "width": 220, "height": 80, "text": "Frontend", "color": "5"},
    {"id": "0000000000000003", "type": "text", "x": -400, "y": 150, "width": 220, "height": 80, "text": "Backend", "color": "4"},
    {"id": "0000000000000004", "type": "text", "x": 400, "y": -150, "width": 220, "height": 80, "text": "DevOps", "color": "2"},
    {"id": "0000000000000005", "type": "text", "x": 400, "y": 150, "width": 220, "height": 80, "text": "Databases", "color": "3"},
    {"id": "0000000000000006", "type": "text", "x": -700, "y": -250, "width": 180, "height": 60, "text": "HTML/CSS"},
    {"id": "0000000000000007", "type": "text", "x": -700, "y": -150, "width": 180, "height": 60, "text": "JavaScript"},
    {"id": "0000000000000008", "type": "text", "x": -700, "y": -50, "width": 180, "height": 60, "text": "React/Vue"}
  ],
  "edges": [
    {"id": "e000000000000001", "fromNode": "0000000000000001", "toNode": "0000000000000002", "toEnd": "arrow"},
    {"id": "e000000000000002", "fromNode": "0000000000000001", "toNode": "0000000000000003", "toEnd": "arrow"},
    {"id": "e000000000000003", "fromNode": "0000000000000001", "toNode": "0000000000000004", "toEnd": "arrow"},
    {"id": "e000000000000004", "fromNode": "0000000000000001", "toNode": "0000000000000005", "toEnd": "arrow"},
    {"id": "e000000000000005", "fromNode": "0000000000000002", "toNode": "0000000000000006", "toEnd": "arrow"},
    {"id": "e000000000000006", "fromNode": "0000000000000002", "toNode": "0000000000000007", "toEnd": "arrow"},
    {"id": "e000000000000007", "fromNode": "0000000000000002", "toNode": "0000000000000008", "toEnd": "arrow"}
  ]
}
```

## Tips for Quality Canvases

1. **Keep text concise** - Each node should be scannable (<2 lines)
2. **Use hierarchy** - Group by importance and relationship
3. **Balance the canvas** - Distribute nodes to avoid clustering
4. **Strategic colors** - Use colors to encode meaning
5. **Meaningful connections** - Only add edges that clarify relationships

## References

For complete JSON Canvas specification, see `references/canvas-spec.md`.
