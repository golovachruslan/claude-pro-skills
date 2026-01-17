#!/usr/bin/env python3
"""
Find Related Notes Script

Searches an Obsidian vault for notes related to given topics, files, or keywords.

Usage:
    python find_related_notes.py <vault-path> --topics "topic1,topic2" --files "file1.ts,file2.py"
    python find_related_notes.py <vault-path> --keywords "authentication,API"
    python find_related_notes.py --help

Output: JSON with related notes and suggested updates
"""

import sys
import os
import json
import re
import argparse
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class RelatedNote:
    """Represents a note related to the search criteria."""
    path: str
    title: str
    match_type: str  # 'topic', 'file', 'keyword', 'tag'
    match_details: str
    suggested_update: str
    relevance_score: float


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Handle arrays
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
            frontmatter[key] = value

    return frontmatter


def extract_title(content: str, filepath: Path) -> str:
    """Extract title from note content or filename."""
    # Try H1 header first
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Try frontmatter title
    fm = extract_frontmatter(content)
    if 'title' in fm:
        return fm['title']

    # Fall back to filename
    return filepath.stem


def calculate_relevance(matches: list[str], match_type: str) -> float:
    """Calculate relevance score based on matches."""
    base_scores = {
        'topic': 0.8,
        'file': 0.9,
        'keyword': 0.6,
        'tag': 0.7,
    }

    base = base_scores.get(match_type, 0.5)
    # More matches = higher score (diminishing returns)
    match_bonus = min(len(matches) * 0.1, 0.3)

    return min(base + match_bonus, 1.0)


def suggest_update(match_type: str, match_details: str, note_title: str) -> str:
    """Generate a suggested update for the related note."""
    suggestions = {
        'topic': f"Add link to capture in '{note_title}' topic section",
        'file': f"Reference this session in '{note_title}' development log",
        'keyword': f"Link to this capture from relevant section in '{note_title}'",
        'tag': f"Add bidirectional link in '{note_title}'",
    }
    return suggestions.get(match_type, f"Consider linking to '{note_title}'")


def search_vault(
    vault_path: Path,
    topics: list[str],
    files: list[str],
    keywords: list[str],
    exclude_patterns: Optional[list[str]] = None,
) -> list[RelatedNote]:
    """Search vault for related notes."""
    if exclude_patterns is None:
        exclude_patterns = ['.git', '.obsidian', 'node_modules', '.trash']

    related_notes = []
    seen_paths = set()

    # Normalize search terms
    topics_lower = [t.lower().strip() for t in topics if t.strip()]
    files_lower = [f.lower().strip() for f in files if f.strip()]
    keywords_lower = [k.lower().strip() for k in keywords if k.strip()]

    # Get just filenames without paths for file matching
    file_names = [Path(f).stem.lower() for f in files_lower]

    for md_file in vault_path.rglob('*.md'):
        # Skip excluded directories
        if any(excl in str(md_file) for excl in exclude_patterns):
            continue

        # Skip capture notes themselves
        if 'Claude Session' in md_file.name or 'claude-capture' in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue

        content_lower = content.lower()
        relative_path = str(md_file.relative_to(vault_path))
        title = extract_title(content, md_file)
        frontmatter = extract_frontmatter(content)

        # Check for topic matches
        if topics_lower:
            topic_matches = []
            for topic in topics_lower:
                if topic in content_lower:
                    topic_matches.append(topic)
                # Check tags
                tags = frontmatter.get('tags', [])
                if isinstance(tags, list):
                    if any(topic in str(tag).lower() for tag in tags):
                        topic_matches.append(f"tag:{topic}")

            if topic_matches and relative_path not in seen_paths:
                seen_paths.add(relative_path)
                related_notes.append(RelatedNote(
                    path=relative_path,
                    title=title,
                    match_type='topic',
                    match_details=f"Topics: {', '.join(topic_matches)}",
                    suggested_update=suggest_update('topic', ', '.join(topic_matches), title),
                    relevance_score=calculate_relevance(topic_matches, 'topic'),
                ))

        # Check for file references
        if file_names and relative_path not in seen_paths:
            file_matches = []
            for file_name in file_names:
                if file_name in content_lower:
                    file_matches.append(file_name)

            if file_matches:
                seen_paths.add(relative_path)
                related_notes.append(RelatedNote(
                    path=relative_path,
                    title=title,
                    match_type='file',
                    match_details=f"References: {', '.join(file_matches)}",
                    suggested_update=suggest_update('file', ', '.join(file_matches), title),
                    relevance_score=calculate_relevance(file_matches, 'file'),
                ))

        # Check for keyword matches
        if keywords_lower and relative_path not in seen_paths:
            keyword_matches = []
            for keyword in keywords_lower:
                if keyword in content_lower:
                    keyword_matches.append(keyword)

            if keyword_matches:
                seen_paths.add(relative_path)
                related_notes.append(RelatedNote(
                    path=relative_path,
                    title=title,
                    match_type='keyword',
                    match_details=f"Keywords: {', '.join(keyword_matches)}",
                    suggested_update=suggest_update('keyword', ', '.join(keyword_matches), title),
                    relevance_score=calculate_relevance(keyword_matches, 'keyword'),
                ))

    # Sort by relevance
    related_notes.sort(key=lambda x: x.relevance_score, reverse=True)

    return related_notes


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Find notes related to given topics, files, or keywords.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('vault_path', help='Path to Obsidian vault')
    parser.add_argument('--topics', default='', help='Comma-separated list of topics')
    parser.add_argument('--files', default='', help='Comma-separated list of files')
    parser.add_argument('--keywords', default='', help='Comma-separated list of keywords')
    parser.add_argument('--limit', type=int, default=10, help='Maximum number of results')
    parser.add_argument('--min-score', type=float, default=0.5, help='Minimum relevance score')

    args = parser.parse_args()

    vault_path = Path(args.vault_path).expanduser().resolve()

    if not vault_path.exists():
        print(json.dumps({'error': f'Vault path does not exist: {vault_path}'}))
        sys.exit(1)

    if not vault_path.is_dir():
        print(json.dumps({'error': f'Vault path is not a directory: {vault_path}'}))
        sys.exit(1)

    topics = [t.strip() for t in args.topics.split(',') if t.strip()]
    files = [f.strip() for f in args.files.split(',') if f.strip()]
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]

    if not topics and not files and not keywords:
        print(json.dumps({'error': 'At least one of --topics, --files, or --keywords must be provided'}))
        sys.exit(1)

    results = search_vault(vault_path, topics, files, keywords)

    # Filter by score and limit
    filtered = [r for r in results if r.relevance_score >= args.min_score][:args.limit]

    output = {
        'vault_path': str(vault_path),
        'search_criteria': {
            'topics': topics,
            'files': files,
            'keywords': keywords,
        },
        'related_notes': [asdict(note) for note in filtered],
        'total_found': len(results),
        'returned': len(filtered),
    }

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
