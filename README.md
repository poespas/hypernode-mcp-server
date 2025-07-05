# Hypernode MCP Server

A Model Context Protocol (MCP) server for managing Hypernode environments with comprehensive tools for vhost management, incident handling, attack blocking, and nginx log analysis.

## Features

- **VHost Management**: List and modify vhost configurations
- **Incident Management**: List and retrieve incident files
- **Attack Blocking**: List and block various types of attacks
- **Nginx Log Analysis**: Analyze logs with filters and date ranges
- **Shell Command Execution**: Safe command execution with restrictions
- **Multiple Transport Support**: stdio, HTTP, and SSE (Server-Sent Events)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python server.py
```

The server will start with:
- stdio transport for MCP clients
- HTTP server on port 8000
- SSE server on port 8001

## Available Tools

### VHost Management

#### List VHosts
Lists all configured vhosts with their settings.

```json
{
  "name": "list_vhosts",
  "description": "List all vhosts configured on the Hypernode with their settings"
}
```

**Response:**
```json
{
  "success": true,
  "vhosts": {
    "example.hypernode.io": {
      "default_server": false,
      "force_https": true,
      "https": true,
      "ssl_config": "intermediate",
      "type": "magento2",
      "varnish": false
    }
  },
  "count": 1
}
```

#### Modify VHost
Modify vhost configurations (create, update, delete, SSL settings, etc.).

```json
{
  "name": "modify_vhost",
  "description": "Modify vhost configurations (create, update, delete, SSL settings, etc.)",
  "arguments": {
    "servername": "example.hypernode.io",
    "action": "create",
    "vhost_type": "magento2",
    "https": true,
    "force_https": true,
    "varnish": false
  }
}
```

### Incident Management

#### List Incidents
List all incidents in the ~/incidents directory.

```json
{
  "name": "list_incidents",
  "description": "List all incidents in the ~/incidents directory"
}
```

#### Get Incident
Retrieve files from a specific incident directory.

```json
{
  "name": "get_incident",
  "description": "Get files from a specific incident directory ~/incidents/[date]/*",
  "arguments": {
    "date": "2024-01-15",
    "file_pattern": "*.log"
  }
}
```

### Attack Blocking

#### List Attacks
List all available attack blocking options.

```json
{
  "name": "list_attacks",
  "description": "List all available attack blocking options from hypernode-systemctl block_attack"
}
```

#### Block Attack
Block a specific attack type.

```json
{
  "name": "block_attack",
  "description": "Block a specific attack using hypernode-systemctl block_attack",
  "arguments": {
    "attack_name": "BlockChinaBruteForce"
  }
}
```

### Nginx Log Analysis

#### Analyze Nginx Logs
Analyze nginx logs with various filters and options.

```json
{
  "name": "analyze_nginx_logs",
  "description": "Analyze nginx logs using pnl with filters, date ranges, and field selection",
  "arguments": {
    "date_range": "today",
    "fields": "ip,status,request,user_agent",
    "filters": ["status=404", "ip~192.168"],
    "php_only": true,
    "limit": 100
  }
}
```

**Available Fields:**
- `remote_user`, `ssl_protocol`, `referer`, `user_agent`
- `remote_addr`, `ssl_cipher`, `body_bytes_sent`, `country`
- `status`, `time`, `request_time`, `port`, `request`
- `server_name`, `host`, `handler`

**Filter Examples:**
- `status=404` - Exact match
- `ip~192.168` - Regex match
- `user_agent!~bot` - Negative regex match

### Shell Command Execution

#### Execute Shell Command
Execute shell commands with safety restrictions.

```json
{
  "name": "execute_shell_command",
  "description": "Execute shell commands with safety restrictions (dangerous commands like rm are blocked)",
  "arguments": {
    "command": "ls -la /var/log",
    "timeout": 30,
    "working_directory": "/tmp"
  }
}
```

**Blocked Commands:**
- `rm`, `rmdir`, `del`, `format`, `mkfs`, `dd`, `shred`
- `kill`, `killall`, `pkill`, `halt`, `shutdown`, `reboot`

## Usage Examples

### Using with MCP Client

1. Start the server:
```bash
python server.py
```

2. Connect with an MCP client:
```bash
# Example with stdio transport
python server.py | mcp-client
```

### Using with HTTP API

The server exposes an HTTP API on port 8000:

```bash
# List vhosts
curl -X POST http://localhost:8000/tools/list_vhosts \
  -H "Content-Type: application/json" \
  -d '{}'

# Analyze nginx logs
curl -X POST http://localhost:8000/tools/analyze_nginx_logs \
  -H "Content-Type: application/json" \
  -d '{
    "date_range": "today",
    "fields": "ip,status,request",
    "filters": ["status=404"]
  }'
```

### Using with SSE (Server-Sent Events)

The server supports SSE on port 8001 for streaming responses:

```javascript
const eventSource = new EventSource('http://localhost:8001/stream');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## Security Features

- **Command Validation**: Dangerous commands are blocked
- **Input Sanitization**: All inputs are validated
- **Timeout Protection**: Commands have configurable timeouts
- **Error Handling**: Comprehensive error handling and logging
- **Audit Logging**: All command executions are logged

## Configuration

The server can be configured through environment variables:

- `MCP_HTTP_HOST`: HTTP server host (default: 0.0.0.0)
- `MCP_HTTP_PORT`: HTTP server port (default: 8000)
- `MCP_SSE_HOST`: SSE server host (default: 0.0.0.0)
- `MCP_SSE_PORT`: SSE server port (default: 8001)
- `MCP_LOG_LEVEL`: Logging level (default: INFO)

## Development

### Project Structure

```
.
├── server.py                 # Main server entry point
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .cursorrules             # Coding standards
├── utils/                   # Shared utilities
│   ├── __init__.py
│   └── command_executor.py  # Command execution utilities
└── tools/                   # MCP tools
    ├── __init__.py
    ├── vhosts/              # VHost management tools
    │   ├── __init__.py
    │   ├── list.py
    │   └── modify.py
    ├── incidents/           # Incident management tools
    │   ├── __init__.py
    │   ├── list.py
    │   └── get.py
    ├── block_attack/        # Attack blocking tools
    │   ├── __init__.py
    │   ├── list.py
    │   └── block.py
    ├── nginx_logs/          # Nginx log analysis tools
    │   ├── __init__.py
    │   └── analyze.py
    └── shell/               # Shell command tools
        ├── __init__.py
        └── execute.py
```

### Adding New Tools

1. Create a new tool file in the appropriate directory
2. Inherit from `mcp.Tool`
3. Implement the `run` method
4. Register the tool in `server.py`

Example:
```python
from mcp import Tool
from utils.command_executor import CommandExecutor

class MyTool(Tool):
    name = "my_tool"
    description = "Description of my tool"
    
    async def run(self, arguments):
        # Tool implementation
        return {"success": True, "result": "..."}

# Tool instance
my_tool = MyTool()
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure the user has appropriate permissions for Hypernode commands
2. **Command Not Found**: Verify that Hypernode tools are installed and in PATH
3. **Timeout Errors**: Increase timeout values for long-running operations
4. **JSON Parse Errors**: Check command output format and error handling

### Logging

Enable debug logging:
```bash
export MCP_LOG_LEVEL=DEBUG
python server.py
```

## License

This project is licensed under the MIT License.

## Contributing

1. Follow the coding standards in `.cursorrules`
2. Add tests for new functionality
3. Update documentation for new tools
4. Ensure all commands are tested before implementation 