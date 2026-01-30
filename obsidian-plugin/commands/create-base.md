# Create Base

Create an Obsidian Base file for dynamic views of your vault notes.

## Usage

```
/create-base [description of what to track]
```

## Examples

- `/create-base track all my projects with status and due dates`
- `/create-base reading list with ratings and authors`
- `/create-base task dashboard grouped by project`

## What it does

1. Understands what notes you want to query
2. Designs appropriate filters and properties
3. Creates views (table, cards, list) for your data
4. Adds formulas for computed fields if needed
5. Generates a valid `.base` file

## View Types

- **Table**: Structured columns with sorting and grouping
- **Cards**: Visual gallery layout
- **List**: Simple linear presentation
- **Map**: Geographic view (requires Maps plugin)

The skill uses the obsidian-bases skill to generate properly formatted YAML base files.
