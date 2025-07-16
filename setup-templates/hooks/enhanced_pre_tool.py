#!/usr/bin/env python3
"""
Enhanced pre-tool hook with smart validation and notifications
"""
import sys
import json
import re
import subprocess
import platform

def send_notification(title, message, sound="Glass"):
    """Send system notification"""
    if platform.system() == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def validate_command(command, tool_name):
    """Advanced command validation with context awareness"""
    
    # Ultra-safe commands (always allow)
    ultra_safe = [
        r'^ls(\s|$)',
        r'^cat\s+[^|>;&]+$',  # cat with simple file paths
        r'^grep\s+[^|>;&]+$',
        r'^find\s+.*-name',
        r'^git\s+(status|log|diff|show)(\s|$)',
        r'^python.*--help',
        r'^npm\s+(list|info|view)',
        r'^echo\s+',
        r'^pwd$',
        r'^whoami$',
        r'^date$'
    ]
    
    # Development commands (allow with notification)
    dev_commands = [
        r'^git\s+(add|commit|push)',
        r'^npm\s+(install|update|run)',
        r'^pip\s+(install|update)',
        r'^python\s+[^;|>&]+\.py',
        r'^node\s+[^;|>&]+\.js',
        r'^cargo\s+(build|run|test)',
        r'^mvn\s+(compile|test|package)'
    ]
    
    # Potentially dangerous (require extra validation)
    dangerous = [
        r'rm\s.*-rf',
        r'sudo\s',
        r'chmod\s777',
        r'>\s*/dev/',
        r'curl.*\|\s*(sh|bash)',
        r'wget.*\|\s*(sh|bash)',
        r'eval\s',
        r'exec\s'
    ]
    
    # Check ultra-safe first
    for pattern in ultra_safe:
        if re.match(pattern, command):
            return {"ok": True, "level": "safe"}
    
    # Check dangerous patterns
    for pattern in dangerous:
        if re.search(pattern, command):
            send_notification("⚠️ Claude Code", f"Blocked dangerous command: {command[:50]}...", "Basso")
            return {"error": f"Blocked dangerous command: {command}"}
    
    # Check development commands
    for pattern in dev_commands:
        if re.search(pattern, command):
            send_notification("🔧 Claude Code", f"Running: {command[:50]}...", "Glass")
            return {"ok": True, "level": "dev"}
    
    # Default: allow with logging
    return {"ok": True, "level": "standard"}

def validate_file_operation(tool_name, parameters):
    """Validate file operations"""
    
    if tool_name in ["write", "edit", "multi_edit"]:
        file_path = parameters.get("file_path", "")
        
        # Block writing to system directories
        dangerous_paths = ["/etc/", "/usr/", "/var/", "/sys/", "/proc/"]
        for path in dangerous_paths:
            if file_path.startswith(path):
                return {"error": f"Blocked write to system directory: {file_path}"}
        
        # Notify for important file modifications
        important_files = ["package.json", "requirements.txt", "Cargo.toml", ".gitignore"]
        if any(file_path.endswith(f) for f in important_files):
            send_notification("📝 Claude Code", f"Modifying {file_path}", "Glass")
    
    return {"ok": True}

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        parameters = data.get("parameters", {})
        
        # Handle bash commands
        if tool_name == "bash":
            command = parameters.get("command", "")
            if command:
                result = validate_command(command, tool_name)
                print(json.dumps(result))
                if result.get("error"):
                    sys.exit(1)
                return
        
        # Handle file operations
        file_result = validate_file_operation(tool_name, parameters)
        if file_result.get("error"):
            send_notification("⚠️ Claude Code", file_result["error"], "Basso")
            print(json.dumps(file_result))
            sys.exit(1)
        
        # Default: allow operation
        print(json.dumps({"ok": True}))
        
    except Exception as e:
        error_msg = f"Hook error: {str(e)}"
        send_notification("❌ Claude Code", error_msg, "Basso")
        print(json.dumps({"error": error_msg}))
        sys.exit(1)

if __name__ == "__main__":
    main()