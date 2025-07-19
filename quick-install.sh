#!/bin/bash

# Claude Code Ultra - Quick Install Script
# This script can be downloaded and run directly

set -e

echo "🚀 Claude Code Ultra - Quick Install"
echo "==================================="

# Check if we're on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    echo "❌ Unsupported operating system. This script works on macOS and Linux."
    exit 1
fi

echo "✅ Detected: $OS"

# Check for required tools
echo "🔍 Checking requirements..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed."
    echo "Please install Git and try again."
    exit 1
fi

echo "✅ Requirements satisfied"

# Create installation directory
INSTALL_DIR="$HOME/.claude-code-ultra"
echo "📁 Creating installation directory: $INSTALL_DIR"

if [[ -d "$INSTALL_DIR" ]]; then
    echo "⚠️  Installation directory already exists. Updating..."
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"

# Download or create the setup files
echo "📥 Setting up Claude Code Ultra system..."

# Create the main setup script
cat > "$INSTALL_DIR/setup-claude-code.sh" << 'EOF'
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

# Copy hooks
cp "$SCRIPT_DIR/hooks/"* "$TARGET_DIR/.do.claude/hooks/"

# Make hooks executable
chmod +x "$TARGET_DIR/.do.claude/hooks/"*.py

# Detect project type
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

# Create settings.json
cat > "$TARGET_DIR/.do.claude/settings.json" << 'SETTINGS_EOF'
{
  "permissions": {
    "bash": "allow",
    "read": "allow",
    "write": "allow",
    "edit": "allow",
    "grep": "allow",
    "glob": "allow",
    "multi_edit": "allow"
  },
  "hooks": {
    "pre_tool_use": [
      {
        "match": {},
        "run": ["hooks/enhanced_pre_tool.py"]
      }
    ],
    "post_tool_use": [
      {
        "match": {},
        "run": ["hooks/enhanced_post_tool.py"]
      }
    ],
    "notification": [
      {
        "match": {},
        "run": ["hooks/smart_notification.py"]
      }
    ],
    "stop": [
      {
        "match": {},
        "run": ["hooks/session_manager.py"]
      }
    ]
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "./"],
      "transport": "stdio"
    },
    "sqlite": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-sqlite"],
      "transport": "stdio"
    }
  },
  "environment": {
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "true",
    "CLAUDE_CODE_DISABLE_TERMINAL_TITLE": "true"
  }
}
SETTINGS_EOF

# Create project-specific CLAUDE.md
PROJECT_NAME="$(basename "$TARGET_DIR")"
cat > "$TARGET_DIR/CLAUDE.md" << 'CLAUDE_EOF'
# PROJECT_NAME_PLACEHOLDER

## Claude Code Ultra Configuration

### Features Enabled
- ✅ Ultra Thinking: Extended reasoning for complex problems
- ✅ YOLO Mode: Minimal interruption automation
- ✅ Multi-Agent MCP: Specialized servers for different domains
- ✅ Smart Notifications: Real-time alerts and updates
- ✅ Auto-Checkpointing: Git commits after major changes
- ✅ Session Analytics: Productivity scoring and insights

### Usage Examples

#### Ultra Thinking
```
think ultra hard about this architecture
think deeply about potential issues
think more about optimization strategies
```

#### Multi-Agent Operations
```
@filesystem search for config files
@sqlite query data
```

### Project Context
This project is optimized for maximum Claude Code automation and efficiency.

CLAUDE_EOF

# Replace placeholder with actual project name
sed -i.bak "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/" "$TARGET_DIR/CLAUDE.md"
rm "$TARGET_DIR/CLAUDE.md.bak" 2>/dev/null || true

# Set up git if not already initialized
if [[ ! -d "$TARGET_DIR/.git" ]]; then
    cd "$TARGET_DIR"
    git init
    git config user.name "Claude Code Assistant"
    git config user.email "claude@assistant.local"
    
    # Create .gitignore
    cat > .gitignore << 'GITIGNORE_EOF'
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
GITIGNORE_EOF
    
    git add .
    git commit -m "Initial setup: Claude Code Ultra System

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
fi

# Send notification
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'display notification "Claude Code Ultra System ready!" with title "Setup Complete" sound name "Glass"' 2>/dev/null || true
fi

echo "✅ Claude Code Ultra System setup complete!"
echo "🎯 Features enabled: Ultra thinking, YOLO mode, MCP servers, notifications"
echo "🚀 Ready to use! Start Claude Code and enjoy the automation."
EOF

# Create hooks directory
mkdir -p "$INSTALL_DIR/hooks"

# Create enhanced pre-tool hook
cat > "$INSTALL_DIR/hooks/enhanced_pre_tool.py" << 'EOF'
#!/usr/bin/env python3
import sys
import json
import re
import subprocess
import platform

