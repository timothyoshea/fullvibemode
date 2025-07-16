#!/bin/bash

# Global Claude Code Ultra Setup Installer
# This script can be run from anywhere to set up the system

set -e

echo "🚀 Installing Claude Code Ultra Setup System..."

# Detect if we're in the ClaudeResearch repo or need to download
if [[ -f "setup-templates/setup-claude-code.sh" ]]; then
    # We're in the repo
    SETUP_DIR="$(pwd)/setup-templates"
    echo "✅ Using local setup templates"
else
    # Download or clone the setup system
    echo "📥 Setting up global installation..."
    
    # Create global directory
    GLOBAL_DIR="$HOME/.claude-code-ultra"
    mkdir -p "$GLOBAL_DIR"
    
    # Copy or link setup files
    if [[ -d "/Users/timoshea/repos/ClaudeResearch/setup-templates" ]]; then
        cp -r "/Users/timoshea/repos/ClaudeResearch/setup-templates" "$GLOBAL_DIR/"
        SETUP_DIR="$GLOBAL_DIR/setup-templates"
        echo "✅ Copied setup templates to $GLOBAL_DIR"
    else
        echo "❌ Could not find setup templates. Please run from ClaudeResearch repo or provide path."
        exit 1
    fi
fi

# Make scripts executable
chmod +x "$SETUP_DIR"/*.sh
chmod +x "$SETUP_DIR"/scripts/*.py
chmod +x "$SETUP_DIR"/hooks/*.py

# Add to shell profile for global access
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]] && [[ -f "$SHELL_RC" ]]; then
    # Check if alias already exists
    if ! grep -q "claude-setup" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# Claude Code Ultra Setup" >> "$SHELL_RC"
        echo "alias claude-setup='$SETUP_DIR/setup-claude-code.sh'" >> "$SHELL_RC"
        echo "✅ Added 'claude-setup' alias to $SHELL_RC"
        echo "💡 Run 'source $SHELL_RC' or restart your terminal to use the alias"
    else
        echo "✅ 'claude-setup' alias already exists"
    fi
fi

# Create desktop shortcut on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    DESKTOP_APP="$HOME/Desktop/Claude Setup.app"
    if [[ ! -d "$DESKTOP_APP" ]]; then
        mkdir -p "$DESKTOP_APP/Contents/MacOS"
        
        cat > "$DESKTOP_APP/Contents/MacOS/claude-setup" << EOF
#!/bin/bash
cd "\$(dirname "\$0")/../../../"
open -a Terminal "$SETUP_DIR/setup-claude-code.sh"
EOF
        chmod +x "$DESKTOP_APP/Contents/MacOS/claude-setup"
        
        cat > "$DESKTOP_APP/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Claude Setup</string>
    <key>CFBundleExecutable</key>
    <string>claude-setup</string>
    <key>CFBundleIdentifier</key>
    <string>com.claude.setup</string>
</dict>
</plist>
EOF
        echo "✅ Created desktop app: Claude Setup.app"
    fi
fi

echo ""
echo "🎉 Installation Complete!"
echo ""
echo "Usage options:"
echo "1. Command line: claude-setup (if you reloaded shell)"
echo "2. Direct path: $SETUP_DIR/setup-claude-code.sh"
echo "3. In any directory: $SETUP_DIR/setup-claude-code.sh ."
echo ""
echo "Quick test:"
echo "  cd /tmp && mkdir test-claude && cd test-claude"
echo "  claude-setup"
echo ""
echo "🚀 Ready to supercharge your Claude Code projects!"