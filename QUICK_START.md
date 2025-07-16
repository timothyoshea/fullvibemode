# 🚀 Claude Code Ultra Setup - Quick Start

## One-Command Setup

To instantly set up the complete Claude Code automation system in any new repository:

```bash
# From anywhere on your system:
curl -s https://raw.githubusercontent.com/your-repo/claude-research/main/setup-templates/setup-claude-code.sh | bash

# Or if you have this repo locally:
/path/to/ClaudeResearch/setup-templates/setup-claude-code.sh
```

## What You Get Instantly

### ✅ Complete Automation System
- **YOLO Mode**: Minimal interruption, maximum automation
- **Ultra Thinking**: Extended reasoning for complex problems
- **Multi-Agent MCP**: Specialized servers for different domains
- **Smart Notifications**: Real-time macOS notifications
- **Auto-Logging**: Comprehensive usage analytics
- **Git Checkpointing**: Automatic progress saves

### ✅ Enhanced Hooks
- **Smart Validation**: Context-aware command safety
- **Progress Tracking**: Detailed session analytics
- **Auto-Checkpoints**: Git commits after major changes
- **Error Handling**: Graceful failure management

### ✅ Project Detection
- **Node.js**: NPM integration, build tools
- **Python**: Pip integration, virtual environments
- **Rust**: Cargo integration
- **Java**: Maven integration
- **Generic**: Universal tools and patterns

## Usage Examples

### Ultra Thinking
```
think ultra hard about this architecture
think deeply about potential issues
think more about optimization strategies
```

### Multi-Agent Operations
```
@filesystem search for config files
@github create pull request
@sqlite query user data
@npm install dependencies
```

### Smart Notifications
- 🔧 Development actions (installs, builds)
- 📝 File modifications
- ⚠️ Blocked dangerous commands
- 📁 Auto-checkpoints created
- 📊 Session summaries

## Directory Structure Created

```
your-project/
├── .do.claude/
│   ├── hooks/
│   │   ├── enhanced_pre_tool.py     # Smart command validation
│   │   ├── enhanced_post_tool.py    # Advanced logging + checkpoints
│   │   ├── smart_notification.py    # Contextual notifications
│   │   └── session_manager.py       # Session analytics
│   ├── logs/                        # Usage logs and analytics
│   └── settings.json               # Complete configuration
├── CLAUDE.md                       # Project-specific context
└── .gitignore                      # Optimized for Claude Code
```

## Configuration Examples

### For Maximum Automation (YOLO Mode)
```json
{
  "permissions": {
    "bash": "allow",
    "write": "allow",
    "edit": "allow",
    "read": "allow"
  }
}
```

### For Development Safety
```json
{
  "permissions": {
    "bash": "approve",
    "write": "allow",
    "edit": "allow",
    "read": "allow"
  }
}
```

## Notifications You'll See

### 🔧 Development Actions
- `📦 NPM: Packages installed successfully`
- `🔨 Build: Build completed successfully`
- `🚀 Git: Changes pushed to remote`

### 📝 File Operations
- `📝 File Updated: filename.js`
- `⚠️ Claude Code: Blocked dangerous command`

### 📁 Auto-Checkpoints
- `📁 Auto-Checkpoint: Progress saved to git`
- `📊 Session Complete: 25 tools in 12.5m`

## Advanced Features

### Session Analytics
- Productivity scoring
- Tool usage patterns
- Automation efficiency metrics
- Session history tracking

### Smart Command Validation
- Ultra-safe commands: Always allowed
- Development commands: Allowed with notifications
- Dangerous commands: Blocked with alerts

### Auto-Checkpointing
- After successful file modifications
- After builds and installations
- Session end checkpoints
- Descriptive commit messages

## Customization

### Add Custom MCP Servers
Edit `.do.claude/settings.json`:
```json
{
  "mcpServers": {
    "your-server": {
      "command": "your-command",
      "args": ["arg1", "arg2"],
      "transport": "stdio"
    }
  }
}
```

### Modify Notification Behavior
Edit `.do.claude/hooks/smart_notification.py` to customize:
- Notification conditions
- Message formats
- Sound choices
- Urgency levels

### Adjust Automation Level
Edit `.do.claude/hooks/enhanced_pre_tool.py` to modify:
- Command validation rules
- Safety checks
- Auto-approval patterns

## Troubleshooting

### No Notifications?
- Check macOS notification permissions
- Verify hooks are executable: `chmod +x .do.claude/hooks/*.py`

### Hooks Not Working?
- Check `.do.claude/logs/` for error messages
- Verify Python 3 is available
- Test individual hooks manually

### Git Issues?
- Ensure git is initialized: `git init`
- Check git config: `git config --list`
- Verify write permissions

## Global Installation

To use this system globally, add to your shell profile:

```bash
# Add to ~/.zshrc or ~/.bashrc
alias claude-setup='/path/to/ClaudeResearch/setup-templates/setup-claude-code.sh'

# Then use anywhere:
cd my-new-project
claude-setup
```

## What's Next?

1. **Start Claude Code** in your set-up directory
2. **Test ultra thinking**: `think harder about this problem`
3. **Use MCP servers**: `@filesystem search for files`
4. **Enjoy notifications**: Watch for real-time updates
5. **Check logs**: Review `.do.claude/logs/` for analytics

The system learns and improves with each session, providing increasingly intelligent automation and insights.

## Support

If you encounter issues:
1. Check `.do.claude/logs/` for error messages
2. Verify all hooks are executable
3. Test individual components
4. Check the main research documentation

Ready to supercharge your Claude Code experience! 🚀