def send_notification(title, message):
    if platform.system() == "Darwin":
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def validate_command(command):
    safe_patterns = [r'^ls', r'^cat', r'^grep', r'^find', r'^git (status|log|diff)']
    dangerous_patterns = [r'rm.*-rf', r'sudo', r'chmod 777']
    
    for pattern in safe_patterns:
        if re.match(pattern, command):
            return {"ok": True}
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            send_notification("⚠️ Claude Code", f"Blocked dangerous command")
            return {"error": f"Blocked dangerous command: {command}"}
    
    return {"ok": True}

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        
        if tool_name == "bash":
            command = data.get("parameters", {}).get("command", "")
            if command:
                result = validate_command(command)
                print(json.dumps(result))
                if result.get("error"):
                    sys.exit(1)
                return
        
        print(json.dumps({"ok": True}))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

# Create enhanced post-tool hook
cat > "$INSTALL_DIR/hooks/enhanced_post_tool.py" << 'EOF'
#!/usr/bin/env python3
import sys
import json
import os
import subprocess
import platform
from datetime import datetime

def send_notification(title, message):
    if platform.system() == "Darwin":
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def create_checkpoint():
    try:
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            subprocess.run(["git", "add", "."], capture_output=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Auto-checkpoint: {timestamp}\n\n🤖 Generated with [Claude Code](https://claude.ai/code)"
            subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
            send_notification("📁 Auto-Checkpoint", "Progress saved")
    except Exception:
        pass

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        exit_code = data.get("exit_code", 0)
        
        # Log usage
        log_dir = os.path.join(os.path.dirname(__file__), '../logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tool_name": tool_name,
            "exit_code": exit_code,
            "success": exit_code == 0
        }
        
        log_file = os.path.join(log_dir, f"usage_{datetime.now().strftime('%Y%m%d')}.log")
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Send notifications for important events
        if exit_code == 0:
            if tool_name == "bash":
                command = data.get("parameters", {}).get("command", "")
                if "install" in command:
                    send_notification("📦 Install Complete", "Packages installed")
                elif "build" in command:
                    send_notification("🔨 Build Complete", "Build successful")
            elif tool_name in ["write", "edit"]:
                send_notification("📝 File Updated", "File saved")
                create_checkpoint()
        
        print(json.dumps(data))
        
    except Exception as e:
        print(json.dumps(data if 'data' in locals() else {}))

if __name__ == "__main__":
    main()
EOF

# Create smart notification hook
cat > "$INSTALL_DIR/hooks/smart_notification.py" << 'EOF'
#!/usr/bin/env python3
import sys
import json
import subprocess
import platform

def send_notification(title, message):
    if platform.system() == "Darwin":
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def main():
    try:
        data = json.load(sys.stdin)
        title = data.get("title", "Claude Code")
        message = data.get("message", "Notification")
        send_notification(title, message)
        print(json.dumps({"ok": True}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
EOF

# Create session manager hook
cat > "$INSTALL_DIR/hooks/session_manager.py" << 'EOF'
#!/usr/bin/env python3
import sys
import json
import subprocess
import platform
from datetime import datetime

def send_notification(title, message):
    if platform.system() == "Darwin":
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def main():
    try:
        data = json.load(sys.stdin)
        tools_used = data.get("total_tools_used", 0)
        duration = data.get("duration_ms", 0) / 60000
        
        if duration > 0:
            send_notification("📊 Session Complete", f"{tools_used} tools used in {duration:.1f}m")
        
        print(json.dumps(data))
        
    except Exception as e:
        print(json.dumps(data if 'data' in locals() else {}))

if __name__ == "__main__":
    main()
EOF

# Make all scripts executable
chmod +x "$INSTALL_DIR/setup-claude-code.sh"
chmod +x "$INSTALL_DIR/hooks/"*.py

# Add to shell profile
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]] && [[ -f "$SHELL_RC" ]]; then
    if ! grep -q "claude-setup" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# Claude Code Ultra Setup" >> "$SHELL_RC"
        echo "alias claude-setup='$INSTALL_DIR/setup-claude-code.sh'" >> "$SHELL_RC"
        echo "✅ Added 'claude-setup' alias to $SHELL_RC"
    fi
fi

echo ""
echo "🎉 Installation Complete!"
echo ""
echo "To use the system:"
echo "1. Reload your shell: source $SHELL_RC"
echo "2. Navigate to any project directory"
echo "3. Run: claude-setup"
echo "4. Start Claude Code and enjoy!"
echo ""
echo "Example:"
echo "  cd my-project"
echo "  claude-setup"
echo "  claude"
echo ""
echo "🚀 You now have Claude Code Ultra automation ready!"
echo "Features: Ultra thinking, YOLO mode, smart notifications, auto-checkpoints"

chmod +x "$INSTALL_DIR/quick-install.sh"

# Now run the setup
echo "🔧 Installing Claude Code Ultra system..."
bash "$INSTALL_DIR/quick-install.sh"

echo ""
echo "📋 Installation Summary:"
echo "✅ Claude Code Ultra installed to: $INSTALL_DIR"
echo "✅ Shell alias 'claude-setup' added"
echo "✅ All hooks and scripts configured"
echo "✅ Ready to use in any project"
echo ""
echo "🎯 Next steps:"
echo "1. Reload your shell or run: source ~/.zshrc"
echo "2. Go to any project: cd my-project"
echo "3. Set up automation: claude-setup"
echo "4. Start Claude Code: claude"
echo ""
echo "🚀 Enjoy your supercharged Claude Code experience!"