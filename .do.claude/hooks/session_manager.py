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
