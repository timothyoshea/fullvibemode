#!/usr/bin/env python3
"""
Smart notification hook for Claude Code events
"""
import sys
import json
import subprocess
import platform
import os
from datetime import datetime

def send_notification(title, message, sound="Glass", urgent=False):
    """Send system notification with platform detection"""
    
    if platform.system() == "Darwin":  # macOS
        urgency = "critical" if urgent else "normal"
        script = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)
        
    elif platform.system() == "Linux":
        urgency = "critical" if urgent else "normal"
        try:
            subprocess.run([
                "notify-send",
                f"--urgency={urgency}",
                title,
                message
            ], capture_output=True)
        except FileNotFoundError:
            pass  # notify-send not available
    
    # Log notification
    log_notification(title, message, urgent)

def log_notification(title, message, urgent):
    """Log notifications for debugging"""
    
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "message": message,
        "urgent": urgent,
        "type": "notification"
    }
    
    log_file = os.path.join(log_dir, f"notifications_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def handle_session_events(data):
    """Handle session-level events"""
    
    event_type = data.get("event_type", "")
    
    if event_type == "session_start":
        send_notification("🚀 Claude Code", "Session started - Ultra mode active", "Glass")
    
    elif event_type == "session_end":
        duration = data.get("duration_ms", 0)
        tools_used = data.get("total_tools_used", 0)
        
        if duration > 0:
            duration_min = duration / 60000
            send_notification(
                "👋 Claude Code", 
                f"Session ended: {tools_used} tools used in {duration_min:.1f}m",
                "Glass"
            )
    
    elif event_type == "error":
        error_msg = data.get("message", "Unknown error")
        send_notification("❌ Claude Code Error", error_msg, "Basso", urgent=True)
    
    elif event_type == "warning":
        warning_msg = data.get("message", "Unknown warning")
        send_notification("⚠️ Claude Code Warning", warning_msg, "Funk")

def handle_progress_events(data):
    """Handle progress and milestone events"""
    
    event_type = data.get("event_type", "")
    
    if event_type == "checkpoint_created":
        send_notification("📁 Auto-Checkpoint", "Progress saved to git", "Glass")
    
    elif event_type == "build_complete":
        success = data.get("success", False)
        if success:
            send_notification("✅ Build Success", "Build completed successfully", "Glass")
        else:
            send_notification("❌ Build Failed", "Build failed - check logs", "Basso", urgent=True)
    
    elif event_type == "tests_complete":
        passed = data.get("passed", 0)
        failed = data.get("failed", 0)
        
        if failed == 0:
            send_notification("✅ Tests Passed", f"All {passed} tests passed", "Glass")
        else:
            send_notification("❌ Tests Failed", f"{failed} tests failed", "Basso", urgent=True)

def handle_automation_events(data):
    """Handle automation-specific events"""
    
    event_type = data.get("event_type", "")
    
    if event_type == "auto_fix_applied":
        fix_type = data.get("fix_type", "unknown")
        send_notification("🔧 Auto-Fix", f"Applied {fix_type} fix", "Glass")
    
    elif event_type == "permission_blocked":
        operation = data.get("operation", "unknown")
        send_notification("🛡️ Security", f"Blocked {operation} operation", "Funk")
    
    elif event_type == "batch_complete":
        count = data.get("operations", 0)
        send_notification("⚡ Batch Complete", f"{count} operations completed", "Glass")

def main():
    try:
        data = json.load(sys.stdin)
        
        # Handle different event types
        event_type = data.get("event_type", "")
        
        if event_type.startswith("session_"):
            handle_session_events(data)
        elif event_type.endswith("_complete"):
            handle_progress_events(data)
        elif event_type.startswith("auto_"):
            handle_automation_events(data)
        else:
            # Default notification handling
            title = data.get("title", "Claude Code")
            message = data.get("message", "Notification")
            urgent = data.get("urgent", False)
            sound = data.get("sound", "Glass")
            
            send_notification(title, message, sound, urgent)
        
        # Always return success
        print(json.dumps({"ok": True}))
        
    except Exception as e:
        # Log error but don't fail
        error_msg = f"Notification hook error: {str(e)}"
        send_notification("❌ Hook Error", error_msg, "Basso", urgent=True)
        print(json.dumps({"error": error_msg}))

if __name__ == "__main__":
    main()