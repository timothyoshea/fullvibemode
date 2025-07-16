#!/usr/bin/env python3
import sys
import json

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    if "rm" in tool_name or "delete" in tool_name:
        print(json.dumps({"error": "Blocked dangerous tool use: " + tool_name}))
        sys.exit(1)
    print(json.dumps({"ok": True}))

if __name__ == "__main__":
    main()