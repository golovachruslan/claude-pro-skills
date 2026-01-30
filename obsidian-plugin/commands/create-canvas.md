# Create Canvas

Create an Obsidian Canvas file with visual layouts for organizing information.

## Usage

```
/create-canvas [topic or content]
```

## Examples

- `/create-canvas mind map about machine learning concepts`
- `/create-canvas project timeline for Q1 goals`
- `/create-canvas organize my research notes visually`

## What it does

1. Analyzes your topic or provided content
2. Determines the best layout (MindMap or freeform)
3. Generates a valid `.canvas` file with nodes and edges
4. Places the canvas in your vault

## Options

- **MindMap**: Hierarchical radial layout from central concept
- **Freeform**: Flexible positioning for complex relationships

The skill uses the obsidian-canvas skill to generate properly formatted JSON Canvas files.
