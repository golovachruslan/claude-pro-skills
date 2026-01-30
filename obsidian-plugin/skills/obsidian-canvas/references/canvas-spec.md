# JSON Canvas Specification 1.0

This document describes the complete JSON Canvas file format for Obsidian `.canvas` files.

## File Format

Canvas files use the `.canvas` extension and contain valid JSON conforming to this specification.

## Top-Level Structure

```json
{
  "nodes": [],
  "edges": []
}
```

Both arrays are required. Empty arrays are valid for an empty canvas.

## Nodes

### Common Node Properties

All nodes share these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique 16-character lowercase hex string |
| `type` | string | Yes | One of: `text`, `file`, `link`, `group` |
| `x` | number | Yes | X coordinate (increases rightward) |
| `y` | number | Yes | Y coordinate (increases downward) |
| `width` | number | Yes | Width in pixels (minimum 50) |
| `height` | number | Yes | Height in pixels (minimum 50) |
| `color` | string | No | Preset ("1"-"6") or hex ("#RRGGBB") |

### Text Node

Contains Markdown-formatted text content.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `text` | string | Yes | Markdown content |

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 100,
  "y": 200,
  "width": 260,
  "height": 120,
  "text": "# Heading\n\nParagraph with **bold** and *italic*.",
  "color": "4"
}
```

### File Node

References a file in the vault.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `file` | string | Yes | Path to file relative to vault root |
| `subpath` | string | No | Heading (`#Heading`) or block (`#^blockid`) reference |

```json
{
  "id": "a1b2c3d4e5f67890",
  "type": "file",
  "x": 400,
  "y": 200,
  "width": 400,
  "height": 400,
  "file": "Projects/My Project.md",
  "subpath": "#Overview"
}
```

### Link Node

Embeds an external URL.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | string | Yes | Full URL including protocol |

```json
{
  "id": "b2c3d4e5f6789012",
  "type": "link",
  "x": 800,
  "y": 200,
  "width": 400,
  "height": 300,
  "url": "https://obsidian.md"
}
```

### Group Node

Visual container for organizing other nodes.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `label` | string | No | Display name in group header |
| `background` | string | No | Background color (preset or hex) |
| `backgroundStyle` | string | No | `cover` or `ratio` for image backgrounds |

```json
{
  "id": "c3d4e5f678901234",
  "type": "group",
  "x": 50,
  "y": 150,
  "width": 600,
  "height": 400,
  "label": "Research Notes",
  "background": "5"
}
```

Groups are rendered below other nodes. Nodes within the group's bounds appear inside it visually.

## Edges

Edges connect nodes with lines/arrows.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique 16-character lowercase hex string |
| `fromNode` | string | Yes | ID of source node |
| `toNode` | string | Yes | ID of target node |
| `fromSide` | string | No | Connection point: `top`, `right`, `bottom`, `left` |
| `toSide` | string | No | Connection point: `top`, `right`, `bottom`, `left` |
| `fromEnd` | string | No | End style: `none`, `arrow` |
| `toEnd` | string | No | End style: `none`, `arrow` |
| `color` | string | No | Preset ("1"-"6") or hex ("#RRGGBB") |
| `label` | string | No | Text displayed on the edge |

```json
{
  "id": "d4e5f67890123456",
  "fromNode": "6f0ad84f44ce9c17",
  "toNode": "a1b2c3d4e5f67890",
  "fromSide": "right",
  "toSide": "left",
  "fromEnd": "none",
  "toEnd": "arrow",
  "color": "2",
  "label": "references"
}
```

## Color Presets

| Preset | Color |
|--------|-------|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Custom colors use hex format: `"#FF5733"` (always uppercase hex digits).

## Coordinate System

- Origin (0, 0) is at canvas center
- X increases to the right
- Y increases downward
- Negative coordinates are valid (infinite canvas)
- Coordinates represent the top-left corner of nodes

## ID Requirements

- Exactly 16 lowercase hexadecimal characters
- Must be unique across all nodes and edges in the file
- Example: `"6f0ad84f44ce9c17"`

Generation method: Random hex or sequential with prefix.

## Text Escaping

In JSON strings:
- Newlines: `\n` (not literal line breaks)
- Quotes: `\"`
- Backslashes: `\\`
- Tabs: `\t`

Example:
```json
{
  "text": "Line 1\nLine 2\n\n**Bold text** with \"quotes\""
}
```

## Validation Rules

1. All IDs must be unique 16-character hex strings
2. All `fromNode` and `toNode` values must reference existing node IDs
3. `type` must be one of: `text`, `file`, `link`, `group`
4. `width` and `height` must be positive numbers (minimum 50)
5. File nodes must have non-empty `file` property
6. Link nodes must have non-empty `url` property
7. Text nodes must have `text` property (can be empty string)

## Complete Example

```json
{
  "nodes": [
    {
      "id": "0000000000000001",
      "type": "group",
      "x": -100,
      "y": -100,
      "width": 700,
      "height": 500,
      "label": "Project Overview",
      "background": "5"
    },
    {
      "id": "0000000000000002",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 260,
      "height": 100,
      "text": "# Main Topic\n\nCentral concept for the project.",
      "color": "6"
    },
    {
      "id": "0000000000000003",
      "type": "file",
      "x": 320,
      "y": 0,
      "width": 250,
      "height": 200,
      "file": "Notes/Research.md"
    },
    {
      "id": "0000000000000004",
      "type": "text",
      "x": 0,
      "y": 200,
      "width": 220,
      "height": 80,
      "text": "Supporting detail",
      "color": "4"
    },
    {
      "id": "0000000000000005",
      "type": "link",
      "x": 320,
      "y": 250,
      "width": 250,
      "height": 150,
      "url": "https://example.com/docs"
    }
  ],
  "edges": [
    {
      "id": "e000000000000001",
      "fromNode": "0000000000000002",
      "toNode": "0000000000000003",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e000000000000002",
      "fromNode": "0000000000000002",
      "toNode": "0000000000000004",
      "fromSide": "bottom",
      "toSide": "top",
      "toEnd": "arrow"
    },
    {
      "id": "e000000000000003",
      "fromNode": "0000000000000003",
      "toNode": "0000000000000005",
      "toEnd": "arrow",
      "label": "documentation"
    }
  ]
}
```
