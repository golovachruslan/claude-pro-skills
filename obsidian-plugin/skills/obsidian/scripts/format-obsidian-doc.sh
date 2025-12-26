#!/bin/bash
# format-obsidian-doc.sh
# Master script to format Obsidian markdown documents
# Usage: ./format-obsidian-doc.sh "path/to/file.md"

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file.md>"
    echo "Example: $0 /path/to/document.md"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found"
    exit 1
fi

echo "Formatting Obsidian document: $FILE"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create backup
BACKUP="${FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$FILE" "$BACKUP"
echo "✓ Backup created: $BACKUP"

# Step 1: Remove lines with only two spaces and squeeze blank lines
echo "→ Removing excessive whitespace..."
sed 's/^  $//' "$FILE" | cat -s > "${FILE}.tmp"
mv "${FILE}.tmp" "$FILE"
echo "✓ Whitespace cleaned"

# Step 2: Clean Mermaid diagrams
echo "→ Cleaning Mermaid diagrams..."
awk -f "$SCRIPT_DIR/clean-mermaid.awk" "$FILE" > "${FILE}.tmp"
mv "${FILE}.tmp" "$FILE"
echo "✓ Mermaid diagrams cleaned"

# Step 3: Fix tables
echo "→ Fixing table formatting..."
python3 "$SCRIPT_DIR/fix-tables.py" "$FILE"
echo "✓ Tables fixed"

# Get line count
LINES=$(wc -l < "$FILE")
echo ""
echo "✓ Formatting complete!"
echo "  File: $FILE"
echo "  Lines: $LINES"
echo "  Backup: $BACKUP"
