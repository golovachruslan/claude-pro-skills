# setup.yaml Format Reference

## Schema

```yaml
marketplaces:
  - <source>       # GitHub slug or URL for `claude plugin marketplace add`

plugins:
  - <name>@<marketplace>   # Plugin name and marketplace identifier
```

## Fields

### `marketplaces`

A list of marketplace sources. Each entry is passed directly to `claude plugin marketplace add <source>`.

Supported formats:
- **GitHub slug**: `owner/repo` (e.g., `anthropics/claude-plugins-official`)
- **Git URL with sparse checkout**: `https://github.com/owner/repo.git --sparse <path> <name>`

### `plugins`

A list of plugins to install and enable. Each entry uses the format `plugin-name@marketplace-name`, where:
- `plugin-name` is the plugin identifier within the marketplace
- `marketplace-name` is the short name of the marketplace (typically the repo name)

Comments (`#`) can be used to group plugins by marketplace for readability.

## Example

```yaml
marketplaces:
  - anthropics/claude-plugins-official
  - golovachruslan/claude-pro-skills
  - https://github.com/anthropics/claude-code.git --sparse .claude-plugin plugins

plugins:
  # claude-plugins-official
  - playwright@claude-plugins-official
  - plugin-dev@claude-plugins-official
  - hookify@claude-plugins-official

  # claude-pro-skills
  - skills-improver@claude-pro-skills
  - project-context@claude-pro-skills
```

## Notes

- The `setup.sh` script parses this file using simple `sed`/`grep` — no YAML library required.
- Inline comments after list items are stripped automatically.
- Blank lines and comment-only lines within a section are ignored.
- The marketplace short name used in `name@marketplace` is typically the last segment of the GitHub slug (e.g., `claude-plugins-official` from `anthropics/claude-plugins-official`).
