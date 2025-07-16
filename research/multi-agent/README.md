# Multi-Agent Setup with Claude Code

## Overview
Claude Code supports advanced multi-agent workflows through the Model Context Protocol (MCP) system.

## Key Capabilities

### Multiple Server Connections
- Claude Code can connect to multiple specialized servers simultaneously
- Servers can be configured at different scopes: local, project, and user-level
- Each server can provide different tools and capabilities

### Resource Sharing
- MCP servers expose resources that can be referenced using @ mentions
- Resources include text, JSON, structured data, and more
- Multiple resources can be referenced in a single prompt

### Dynamic Command Discovery
- MCP servers expose prompts that become available as slash commands
- Prompts are dynamically discovered from connected servers
- Support for executing prompts with or without arguments

### Transport Types
- stdio: Direct process communication
- SSE (Server-Sent Events): Real-time web communication
- HTTP: Standard web API communication

## Best Practices

1. **Server Organization**: Use different servers for different domains (databases, docs, version control)
2. **Resource Management**: Use @ mentions to reference specific resources efficiently
3. **Authentication**: Implement OAuth 2.0 for remote servers requiring authentication
4. **Scoping**: Configure servers at appropriate scopes (user vs project vs local)

## Example Configuration
```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-sqlite"],
      "transport": "stdio"
    },
    "docs": {
      "command": "python",
      "args": ["-m", "docs_server"],
      "transport": "stdio"
    }
  }
}
```