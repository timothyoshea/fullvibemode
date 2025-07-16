#!/usr/bin/env python3
import sys
import json
import os
from datetime import datetime

def main():
    data = json.load(sys.stdin)
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": data.get("tool_name", "unknown"),
        "exit_code": data.get("exit_code", None),
        "duration_ms": data.get("duration_ms", 0)
    }
    
    log_file = os.path.join(log_dir, f"tool_usage_{datetime.now().strftime('%Y%m%d')}.log")
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(json.dumps(data))

if __name__ == "__main__":
    main()