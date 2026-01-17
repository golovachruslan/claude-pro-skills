#!/usr/bin/env python3
"""
Capture Conversation Script

Analyzes a Claude Code conversation and generates structured output
for creating an Obsidian capture note.

Usage:
    python capture_conversation.py [--quick] < conversation.txt
    python capture_conversation.py --help

Output: JSON with extracted information for note generation
"""

import sys
import json
import re
from datetime import datetime
from typing import Optional


def detect_session_type(text: str) -> str:
    """Detect the type of session based on conversation content."""
    text_lower = text.lower()

    patterns = {
        'bug-fix': ['fix', 'bug', 'error', 'broken', 'issue', 'debug', 'crash', 'exception'],
        'feature': ['implement', 'add feature', 'create', 'new feature', 'build'],
        'refactor': ['refactor', 'improve', 'clean up', 'reorganize', 'restructure', 'optimize'],
        'documentation': ['document', 'readme', 'docstring', 'comment', 'explain'],
        'review': ['review', 'check', 'audit', 'look at', 'examine'],
        'learning': ['how does', 'what is', 'learn', 'understand', 'explain'],
        'exploration': ['explore', 'investigate', 'research', 'find out', 'discover'],
    }

    scores = {session_type: 0 for session_type in patterns}

    for session_type, keywords in patterns.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[session_type] += 1

    max_score = max(scores.values())
    if max_score == 0:
        return 'general'

    return max(scores, key=scores.get)


def extract_file_paths(text: str) -> list[str]:
    """Extract file paths mentioned in the conversation."""
    # Common patterns for file paths
    patterns = [
        r'`([a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)`',  # Backtick-wrapped paths
        r'(?:^|\s)([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)',  # Path with directory
        r'(?:reading|wrote|created|modified|editing)\s+`?([^\s`]+\.[a-zA-Z0-9]+)`?',  # Action + file
    ]

    files = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            # Filter out common false positives
            if not any(fp in match.lower() for fp in ['http', 'https', 'example.', 'e.g.']):
                if '/' in match or match.count('.') == 1:
                    files.add(match)

    return sorted(list(files))


def extract_topics(text: str) -> list[str]:
    """Extract main topics from conversation."""
    # Look for common topic indicators
    topic_patterns = [
        r'(?:working on|about|regarding|for)\s+([a-zA-Z][a-zA-Z0-9\s\-]+?)(?:\.|,|\?|$)',
        r'(?:implement|create|fix|add)\s+(?:a\s+)?([a-zA-Z][a-zA-Z0-9\s\-]+?)(?:\.|,|\?|$)',
    ]

    topics = set()
    for pattern in topic_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            cleaned = match.strip().lower()
            if len(cleaned) > 3 and len(cleaned) < 50:
                topics.add(cleaned)

    return sorted(list(topics))[:5]  # Limit to 5 topics


def extract_action_items(text: str) -> list[str]:
    """Extract potential action items and TODOs."""
    patterns = [
        r'(?:TODO|FIXME|NOTE):\s*(.+?)(?:\n|$)',
        r'(?:need to|should|will)\s+(.+?)(?:\.|$)',
        r'(?:next step|action item):\s*(.+?)(?:\n|$)',
    ]

    items = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        items.extend(matches)

    # Deduplicate and limit
    seen = set()
    unique_items = []
    for item in items:
        cleaned = item.strip()
        if cleaned.lower() not in seen and len(cleaned) > 5:
            seen.add(cleaned.lower())
            unique_items.append(cleaned)

    return unique_items[:10]


def generate_title(text: str, session_type: str, files: list[str]) -> str:
    """Generate a descriptive title for the session."""
    # Try to extract a meaningful title from context
    title_patterns = [
        r'(?:implement|create|fix|add|build)\s+([a-zA-Z][a-zA-Z0-9\s\-]+?)(?:\.|,|\?|$)',
        r'(?:working on)\s+([a-zA-Z][a-zA-Z0-9\s\-]+?)(?:\.|,|\?|$)',
    ]

    for pattern in title_patterns:
        matches = re.findall(pattern, text[:500], re.IGNORECASE)
        if matches:
            title = matches[0].strip().title()
            if len(title) > 5 and len(title) < 60:
                return title

    # Fallback: use session type and first file
    type_names = {
        'bug-fix': 'Bug Fix',
        'feature': 'Feature Implementation',
        'refactor': 'Code Refactoring',
        'documentation': 'Documentation Update',
        'review': 'Code Review',
        'learning': 'Learning Session',
        'exploration': 'Exploration',
        'general': 'Development Session',
    }

    base_title = type_names.get(session_type, 'Session')

    if files:
        # Get the most significant file name
        main_file = files[0].split('/')[-1].rsplit('.', 1)[0]
        return f"{base_title} - {main_file}"

    return base_title


def analyze_conversation(text: str, quick_mode: bool = False) -> dict:
    """Analyze conversation and extract structured information."""
    today = datetime.now().strftime('%Y-%m-%d')

    session_type = detect_session_type(text)
    files = extract_file_paths(text)

    result = {
        'date': today,
        'session_type': session_type,
        'files_touched': files,
        'title': generate_title(text, session_type, files),
        'status': 'quick-capture' if quick_mode else 'captured',
    }

    if not quick_mode:
        result['topics'] = extract_topics(text)
        result['action_items'] = extract_action_items(text)
        result['word_count'] = len(text.split())

    return result


def main():
    """Main entry point."""
    quick_mode = '--quick' in sys.argv

    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Read conversation from stdin
    if sys.stdin.isatty():
        print("Error: No input provided. Pipe conversation text to this script.", file=sys.stderr)
        print("Usage: python capture_conversation.py < conversation.txt", file=sys.stderr)
        sys.exit(1)

    text = sys.stdin.read()

    if not text.strip():
        print("Error: Empty input", file=sys.stderr)
        sys.exit(1)

    result = analyze_conversation(text, quick_mode)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
