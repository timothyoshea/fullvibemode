#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

def main():
    data = json.load(sys.stdin)
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    session_log = {
        "timestamp": datetime.now().isoformat(),
        "event": "session_end",
        "total_tools_used": data.get("total_tools_used", 0),
        "duration_ms": data.get("duration_ms", 0)
    }
    
    log_file = os.path.join(log_dir, f"sessions_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, 'a') as f:
        f.write(json.dumps(session_log) + '\n')
    
    print(json.dumps({"ok": True}))

if __name__ == "__main__":
    main()