#!/usr/bin/env python3
"""
Generate project-specific CLAUDE.md file
"""
import sys
import os
import json

def detect_project_info(target_dir):
    """Detect project information from directory contents"""
    info = {
        "name": os.path.basename(target_dir),
        "type": "generic",
        "description": "A software project",
        "tech_stack": []
    }
    
    # Check for package.json
    package_json = os.path.join(target_dir, "package.json")
    if os.path.exists(package_json):
        try:
            with open(package_json, 'r') as f:
                data = json.load(f)
                info["name"] = data.get("name", info["name"])
                info["description"] = data.get("description", info["description"])
                info["type"] = "node"
                info["tech_stack"] = ["Node.js", "JavaScript/TypeScript"]
        except:
            pass
    
    # Check for Python files
    elif any(f.endswith('.py') for f in os.listdir(target_dir)):
        info["type"] = "python"
        info["tech_stack"] = ["Python"]
    
    # Check for Rust
    elif os.path.exists(os.path.join(target_dir, "Cargo.toml")):
        info["type"] = "rust"
        info["tech_stack"] = ["Rust"]
    
    # Check for Java
    elif os.path.exists(os.path.join(target_dir, "pom.xml")):
        info["type"] = "java"
        info["tech_stack"] = ["Java", "Maven"]
    
    return info

def generate_claude_md(target_dir, project_type):
    """Generate CLAUDE.md content for the project"""
    
    info = detect_project_info(target_dir)
    
    template = f"""# {info["name"]}

## Project Overview
{info["description"]}

**Project Type**: {info["type"]}
**Tech Stack**: {", ".join(info["tech_stack"])}

## Claude Code Configuration

### Automation Features Enabled
- ✅ **Ultra Thinking**: Extended reasoning for complex problems
- ✅ **YOLO Mode**: Minimal interruption, maximum automation
- ✅ **Multi-Agent MCP**: Specialized servers for different domains
- ✅ **Smart Notifications**: Contextual alerts and updates
- ✅ **Auto-Logging**: Comprehensive tool usage tracking
- ✅ **Git Checkpointing**: Automated commit system

### MCP Servers Active
- **Filesystem**: Direct file system access and manipulation
- **SQLite**: Database queries and management
- **GitHub**: Repository integration and API access
{f"- **NPM**: Package management and scripts" if info["type"] == "node" else ""}
{f"- **Python**: Package and environment management" if info["type"] == "python" else ""}

### Hooks Configuration
- **Pre-tool validation**: Smart command validation with safety checks
- **Post-tool logging**: Comprehensive usage analytics
- **Notification system**: Real-time alerts for important events
- **Session management**: Automatic session tracking and cleanup

## Project-Specific Instructions

### Development Workflow
1. Use extended thinking for architectural decisions
2. Leverage MCP servers for efficient operations
3. Let automation handle routine tasks
4. Review logs for optimization opportunities

### Code Standards
- Follow existing code style and patterns
- Use automated validation for quality control
- Document decisions and trade-offs
- Maintain comprehensive test coverage

### Automation Guidelines
- Trust the YOLO mode for routine operations
- Use ultra thinking for complex problem-solving
- Leverage multi-agent capabilities for specialized tasks
- Monitor notifications for important updates

## Usage Examples

### Extended Thinking
```
think ultra hard about the architecture for this feature
think deeply about potential edge cases
think more about performance implications
```

### Multi-Agent Operations
```
@filesystem search for configuration files
@github create pull request
@sqlite query user data
```

### Smart Automation
The system automatically:
- Validates commands before execution
- Logs all operations for audit trails
- Sends notifications for important events
- Creates git checkpoints after major changes

## Project Structure
```
{info["name"]}/
├── .do.claude/           # Claude Code configuration
│   ├── hooks/           # Automation hooks
│   ├── logs/            # Usage logs
│   └── settings.json    # Main configuration
├── research/            # Research and documentation
└── CLAUDE.md           # This file
```

## Maintenance
- Update this file as project evolves
- Review and optimize hook configurations
- Monitor usage patterns in logs
- Adjust automation settings as needed

## Quick Commands
- `#` - Add memory quickly
- `/memory` - Manage project memories
- `think harder` - Deeper analysis
- `@resource` - Reference MCP resources

This project is optimized for maximum Claude Code automation and efficiency.
"""
    
    return template

def main():
    if len(sys.argv) != 3:
        print("Usage: generate-claude-md.py <target_dir> <project_type>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    project_type = sys.argv[2]
    
    content = generate_claude_md(target_dir, project_type)
    print(content)

if __name__ == "__main__":
    main()