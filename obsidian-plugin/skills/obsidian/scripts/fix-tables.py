#!/usr/bin/env python3
"""
fix-tables.py
Removes blank lines between table rows in Markdown files
Usage: python3 fix-tables.py <file.md>
"""

import sys


def fix_tables(file_path):
    """Remove blank lines between table rows."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        result.append(line)

        # If this is a table row and next line is blank and line after that is also a table row
        if line.strip().startswith("|"):
            # Skip blank lines between table rows
            while i + 1 < len(lines) and lines[i + 1].strip() == "":
                if i + 2 < len(lines) and lines[i + 2].strip().startswith("|"):
                    i += 1  # Skip the blank line
                else:
                    break

        i += 1

    with open(file_path, "w") as f:
        f.writelines(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix-tables.py <file.md>")
        sys.exit(1)

    file_path = sys.argv[1]
    fix_tables(file_path)
