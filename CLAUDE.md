# FullVibeMode - Claude Code Research Repository

## Project Purpose
FullVibeMode serves as a comprehensive research and automation system for Claude Code, designed to:
- Research and document Claude Code capabilities and best practices
- Provide automated workflows and "YOLO mode" configurations
- Maintain a knowledge base that improves over time
- Create reusable configurations and scripts for Claude Code optimization

## Repository Structure

### Core Directories
- `research/` - Comprehensive research documentation
  - `multi-agent/` - Multi-agent setup and MCP configuration
  - `automation/` - Automation, hooks, and YOLO mode documentation
  - `thinking-modes/` - Extended thinking and ultra thinking capabilities
  - `best-practices/` - Operational best practices and guidelines
  - `examples/` - Practical examples and automation scripts
- `.do.claude/` - Claude Code configuration and hooks
  - `hooks/` - Pre/post tool use hooks for automation
  - `settings.json` - Main configuration file
  - `logs/` - Automated logging (created by hooks)

## Key Features Implemented

### 1. Hooks System
- **Pre-tool validation**: Automatically validates commands before execution
- **Post-tool logging**: Comprehensive logging of all tool usage
- **Notification system**: Automated notifications for important events
- **Session tracking**: Detailed session analytics and usage patterns

### 2. Automation Capabilities
- **YOLO Mode**: Minimal interruption, maximum automation
- **Smart validation**: Context-aware command validation
- **Auto-approval**: Configured permissions for seamless operation
- **Safety checks**: Intelligent blocking of dangerous operations

### 3. Multi-Agent Setup
- **MCP Integration**: Multiple specialized servers for different domains
- **Resource sharing**: Efficient @ mention system for resource access
- **Dynamic commands**: Slash commands from connected servers
- **Flexible transport**: Support for stdio, SSE, and HTTP connections

### 4. Extended Thinking
- **Ultra thinking**: Deep reasoning for complex problems
- **Iterative refinement**: Progressive thinking intensification
- **Context-aware analysis**: Thinking modes optimized for different scenarios
- **Documentation**: Systematic approach to complex problem-solving

## Configuration Guidelines

### For YOLO Mode Operation
```json
{
  "permissions": {
    "bash": "allow",
    "read": "allow",
    "write": "allow",
    "edit": "allow"
  },
  "hooks": {
    "pre_tool_use": [{"match": {}, "run": ["hooks/pre_tool_use.py"]}],
    "post_tool_use": [{"match": {}, "run": ["hooks/post_tool_use.py"]}]
  }
}
```

### For Multi-Agent Workflows
- Configure MCP servers for different domains
- Use appropriate authentication for remote servers
- Organize servers by scope (user, project, local)
- Implement proper resource management

## Usage Instructions

### For Researchers
1. Use extended thinking modes for complex analysis
2. Document findings in appropriate research directories
3. Update this CLAUDE.md file with new insights
4. Create git checkpoints after significant discoveries

### For Automation
1. Test hooks thoroughly before deployment
2. Start with conservative permissions
3. Monitor logs for usage patterns
4. Implement incremental automation improvements

### For Development
1. Use the research documentation as reference
2. Implement examples from the examples directory
3. Follow best practices for configuration
4. Maintain audit trails for all operations

## Git Workflow
- Automated commits after major updates
- Checkpoint system for preserving research
- Comprehensive commit messages with co-authorship
- Proper .gitignore for temporary files

## Best Practices Followed
- **Security First**: All dangerous operations are blocked or require approval
- **Incremental Automation**: Start conservative, increase automation gradually
- **Comprehensive Logging**: All tool usage is logged for audit and analysis
- **Context Preservation**: This file and research docs maintain context across sessions
- **Modular Design**: Separate concerns for different aspects of automation

## Future Enhancements
- Integration with external tools and APIs
- Advanced AI-powered command validation
- Real-time collaboration features
- Enhanced security and audit capabilities
- Custom MCP server development

## How to Use This Repository
1. **Research**: Browse the research/ directory for comprehensive documentation
2. **Configure**: Use the configurations in .do.claude/ as templates
3. **Automate**: Implement the examples and scripts for your workflows
4. **Iterate**: Continuously improve configurations based on usage patterns
5. **Share**: Use this as a foundation for team-wide Claude Code optimization

This repository represents a comprehensive approach to Claude Code mastery, combining research, automation, and best practices into a cohesive system that improves over time.