# claude-pro-skills

Claude Pro Skills - A collection of Claude Code plugins and skills for productivity and development.

## Marketplace

This repository is configured as a Claude Code plugin marketplace. You can add it to your Claude Code environment and install plugins from it.

### Adding the Marketplace

To add this marketplace to your Claude Code environment, use one of the following methods:

**From GitHub:**
```bash
/plugin marketplace add golovachruslan/claude-pro-skills
```

**From Git URL:**
```bash
/plugin marketplace add https://github.com/golovachruslan/claude-pro-skills.git
```

**From Local Directory:**
```bash
/plugin marketplace add ./path/to/claude-pro-skills
```

**From Direct URL:**
```bash
/plugin marketplace add https://raw.githubusercontent.com/golovachruslan/claude-pro-skills/main/.claude-plugin/marketplace.json
```

### Installing Plugins

After adding the marketplace, you can install plugins:

```bash
/plugin install skills-improver@claude-pro-skills
```

Or browse available plugins interactively:
```bash
/plugin
```

### Verifying the Marketplace

List all added marketplaces:
```bash
/plugin marketplace list
```

## Available Plugins

### skills-improver

Automatically analyze conversation history and improve your Claude Code skills and plugins based on user feedback and real usage patterns.

**Installation:**
```bash
/plugin install skills-improver@claude-pro-skills
```

**Features:**
- Conversation analysis with feedback extraction
- Smart improvement proposals
- Safe implementation with user approval
- Comprehensive improvement workflows

See [skills-improver-plugin/README.md](skills-improver-plugin/README.md) for more details.

## Repository Structure

```
claude-pro-skills/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace configuration
├── skills-improver-plugin/   # Skills Improver plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/
│   ├── skills/
│   └── README.md
└── README.md
```

## Contributing

Contributions are welcome! Please ensure any new plugins follow the Claude Code plugin structure and are added to the marketplace.json file.

## License

MIT License - see LICENSE file for details.
