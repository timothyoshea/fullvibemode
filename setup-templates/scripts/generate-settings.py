#!/usr/bin/env python3
"""
Generate Claude Code settings.json based on project type
"""
import sys
import json

def generate_settings(project_type):
    """Generate optimized settings for different project types"""
    
    base_settings = {
        "permissions": {
            "bash": "allow",
            "read": "allow", 
            "write": "allow",
            "edit": "allow",
            "grep": "allow",
            "glob": "allow",
            "multi_edit": "allow"
        },
        "hooks": {
            "pre_tool_use": [
                {
                    "match": {},
                    "run": ["hooks/enhanced_pre_tool.py"]
                }
            ],
            "post_tool_use": [
                {
                    "match": {},
                    "run": ["hooks/enhanced_post_tool.py"]
                }
            ],
            "notification": [
                {
                    "match": {},
                    "run": ["hooks/smart_notification.py"]
                }
            ],
            "stop": [
                {
                    "match": {},
                    "run": ["hooks/session_manager.py"]
                }
            ]
        },
        "environment": {
            "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "true",
            "CLAUDE_CODE_DISABLE_TERMINAL_TITLE": "true"
        }
    }
    
    # Project-specific MCP servers
    mcp_servers = {}
    
    if project_type == "node":
        mcp_servers.update({
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "./src"],
                "transport": "stdio"
            },
            "npm": {
                "command": "npx", 
                "args": ["@modelcontextprotocol/server-npm"],
                "transport": "stdio"
            }
        })
    
    elif project_type == "python":
        mcp_servers.update({
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "./"],
                "transport": "stdio"
            },
            "pip": {
                "command": "python",
                "args": ["-m", "pip_server"],
                "transport": "stdio"
            }
        })
    
    elif project_type == "rust":
        mcp_servers.update({
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "./src"],
                "transport": "stdio"
            }
        })
    
    # Universal MCP servers
    mcp_servers.update({
        "sqlite": {
            "command": "npx",
            "args": ["@modelcontextprotocol/server-sqlite"],
            "transport": "stdio"
        },
        "github": {
            "command": "npx",
            "args": ["@modelcontextprotocol/server-github"],
            "transport": "stdio",
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
            }
        }
    })
    
    if mcp_servers:
        base_settings["mcpServers"] = mcp_servers
    
    return base_settings

def main():
    if len(sys.argv) != 2:
        print("Usage: generate-settings.py <project_type>")
        sys.exit(1)
    
    project_type = sys.argv[1]
    settings = generate_settings(project_type)
    print(json.dumps(settings, indent=2))

if __name__ == "__main__":
    main()