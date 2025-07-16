#!/bin/bash

# Claude Code Ultra Setup Script
# Sets up complete Claude Code automation system in any directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$(pwd)}"

echo "🚀 Setting up Claude Code Ultra System in: $TARGET_DIR"

# Create directory structure
mkdir -p "$TARGET_DIR/.do.claude/hooks"
mkdir -p "$TARGET_DIR/.do.claude/logs"
mkdir -p "$TARGET_DIR/research"

# Copy enhanced hooks
cp "$SCRIPT_DIR/hooks/"* "$TARGET_DIR/.do.claude/hooks/"

# Make hooks executable
chmod +x "$TARGET_DIR/.do.claude/hooks/"*.py

# Detect project type and create appropriate settings
PROJECT_TYPE="generic"
if [[ -f "$TARGET_DIR/package.json" ]]; then
    PROJECT_TYPE="node"
elif [[ -f "$TARGET_DIR/requirements.txt" ]] || [[ -f "$TARGET_DIR/pyproject.toml" ]]; then
    PROJECT_TYPE="python"
elif [[ -f "$TARGET_DIR/Cargo.toml" ]]; then
    PROJECT_TYPE="rust"
elif [[ -f "$TARGET_DIR/pom.xml" ]]; then
    PROJECT_TYPE="java"
fi

# Generate settings based on project type
python3 "$SCRIPT_DIR/scripts/generate-settings.py" "$PROJECT_TYPE" > "$TARGET_DIR/.do.claude/settings.json"

# Generate project-specific CLAUDE.md
python3 "$SCRIPT_DIR/scripts/generate-claude-md.py" "$TARGET_DIR" "$PROJECT_TYPE" > "$TARGET_DIR/CLAUDE.md"

# Set up git if not already initialized
if [[ ! -d "$TARGET_DIR/.git" ]]; then
    cd "$TARGET_DIR"
    git init
    git config user.name "Claude Code Assistant"
    git config user.email "claude@assistant.local"
    
    # Create comprehensive .gitignore
    cat > .gitignore << 'EOF'
# Claude Code
.do.claude/logs/
*.log

# Dependencies
node_modules/
venv/
env/
__pycache__/
target/
build/
dist/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.temp
.tmp/
EOF
    
    git add .
    git commit -m "Initial setup: Claude Code Ultra System

Complete automation system with:
- Ultra thinking capabilities
- Multi-agent MCP configuration
- Advanced hooks with notifications
- YOLO mode for minimal interruption
- Automated logging and checkpointing

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
fi

# Install MCP servers if needed
if [[ "$PROJECT_TYPE" == "node" ]] && command -v npm &> /dev/null; then
    echo "📦 Installing MCP servers..."
    npm install -g @modelcontextprotocol/server-filesystem
    npm install -g @modelcontextprotocol/server-sqlite
fi

# Send setup complete notification
osascript -e 'display notification "Claude Code Ultra System ready!" with title "Setup Complete" sound name "Glass"'

echo "✅ Claude Code Ultra System setup complete!"
echo "🎯 Features enabled:"
echo "   • Ultra thinking modes"
echo "   • Multi-agent MCP servers"
echo "   • YOLO mode automation"
echo "   • Smart notifications"
echo "   • Automated logging"
echo "   • Git checkpointing"
echo ""
echo "🚀 Ready to use! Start Claude Code and enjoy the automation."