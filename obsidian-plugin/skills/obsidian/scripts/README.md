# Obsidian Document Formatting Scripts

Utility scripts for cleaning up and formatting Obsidian markdown documents.

## Scripts

### format-obsidian-doc.sh (Master Script)

Complete formatting pipeline that runs all cleanup operations.

**Usage:**
```bash
./format-obsidian-doc.sh "path/to/file.md"
```

**What it does:**
1. Creates timestamped backup (`.backup.YYYYMMDD_HHMMSS`)
2. Removes lines with only two spaces
3. Squeezes multiple blank lines into single lines
4. Cleans all Mermaid diagrams
5. Fixes table formatting

**Example:**
```bash
./format-obsidian-doc.sh "../../Projects/uCollect/uCollect BE.md"
```

### clean-mermaid.awk

Removes blank lines within Mermaid code blocks while preserving diagram structure.

**Usage:**
```bash
awk -f clean-mermaid.awk input.md > output.md
```

**What it does:**
- Identifies ````mermaid` code blocks
- Removes blank lines between diagram elements
- Preserves all other content unchanged

### fix-tables.py

Removes blank lines between Markdown table rows.

**Usage:**
```bash
python3 fix-tables.py document.md
```

**What it does:**
- Identifies table rows (lines starting with `|`)
- Removes blank lines between consecutive table rows
- Preserves table structure and alignment
- Modifies file in-place

## Common Use Cases

### Clean up imported document
```bash
./format-obsidian-doc.sh "messy-import.md"
```

### Fix only Mermaid diagrams
```bash
awk -f clean-mermaid.awk document.md > document-cleaned.md
mv document-cleaned.md document.md
```

### Fix only tables
```bash
python3 fix-tables.py document.md
```

## Troubleshooting

### Mermaid parse errors
Run `clean-mermaid.awk` to remove blank lines that cause parsing issues.

### Table formatting issues
Run `fix-tables.py` to ensure proper single-line spacing between rows.

### File permissions
If scripts won't execute, make them executable:
```bash
chmod +x format-obsidian-doc.sh clean-mermaid.awk fix-tables.py
```

## Benefits

- **Token efficient**: Scripts execute without loading into context
- **Deterministic**: Consistent formatting every time
- **Reusable**: Single command vs. multiple manual steps
- **Safe**: Master script creates automatic backups
