# agent-config

Configure Claude Code plugin ecosystems for projects — generates `setup.yaml`, `setup.sh`, and a SessionStart hook so teammates get all plugins automatically.

## Features

- **Interactive setup**: Walks you through selecting marketplaces and plugins
- **SessionStart hook**: Automatically runs `setup.sh` when a Claude Code session starts
- **Idempotent**: `setup.sh` uses a `.setup-done` marker to avoid re-running; use `--force` to override
- **Dry-run support**: Preview commands with `bash setup.sh --dry-run`

## Installation

```bash
# Add the marketplace
claude plugin marketplace add golovachruslan/claude-pro-skills

# Install the plugin
claude plugin install agent-config@claude-pro-skills
```

## Usage

Run the slash command in Claude Code:

```
/agent-config:agent-setup
```

Or describe what you want:

> "Set up plugin ecosystem for this project"

The skill will:
1. Ask for your target directory
2. Collect marketplace sources
3. Collect plugins to install
4. Generate `setup.yaml` with your configuration
5. Copy `setup.sh` to the target
6. Add a SessionStart hook to `.claude/settings.json`

## Generated Files

| File | Purpose |
|------|---------|
| `setup.yaml` | Plugin ecosystem configuration |
| `setup.sh` | Installs marketplaces & plugins from setup.yaml |
| `.claude/settings.json` | SessionStart hook for automatic setup |

## setup.sh Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview commands without executing |
| `--force` | Re-run even if `.setup-done` marker exists |

## License

MIT
