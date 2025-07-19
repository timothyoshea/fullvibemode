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
