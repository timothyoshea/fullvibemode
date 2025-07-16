#!/usr/bin/env python3
"""
Enhanced post-tool hook with advanced logging and smart notifications
"""
import sys
import json
import os
import subprocess
import platform
from datetime import datetime

def send_notification(title, message, sound="Glass"):
    """Send system notification"""
    if platform.system() == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)

def should_create_checkpoint(tool_name, parameters, exit_code):
    """Determine if we should create a git checkpoint"""
    
    # Create checkpoint after successful file modifications
    if exit_code == 0 and tool_name in ["write", "edit", "multi_edit"]:
        return True
    
    # Create checkpoint after successful builds/installs
    if exit_code == 0 and tool_name == "bash":
        command = parameters.get("command", "")
        checkpoint_triggers = [
            "npm install",
            "pip install", 
            "cargo build",
            "mvn install",
            "git add",
            "npm run build"
        ]
        return any(trigger in command for trigger in checkpoint_triggers)
    
    return False

def create_auto_checkpoint():
    """Create automatic git checkpoint"""
    try:
        # Check if we're in a git repo
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            return  # Not a git repo
        
        # Check if there are changes
        if not result.stdout.strip():
            return  # No changes
        
        # Create checkpoint
        subprocess.run(["git", "add", "."], capture_output=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"""Auto-checkpoint: {timestamp}

Automated commit from Claude Code session

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
        
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
        send_notification("📁 Git Checkpoint", "Auto-saved progress", "Glass")
        
    except Exception:
        pass  # Silently fail if git operations fail

def log_tool_usage(data):
    """Enhanced logging with analytics"""
    
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Enhanced log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": data.get("tool_name", "unknown"),
        "exit_code": data.get("exit_code", None),
        "duration_ms": data.get("duration_ms", 0),
        "success": data.get("exit_code", 0) == 0,
        "parameters": data.get("parameters", {}),
        "session_id": os.environ.get("CLAUDE_SESSION_ID", "unknown")
    }
    
    # Daily log file
    log_file = os.path.join(log_dir, f"usage_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # Update usage statistics
    update_usage_stats(log_entry)

def update_usage_stats(log_entry):
    """Update usage statistics"""
    
    stats_file = os.path.join(os.path.dirname(__file__), '../logs/stats.json')
    
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_tools": 0,
                "successful_tools": 0,
                "tool_counts": {},
                "last_updated": None
            }
        
        # Update stats
        stats["total_tools"] += 1
        if log_entry["success"]:
            stats["successful_tools"] += 1
        
        tool_name = log_entry["tool_name"]
        stats["tool_counts"][tool_name] = stats["tool_counts"].get(tool_name, 0) + 1
        stats["last_updated"] = datetime.now().isoformat()
        
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
            
    except Exception:
        pass  # Silently handle stats errors

def send_contextual_notification(tool_name, parameters, exit_code, duration_ms):
    """Send contextual notifications based on tool usage"""
    
    if exit_code != 0:
        send_notification("❌ Claude Code", f"{tool_name} failed (exit: {exit_code})", "Basso")
        return
    
    # Success notifications for important operations
    if tool_name == "bash":
        command = parameters.get("command", "")
        
        if "npm install" in command:
            send_notification("📦 NPM", "Packages installed successfully", "Glass")
        elif "pip install" in command:
            send_notification("🐍 Python", "Packages installed successfully", "Glass")
        elif "git push" in command:
            send_notification("🚀 Git", "Changes pushed to remote", "Glass")
        elif "npm run build" in command or "cargo build" in command:
            send_notification("🔨 Build", "Build completed successfully", "Glass")
        elif duration_ms > 5000:  # Long-running commands
            send_notification("⏱️ Claude Code", f"Command completed ({duration_ms/1000:.1f}s)", "Glass")
    
    elif tool_name in ["write", "edit", "multi_edit"]:
        file_path = parameters.get("file_path", "")
        if file_path:
            filename = os.path.basename(file_path)
            send_notification("📝 File Updated", filename, "Glass")

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        parameters = data.get("parameters", {})
        exit_code = data.get("exit_code", 0)
        duration_ms = data.get("duration_ms", 0)
        
        # Log tool usage
        log_tool_usage(data)
        
        # Send contextual notifications
        send_contextual_notification(tool_name, parameters, exit_code, duration_ms)
        
        # Create checkpoint if needed
        if should_create_checkpoint(tool_name, parameters, exit_code):
            create_auto_checkpoint()
        
        # Pass through the original data
        print(json.dumps(data))
        
    except Exception as e:
        # Log error but don't fail
        error_data = data if 'data' in locals() else {}
        error_data["hook_error"] = str(e)
        print(json.dumps(error_data))

if __name__ == "__main__":
    main()