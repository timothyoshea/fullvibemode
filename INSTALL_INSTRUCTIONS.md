# FullVibeMode - Claude Code Ultra Setup

## 🚀 One-Command Installation

### Option 1: Direct Download & Install
```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/timothyoshea/fullvibemode/main/quick-install.sh | bash
```

### Option 2: Clone and Install
```bash
# Clone the repository
git clone https://github.com/timothyoshea/fullvibemode.git
cd fullvibemode

# Run the installer
./install.sh
```

### Option 3: Manual Download
1. Download the entire `ClaudeResearch` repository as a ZIP
2. Extract it anywhere on your system
3. Open Terminal and navigate to the extracted folder
4. Run: `./install.sh`

## What the Installation Does

### ✅ Global Setup
- Installs the setup system to `~/.claude-code-ultra/`
- Adds `claude-setup` command to your shell profile
- Creates a desktop app (macOS) for easy access
- Makes all scripts executable

### ✅ Shell Integration
Adds this to your `~/.zshrc` or `~/.bashrc`:
```bash
# Claude Code Ultra Setup
alias claude-setup='~/.claude-code-ultra/setup-templates/setup-claude-code.sh'
```

## Using the System

### In Any New Project
```bash
# Navigate to your project
cd my-new-project

# Set up Claude Code Ultra
claude-setup

# Start Claude Code
claude
```

### What You Get Instantly
- **YOLO Mode**: Minimal interruption automation
- **Ultra Thinking**: Extended reasoning with `think ultra hard`
- **Multi-Agent MCP**: Specialized servers for your project type
- **Smart Notifications**: Real-time macOS alerts
- **Auto-Checkpointing**: Git commits after major changes
- **Session Analytics**: Productivity scoring and insights

## Project Types Supported

### Node.js Projects
- NPM integration and package management
- Build tool automation
- Filesystem and GitHub MCP servers

### Python Projects
- Pip integration and virtual environment support
- Python-specific tooling
- Database and filesystem access

### Rust Projects
- Cargo integration
- Build and test automation
- Rust-specific configurations

### Java Projects
- Maven integration
- Build lifecycle automation
- Enterprise-grade configurations

### Generic Projects
- Universal MCP servers
- Git integration
- Basic automation hooks

## Features You'll Experience

### 🔔 Smart Notifications
- `📦 NPM: Packages installed successfully`
- `🔨 Build: Build completed successfully`
- `📝 File Updated: filename.js`
- `⚠️ Blocked dangerous command`
- `📁 Auto-Checkpoint: Progress saved`
- `📊 Session Complete: 25 tools in 12.5m`

### 🤖 Ultra Thinking
```
think ultra hard about this architecture
think deeply about potential issues
think more about optimization strategies
```

### 🌐 Multi-Agent Operations
```
@filesystem search for config files
@github create pull request
@sqlite query user data
@npm install dependencies
```

### 📊 Session Analytics
- Productivity scoring
- Tool usage patterns
- Automation efficiency metrics
- Session history tracking

## Directory Structure Created

```
your-project/
├── .do.claude/
│   ├── hooks/
│   │   ├── enhanced_pre_tool.py     # Smart validation
│   │   ├── enhanced_post_tool.py    # Logging + checkpoints
│   │   ├── smart_notification.py    # Notifications
│   │   └── session_manager.py       # Analytics
│   ├── logs/                        # Usage logs
│   └── settings.json               # Configuration
├── CLAUDE.md                       # Project context
└── .gitignore                      # Optimized ignores
```

## Troubleshooting

### Installation Issues
```bash
# Check if installed correctly
which claude-setup

# Reload your shell
source ~/.zshrc  # or ~/.bashrc

# Test in a new directory
mkdir test-claude && cd test-claude
claude-setup
```

### Permission Issues
```bash
# Make scripts executable
chmod +x ~/.claude-code-ultra/setup-templates/*.sh
chmod +x ~/.claude-code-ultra/setup-templates/scripts/*.py
chmod +x ~/.claude-code-ultra/setup-templates/hooks/*.py
```

### Notification Issues
- Check macOS notification permissions for Terminal
- Verify Python 3 is installed: `python3 --version`
- Test notifications manually from hooks

## Customization

### Add Your Own MCP Servers
Edit the generated `.do.claude/settings.json`:
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

### Modify Automation Level
Edit `.do.claude/hooks/enhanced_pre_tool.py` to adjust:
- Command validation rules
- Safety checks
- Auto-approval patterns

### Customize Notifications
Edit `.do.claude/hooks/smart_notification.py` to change:
- Notification triggers
- Message formats
- Sound choices

## System Requirements

### Required
- macOS (for notifications) or Linux
- Python 3.6+
- Git
- Terminal with bash/zsh

### Optional
- Node.js + npm (for Node projects)
- Python + pip (for Python projects)
- Rust + cargo (for Rust projects)
- Java + Maven (for Java projects)

## Getting Started

1. **Install**: Run the installation command above
2. **Test**: Create a new directory and run `claude-setup`
3. **Use**: Start Claude Code and enjoy full automation
4. **Explore**: Try ultra thinking and multi-agent features
5. **Customize**: Adjust settings for your workflow

## Support

If you encounter issues:
1. Check the installation completed successfully
2. Verify all scripts are executable
3. Check `.do.claude/logs/` for error messages
4. Reload your shell profile
5. Test with a fresh directory

## What Makes This Special

- **Zero Configuration**: Works out of the box
- **Project Aware**: Automatically configures for your tech stack
- **Intelligent**: Learns from your usage patterns
- **Safe**: Blocks dangerous commands automatically
- **Productive**: Provides real-time feedback and analytics
- **Extensible**: Easy to customize and expand

Enjoy your supercharged Claude Code experience! 🚀