#!/usr/bin/env python3
"""
Save agent conversation context to .agent-context folder.

Usage:
    python save_context.py --name "short-name" --content "markdown content"
    python save_context.py --name "short-name" --file content.md
    python save_context.py --content "markdown content"  # Auto-generates name
    echo "content" | python save_context.py --name "short-name"  # From stdin
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def sanitize_filename(name: str) -> str:
    """Convert name to kebab-case filename-safe string."""
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and underscores with hyphens
    name = re.sub(r'[\s_]+', '-', name)
    # Remove any character that isn't alphanumeric or hyphen
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Truncate to max 50 characters
    if len(name) > 50:
        name = name[:50].rstrip('-')
    return name


def generate_name_from_content(content: str) -> str:
    """Generate a short descriptive name from content."""
    # Try to extract from first heading
    heading_match = re.search(r'^#\s*(?:Context:\s*)?(.+)$', content, re.MULTILINE)
    if heading_match:
        return sanitize_filename(heading_match.group(1))

    # Try to extract from Summary section
    summary_match = re.search(r'##\s*Summary\s*\n+(.+?)(?:\n\n|\n##|$)', content, re.DOTALL)
    if summary_match:
        # Get first sentence
        first_sentence = summary_match.group(1).split('.')[0]
        # Take first few words
        words = first_sentence.split()[:5]
        return sanitize_filename(' '.join(words))

    # Fallback: use first non-empty line
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            words = line.split()[:5]
            return sanitize_filename(' '.join(words))

    return 'context'


def save_context(name: str | None, content: str, output_dir: str = '.agent-context') -> str:
    """
    Save context to .agent-context folder.

    Args:
        name: Short descriptive name (auto-generated if None)
        content: Markdown content to save
        output_dir: Output directory (default: .agent-context)

    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate or sanitize name
    if name:
        safe_name = sanitize_filename(name)
    else:
        safe_name = generate_name_from_content(content)

    if not safe_name:
        safe_name = 'context'

    # Generate filename with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}_{safe_name}.md"

    # Handle duplicate filenames
    file_path = output_path / filename
    counter = 1
    while file_path.exists():
        filename = f"{date_str}_{safe_name}-{counter}.md"
        file_path = output_path / filename
        counter += 1

    # Save content
    file_path.write_text(content, encoding='utf-8')

    return str(file_path)


def main():
    parser = argparse.ArgumentParser(
        description='Save agent conversation context to .agent-context folder'
    )
    parser.add_argument(
        '--name', '-n',
        help='Short descriptive name for the context (auto-generated if not provided)'
    )
    parser.add_argument(
        '--content', '-c',
        help='Markdown content to save'
    )
    parser.add_argument(
        '--file', '-f',
        help='Read content from file instead of --content'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='.agent-context',
        help='Output directory (default: .agent-context)'
    )

    args = parser.parse_args()

    # Get content from various sources
    content = None

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.content:
        content = args.content
    elif not sys.stdin.isatty():
        content = sys.stdin.read()

    if not content:
        print("Error: No content provided. Use --content, --file, or pipe to stdin.", file=sys.stderr)
        sys.exit(1)

    # Save context
    try:
        saved_path = save_context(args.name, content, args.output_dir)
        print(f"Context saved to: {saved_path}")
    except Exception as e:
        print(f"Error saving context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
