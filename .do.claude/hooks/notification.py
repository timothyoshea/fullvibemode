#!/usr/bin/env python3
import sys
import json
import subprocess
import platform

def main():
    data = json.load(sys.stdin)
    message = data.get("message", "Claude Code notification")
    title = data.get("title", "Claude Code")
    
    if platform.system() == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], capture_output=True)
    elif platform.system() == "Linux":
        try:
            subprocess.run(["notify-send", title, message], capture_output=True)
        except FileNotFoundError:
            pass
    
    print(json.dumps({"ok": True}))

if __name__ == "__main__":
    main()