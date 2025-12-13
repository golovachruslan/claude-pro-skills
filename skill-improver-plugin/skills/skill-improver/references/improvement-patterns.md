# Skill and Plugin Improvement Patterns

This reference document provides detailed examples of common improvement patterns for Claude Code skills and plugins.

## Table of Contents

1. [Description Improvements](#description-improvements)
2. [Content Enhancements](#content-enhancements)
3. [Script Fixes](#script-fixes)
4. [Metadata Updates](#metadata-updates)
5. [Structural Reorganization](#structural-reorganization)

## Description Improvements

### Pattern: Broadening Trigger Coverage

**Problem**: Skill doesn't trigger when users use alternative phrasing.

**Example Scenario**:
- User says "help me with this spreadsheet" but skill description only mentions "Excel" and "CSV"
- Skill should have triggered but didn't

**Solution**: Add synonyms and alternative phrasings to description.

```yaml
# Before
description: Processes Excel and CSV files with pandas for data analysis.

# After
description: Processes Excel, CSV, and spreadsheet files with pandas for data analysis, visualization, and reporting. Use when users request help with tabular data, spreadsheets, data files (.xlsx, .csv, .xls), or ask to "analyze data", "process spreadsheet", "generate reports", or similar data-related tasks.
```

### Pattern: Adding Context Clues

**Problem**: Skill description is too generic and triggers incorrectly.

**Example Scenario**:
- Generic skill triggers for requests it shouldn't handle
- Needs more specific triggering criteria

**Solution**: Add specific contexts where skill should be used.

```yaml
# Before
description: Helps with document creation and editing.

# After
description: Creates and edits Microsoft Word documents (.docx) with tracked changes, comments, and formatting. Use when users need to work with Word documents specifically - NOT for plain text, markdown, or code files. Triggers include "create Word document", "edit .docx file", "track changes", or "add comments to document".
```

### Pattern: Specifying File Types

**Problem**: Skill description doesn't mention supported file types.

**Example Scenario**:
- User has a .pdf file but skill description doesn't mention PDFs
- Skill either doesn't trigger or triggers incorrectly

**Solution**: Explicitly list supported file extensions.

```yaml
# Before
description: Processes image files for editing and analysis.

# After
description: Processes and edits image files (.jpg, .jpeg, .png, .gif, .bmp, .webp) including resizing, cropping, filtering, format conversion, and metadata extraction. Use when users need image manipulation, photo editing, or image analysis tasks.
```

## Content Enhancements

### Pattern: Adding Concrete Examples

**Problem**: Instructions are abstract; users don't know how to apply them.

**Example Scenario**:
- Skill instructions say "configure the settings" but don't show what settings
- User is confused about what to do

**Solution**: Add concrete examples from actual usage.

```markdown
# Before
## Configuration

Configure the tool settings as needed for your use case.

# After
## Configuration

Configure the tool settings based on your use case:

### Example 1: Simple Data Analysis
```python
config = {
    'input_file': 'data.csv',
    'output_format': 'excel',
    'include_charts': True
}
```

### Example 2: Large Dataset Processing
```python
config = {
    'input_file': 'large_data.csv',
    'chunk_size': 10000,  # Process in chunks
    'parallel': True,
    'output_format': 'parquet'
}
```
```

### Pattern: Adding Error Troubleshooting

**Problem**: Users encounter errors but skill doesn't help troubleshoot.

**Example Scenario**:
- Common error occurs during skill usage
- No guidance on how to fix it

**Solution**: Add troubleshooting section with common errors.

```markdown
## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Cause**: Required dependency not installed.

**Solution**: Install pandas:
```bash
pip install pandas
```

### Error: "PermissionError: [Errno 13] Permission denied"

**Cause**: File is open in another program or insufficient permissions.

**Solution**:
1. Close the file in other applications
2. Check file permissions: `ls -l filename`
3. If needed, change permissions: `chmod 644 filename`
```

### Pattern: Adding Decision Trees

**Problem**: Skill covers multiple scenarios but doesn't guide which to use.

**Example Scenario**:
- Skill has multiple approaches but user doesn't know which to choose
- Results in suboptimal approach selection

**Solution**: Add decision tree or workflow guide.

```markdown
## Workflow Decision Tree

Follow this decision tree to choose the right approach:

1. **What type of document?**
   - Creating new document → See [Creating Documents](#creating-documents)
   - Editing existing document → Continue to step 2

2. **What kind of edits?**
   - Simple text changes → See [Simple Editing](#simple-editing)
   - Tracked changes needed → See [Track Changes Mode](#track-changes-mode)
   - Adding comments → See [Comment Insertion](#comment-insertion)
   - Formatting changes → See [Formatting Guide](#formatting-guide)

3. **Is document password protected?**
   - Yes → See [Protected Documents](#protected-documents)
   - No → Proceed with chosen method from step 2
```

## Script Fixes

### Pattern: Adding Input Validation

**Problem**: Script crashes on invalid input.

**Example Scenario**:
- Script expects a file path but receives a directory
- No validation causes cryptic error

**Solution**: Add input validation with clear error messages.

```python
# Before
def process_file(file_path):
    with open(file_path) as f:
        data = f.read()
    # ... process data

# After
def process_file(file_path):
    """Process a file with validation."""
    # Validate input
    if not file_path:
        raise ValueError("file_path is required")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.is_dir():
        raise ValueError(f"Expected file but got directory: {file_path}")

    if not path.suffix == '.txt':
        raise ValueError(f"Expected .txt file but got: {path.suffix}")

    # Process file
    with open(path) as f:
        data = f.read()
    # ... process data
```

### Pattern: Adding Progress Feedback

**Problem**: Long-running script provides no feedback.

**Example Scenario**:
- Script takes 2 minutes to run
- User doesn't know if it's working or frozen

**Solution**: Add progress indicators.

```python
# Before
def process_files(files):
    results = []
    for file in files:
        result = process_single_file(file)
        results.append(result)
    return results

# After
def process_files(files):
    """Process multiple files with progress feedback."""
    results = []
    total = len(files)

    print(f"Processing {total} files...")

    for i, file in enumerate(files, 1):
        print(f"  [{i}/{total}] Processing {file.name}...", end='')
        result = process_single_file(file)
        results.append(result)
        print(" ✓")

    print(f"\n✅ Completed! Processed {total} files.")
    return results
```

### Pattern: Making Scripts More Configurable

**Problem**: Script has hardcoded values that users need to change.

**Example Scenario**:
- Output format is hardcoded but users want different formats
- Script needs editing for simple changes

**Solution**: Add command-line arguments or configuration.

```python
# Before
def main():
    data = load_data('input.csv')
    processed = process(data)
    save_data(processed, 'output.xlsx')

# After
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process data files')
    parser.add_argument('input_file', help='Input CSV file')
    parser.add_argument('output_file', help='Output file')
    parser.add_argument('--format', choices=['xlsx', 'csv', 'json'],
                       default='xlsx', help='Output format')
    args = parser.parse_args()

    data = load_data(args.input_file)
    processed = process(data)
    save_data(processed, args.output_file, format=args.format)
```

## Metadata Updates

### Pattern: Adding Missing Keywords

**Problem**: Plugin/skill hard to find in marketplace.

**Example Scenario**:
- Users search for "spreadsheet" but plugin keywords only include "excel", "csv"
- Plugin doesn't appear in search results

**Solution**: Add relevant search keywords.

```json
// Before
{
  "name": "data-processor",
  "keywords": ["excel", "csv"]
}

// After
{
  "name": "data-processor",
  "keywords": [
    "excel", "csv", "spreadsheet", "data", "analysis",
    "pandas", "dataframe", "xlsx", "tabular", "statistics"
  ]
}
```

### Pattern: Improving Plugin Description

**Problem**: Plugin description is too technical or unclear.

**Example Scenario**:
- Description uses jargon that users don't understand
- Users don't know what the plugin does

**Solution**: Rewrite for clarity and user benefit.

```json
// Before
{
  "description": "Utilizes pandas DataFrame API for tabular data ETL operations"
}

// After
{
  "description": "Analyze, clean, and transform spreadsheet data (Excel, CSV) with powerful data analysis tools. Perfect for generating statistics, creating reports, and processing large datasets."
}
```

### Pattern: Version Incrementing

**Problem**: Changes made but version not updated.

**Example Scenario**:
- Skill/plugin updated with bug fixes
- Version number still shows old version

**Solution**: Increment version appropriately.

```json
// Versioning guide:
// - Major (1.0.0 → 2.0.0): Breaking changes, complete rewrites
// - Minor (1.0.0 → 1.1.0): New features, significant enhancements
// - Patch (1.0.0 → 1.0.1): Bug fixes, small improvements

// For bug fix:
{
  "version": "1.2.3"  // was 1.2.2
}

// For new feature:
{
  "version": "1.3.0"  // was 1.2.3
}

// For breaking change:
{
  "version": "2.0.0"  // was 1.3.0
}
```

## Structural Reorganization

### Pattern: Splitting Long SKILL.md

**Problem**: SKILL.md is too long and overwhelming.

**Example Scenario**:
- SKILL.md is 1000+ lines
- Most content not relevant to typical use case

**Solution**: Move detailed content to references.

```markdown
# Before: All in SKILL.md (1000+ lines)
## Overview
...
## Basic Usage
...
## Advanced Feature 1
... (100 lines)
## Advanced Feature 2
... (100 lines)
## Advanced Feature 3
... (100 lines)
## API Reference
... (500 lines)

# After: Split across files

## SKILL.md (200 lines)
## Overview
...
## Basic Usage
...
## Advanced Features
For detailed information on advanced features:
- **Feature 1**: See [references/feature1.md](references/feature1.md)
- **Feature 2**: See [references/feature2.md](references/feature2.md)
- **Feature 3**: See [references/feature3.md](references/feature3.md)

## API Reference
See [references/api.md](references/api.md) for complete API documentation.

## references/feature1.md (100 lines)
[Detailed content for feature 1]

## references/feature2.md (100 lines)
[Detailed content for feature 2]

## references/api.md (500 lines)
[Complete API reference]
```

### Pattern: Organizing by Domain

**Problem**: Skill covers multiple unrelated domains in one file.

**Example Scenario**:
- Analytics skill covers finance, sales, and marketing
- Users only need one domain at a time

**Solution**: Organize references by domain.

```
Before structure:
analytics-skill/
└── SKILL.md (covers all domains)

After structure:
analytics-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md (finance-specific queries)
    ├── sales.md (sales-specific queries)
    └── marketing.md (marketing-specific queries)
```

```markdown
# SKILL.md
## Domain-Specific Guides

This skill supports multiple business domains. Load the relevant reference:

- **Finance analytics**: See [references/finance.md](references/finance.md)
  - Revenue metrics, profit analysis, financial forecasting

- **Sales analytics**: See [references/sales.md](references/sales.md)
  - Pipeline metrics, conversion rates, sales forecasting

- **Marketing analytics**: See [references/marketing.md](references/marketing.md)
  - Campaign performance, attribution, ROI analysis
```

### Pattern: Adding Quick Reference Section

**Problem**: Users need to find specific information quickly.

**Example Scenario**:
- Long skill with many commands/functions
- Users can't quickly find what they need

**Solution**: Add quick reference table at top.

```markdown
# Skill Name

## Quick Reference

| Task | Command/Function | Reference |
|------|-----------------|-----------|
| Create new document | `create_doc(title)` | [Creating](#creating) |
| Add heading | `add_heading(text, level)` | [Headings](#headings) |
| Insert table | `insert_table(rows, cols)` | [Tables](#tables) |
| Track changes | Enable with `track=True` | [Track Changes](#track-changes) |
| Save document | `save_doc(path)` | [Saving](#saving) |

## Detailed Documentation

[Rest of the skill content...]
```

## Implementation Checklist

When applying any improvement pattern:

- [ ] Read the current file(s) completely
- [ ] Identify exact sections to modify
- [ ] Create before/after examples
- [ ] Get user approval before changing
- [ ] Use Edit tool with exact string matches
- [ ] Test changes (run scripts, validate YAML)
- [ ] Verify no unintended side effects
- [ ] Document what changed and why
