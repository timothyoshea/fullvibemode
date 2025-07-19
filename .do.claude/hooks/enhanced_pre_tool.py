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
