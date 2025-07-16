# Automation Scripts and Examples

## Advanced Hook Examples

### Smart Command Validation
```python
#!/usr/bin/env python3
import sys
import json
import re

def validate_command(command):
    """Intelligent command validation with context awareness"""
    
    # Safe commands that can always run
    safe_patterns = [
        r'^ls\s',
        r'^cat\s',
        r'^grep\s',
        r'^find\s.*-name',
        r'^git status',
        r'^git log',
        r'^python.*--help',
        r'^npm\s(list|info|view)'
    ]
    
    # Commands that need approval
    approval_patterns = [
        r'^git\s(add|commit|push)',
        r'^npm\s(install|update)',
        r'^pip\s(install|update)',
        r'^chmod\s',
        r'^mkdir\s',
        r'^touch\s'
    ]
    
    # Dangerous commands to block
    dangerous_patterns = [
        r'rm\s.*-rf',
        r'sudo\s',
        r'chmod\s777',
        r'>\s*/dev/',
        r'curl.*\|\s*sh',
        r'wget.*\|\s*sh'
    ]
    
    for pattern in safe_patterns:
        if re.match(pattern, command):
            return {"ok": True}
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            return {"error": f"Blocked dangerous command: {command}"}
    
    for pattern in approval_patterns:
        if re.search(pattern, command):
            return {"approve": True, "message": f"Command needs approval: {command}"}
    
    return {"ok": True}

def main():
    data = json.load(sys.stdin)
    command = data.get("parameters", {}).get("command", "")
    
    if not command:
        print(json.dumps({"ok": True}))
        return
    
    result = validate_command(command)
    print(json.dumps(result))
    
    if result.get("error"):
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Automated Project Setup
```python
#!/usr/bin/env python3
import sys
import json
import os
import subprocess

def setup_project_environment():
    """Automatically set up project environment based on detected files"""
    
    project_root = os.getcwd()
    setup_actions = []
    
    # Check for different project types
    if os.path.exists("package.json"):
        setup_actions.append("npm install")
    
    if os.path.exists("requirements.txt"):
        setup_actions.append("pip install -r requirements.txt")
    
    if os.path.exists("Cargo.toml"):
        setup_actions.append("cargo build")
    
    if os.path.exists("pom.xml"):
        setup_actions.append("mvn install")
    
    # Execute setup actions
    for action in setup_actions:
        try:
            subprocess.run(action.split(), check=True, cwd=project_root)
        except subprocess.CalledProcessError as e:
            return {"error": f"Setup failed: {e}"}
    
    return {"ok": True, "actions": setup_actions}

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    
    # Trigger setup on project entry
    if tool_name == "cd" and "project" in data.get("parameters", {}).get("command", ""):
        result = setup_project_environment()
        print(json.dumps(result))
    else:
        print(json.dumps({"ok": True}))

if __name__ == "__main__":
    main()
```

## Configuration Examples

### YOLO Mode Settings
```json
{
  "permissions": {
    "bash": "allow",
    "read": "allow",
    "write": "allow",
    "edit": "allow",
    "grep": "allow",
    "glob": "allow"
  },
  "hooks": {
    "pre_tool_use": [
      {
        "match": {"tool_name": "bash"},
        "run": ["hooks/smart_validation.py"]
      }
    ],
    "post_tool_use": [
      {
        "match": {},
        "run": ["hooks/enhanced_logging.py"]
      }
    ]
  },
  "environment": {
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "true",
    "CLAUDE_CODE_DISABLE_TERMINAL_TITLE": "true"
  }
}
```

### Multi-Agent MCP Configuration
```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-sqlite", "./data/app.db"],
      "transport": "stdio"
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "./src"],
      "transport": "stdio"
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "transport": "stdio",
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "docs": {
      "command": "python",
      "args": ["-m", "docs_server", "--port", "8080"],
      "transport": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

## Workflow Examples

### Automated Code Review
```bash
# Hook that runs on git commit
#!/bin/bash
# Check code quality before commit
npm run lint
npm run test
npm run build

# If all pass, proceed with commit
if [ $? -eq 0 ]; then
    echo "All checks passed, proceeding with commit"
    exit 0
else
    echo "Quality checks failed, blocking commit"
    exit 1
fi
```

### Auto-Documentation Generation
```python
def generate_documentation():
    """Auto-generate documentation from code changes"""
    
    # Get changed files
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True, text=True
    )
    
    changed_files = result.stdout.strip().split('\n')
    
    # Generate docs for changed files
    for file in changed_files:
        if file.endswith('.py'):
            generate_python_docs(file)
        elif file.endswith('.js'):
            generate_js_docs(file)
    
    return {"ok": True, "files_processed": len(changed_files)}
```