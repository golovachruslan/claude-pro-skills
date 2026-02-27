# CI/CD & Automation

## GitHub Workflows

**`.github/workflows/claude.yml`** - Interactive Claude Code execution:
- Triggers on issue comments, PR reviews, issue creation
- Requires "@claude" mention in comments
- Executes custom prompts via `anthropics/claude-code-action@v1`

**`.github/workflows/claude-code-review.yml`** - Automated PR reviews:
- Triggers on PR open/synchronize
- Evaluates: code quality, bugs, performance, security, test coverage
- Posts review comments via gh CLI
- References CLAUDE.md for style guidance
