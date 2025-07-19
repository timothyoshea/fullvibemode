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
