#!/usr/bin/env python3
"""
Improvement Applicator - Applies approved improvements to skills/plugins

This script takes a JSON file containing approved improvements and applies them
to the specified skill or plugin files.

Usage:
    python apply_improvements.py <skill-or-plugin-path> <improvements.json>

Example:
    python apply_improvements.py .claude/skills/my-skill improvements.json

improvements.json format:
{
  "target": "skill-name",
  "changes": [
    {
      "file": "SKILL.md",
      "type": "edit|write",
      "old_content": "text to replace (for edits)",
      "new_content": "replacement text"
    }
  ]
}
"""

import sys
import json
from pathlib import Path
from typing import Dict, List


class ImprovementApplicator:
    """Applies improvements to skill/plugin files"""

    def __init__(self, target_path: Path):
        self.target_path = target_path
        self.changes_applied = []
        self.errors = []

    def apply_improvements(self, improvements: Dict) -> bool:
        """
        Apply improvements from JSON specification.

        Args:
            improvements: Dictionary containing changes to apply

        Returns:
            True if all changes applied successfully, False otherwise
        """
        if not self.target_path.exists():
            self.errors.append(f"Target path does not exist: {self.target_path}")
            return False

        changes = improvements.get('changes', [])
        if not changes:
            self.errors.append("No changes specified in improvements file")
            return False

        # Apply each change
        for change in changes:
            success = self._apply_change(change)
            if not success:
                # Continue applying other changes even if one fails
                continue

        # Report results
        return len(self.errors) == 0

    def _apply_change(self, change: Dict) -> bool:
        """Apply a single change"""
        file_path = self.target_path / change['file']
        change_type = change.get('type', 'edit')

        try:
            if change_type == 'write':
                # Create or overwrite file
                content = change['new_content']
                file_path.write_text(content)
                self.changes_applied.append(f"Wrote {change['file']}")
                return True

            elif change_type == 'edit':
                # Edit existing file
                if not file_path.exists():
                    self.errors.append(f"File not found for editing: {change['file']}")
                    return False

                current_content = file_path.read_text()
                old_content = change['old_content']
                new_content = change['new_content']

                if old_content not in current_content:
                    self.errors.append(
                        f"Old content not found in {change['file']}. "
                        f"Expected to find: {old_content[:100]}..."
                    )
                    return False

                # Replace content
                updated_content = current_content.replace(old_content, new_content, 1)
                file_path.write_text(updated_content)
                self.changes_applied.append(f"Edited {change['file']}")
                return True

            elif change_type == 'append':
                # Append to file
                if not file_path.exists():
                    self.errors.append(f"File not found for appending: {change['file']}")
                    return False

                current_content = file_path.read_text()
                new_content = change['new_content']
                updated_content = current_content + '\n' + new_content
                file_path.write_text(updated_content)
                self.changes_applied.append(f"Appended to {change['file']}")
                return True

            else:
                self.errors.append(f"Unknown change type: {change_type}")
                return False

        except Exception as e:
            self.errors.append(f"Error applying change to {change['file']}: {str(e)}")
            return False

    def print_summary(self):
        """Print summary of changes applied"""
        print("\n=== Improvement Application Summary ===\n")

        if self.changes_applied:
            print("✅ Changes applied:")
            for change in self.changes_applied:
                print(f"   - {change}")
        else:
            print("No changes were applied.")

        if self.errors:
            print("\n❌ Errors encountered:")
            for error in self.errors:
                print(f"   - {error}")
        else:
            print("\n✅ No errors!")


def load_improvements(improvements_path: Path) -> Dict:
    """Load improvements from JSON file"""
    try:
        with improvements_path.open() as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading improvements file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python apply_improvements.py <skill-or-plugin-path> <improvements.json>")
        print("\nExample:")
        print("  python apply_improvements.py .claude/skills/my-skill improvements.json")
        sys.exit(1)

    target_path = Path(sys.argv[1]).resolve()
    improvements_path = Path(sys.argv[2]).resolve()

    if not improvements_path.exists():
        print(f"❌ Error: Improvements file not found: {improvements_path}")
        sys.exit(1)

    # Load improvements
    improvements = load_improvements(improvements_path)

    # Apply improvements
    applicator = ImprovementApplicator(target_path)
    success = applicator.apply_improvements(improvements)

    # Print summary
    applicator.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
