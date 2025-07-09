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

### Creating New Tools

The Hypernode MCP Server uses a custom tool system that automatically discovers and registers tools. Here's how to create new tools:

#### Tool Structure

1. **Create a new tool file** in the appropriate directory under `tools/`
2. **Inherit from `BaseTool`** (from `tools.generic`)
3. **Implement methods with `tool_` prefix** - these become the actual MCP tools
4. **Use the tool registry** for automatic registration

#### Example: Hello World Tool

Here's a complete example based on `tools/hello_world.py`:

```python
"""
Hello World tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from .generic import BaseTool, tool_registry

class HelloWorldTool(BaseTool):
    """Hello World tool implementation."""
    
    async def tool_hello_world(self) -> Dict[str, Any]:
        """
        Simple hello world tool for testing.
        
        Returns:
            Dict containing a hello world message
        """
        return {
            "message": "Hello World from Hypernode MCP Server!",
            "status": "success"
        }

# Create and register the tool instance automatically
hello_world_tool = HelloWorldTool()
tool_registry.register_tool(hello_world_tool)
```

#### Key Components

1. **BaseTool Inheritance**: All tools inherit from `BaseTool` which provides:
   - Automatic MCP registration
   - Logging setup
   - Common functionality

2. **Method Naming Convention**: 
   - Methods starting with `tool_` become MCP tools
   - The tool name is the method name without the `tool_` prefix
   - Example: `tool_hello_world()` becomes the `hello_world` tool

3. **Return Format**: Tools should return `Dict[str, Any]` with:
   - `success`: Boolean indicating success/failure
   - `error`: Error message if applicable
   - Other relevant data

4. **Automatic Registration**: 
   - Create a tool instance at module level
   - Register it with `tool_registry.register_tool(tool_instance)`
   - The registry automatically discovers and registers all tools

#### Advanced Tool Example

Here's a more complex example with command execution:

```python
"""
Example tool that executes shell commands.
"""

from typing import Dict, Any, Optional
from .generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class ExampleTool(BaseTool):
    """Example tool with command execution."""
    
    async def tool_example_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute a shell command with timeout.
        
        Args:
            command: The shell command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Dict containing command execution results
        """
        try:
            result = await CommandExecutor.execute_command(command, timeout=timeout)
            
            return {
                "success": result.success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.return_code,
                "command": command
            }
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    async def tool_example_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process JSON data.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Dict containing processed data
        """
        return {
            "success": True,
            "processed_data": data,
            "timestamp": "2024-01-01T00:00:00Z"
        }

# Create and register the tool instance
example_tool = ExampleTool()
tool_registry.register_tool(example_tool)
```

#### Tool Organization and Folder Structure

Tools should be organized in appropriate directories following a clear categorization system. Each category should have its own directory with related tools grouped together.

##### Current Tool Categories and Structure

Based on the tools currently in `server.py`, here's the planned folder structure:

```
tools/
├── __init__.py                    # Auto-registration logic
├── generic.py                     # BaseTool and registry
├── hello_world.py                 # Simple example tool
├── vhosts/                        # VHost management tools
│   ├── __init__.py
│   ├── list.py                    # list_vhosts tool
│   └── modify.py                  # modify_vhost tool
├── incidents/                     # Incident management tools
│   ├── __init__.py
│   ├── list.py                    # list_incidents tool
│   └── get.py                     # get_incident tool
├── block_attack/                  # Attack blocking tools
│   ├── __init__.py
│   ├── list.py                    # list_attacks tool
│   └── block.py                   # block_attack tool
├── nginx_logs/                    # Nginx log analysis tools
│   ├── __init__.py
│   ├── analyze.py                 # analyze_nginx_logs tool
│   └── fields.py                  # analyze_nginx_logs_fields tool
└── shell/                         # Shell command tools
    ├── __init__.py
    └── execute.py                 # execute_shell_command tool
```

##### Tool Migration Plan

The following tools from `server.py` will be migrated to their respective directories:

| Tool Function | Category | Target File | Tool Method Name |
|---------------|----------|-------------|------------------|
| `list_vhosts()` | VHosts | `tools/vhosts/list.py` | `tool_list_vhosts()` |
| `modify_vhost()` | VHosts | `tools/vhosts/modify.py` | `tool_modify_vhost()` |
| `list_incidents()` | Incidents | `tools/incidents/list.py` | `tool_list_incidents()` |
| `get_incident()` | Incidents | `tools/incidents/get.py` | `tool_get_incident()` |
| `list_attacks()` | Block Attack | `tools/block_attack/list.py` | `tool_list_attacks()` |
| `block_attack()` | Block Attack | `tools/block_attack/block.py` | `tool_block_attack()` |
| `analyze_nginx_logs()` | Nginx Logs | `tools/nginx_logs/analyze.py` | `tool_analyze_nginx_logs()` |
| `analyze_nginx_logs_fields()` | Nginx Logs | `tools/nginx_logs/fields.py` | `tool_analyze_nginx_logs_fields()` |
| `execute_shell_command()` | Shell | `tools/shell/execute.py` | `tool_execute_shell_command()` |

##### Naming Conventions

1. **Directory Names**: Use lowercase with underscores for multi-word directories
   - `block_attack/` (not `block-attack/` or `blockAttack/`)

2. **File Names**: Use descriptive, action-oriented names
   - `list.py`, `modify.py`, `analyze.py`, `execute.py`

3. **Tool Method Names**: Use the `tool_` prefix followed by the original function name
   - `list_vhosts()` becomes `tool_list_vhosts()`

4. **Class Names**: Use PascalCase with "Tool" suffix
   - `VHostsListTool`, `IncidentsListTool`, `BlockAttackListTool`

##### Directory Structure Rules

1. **One Category Per Directory**: Each directory should contain tools for a single functional area
2. **Related Tools Together**: Tools that work with the same system or command should be grouped
3. **Clear Separation**: Each tool should be in its own file for maintainability
4. **Consistent Structure**: All directories should follow the same pattern:
   ```
   category/
   ├── __init__.py          # Package initialization
   ├── tool1.py             # First tool in category
   ├── tool2.py             # Second tool in category
   └── tool3.py             # Third tool in category
   ```

##### Benefits of This Structure

1. **Maintainability**: Easy to find and modify specific tools
2. **Scalability**: New tools can be added to appropriate categories
3. **Organization**: Clear separation of concerns and functionality
4. **Consistency**: Standardized naming and structure across all tools
5. **Discoverability**: Developers can quickly understand what each directory contains

#### Best Practices

1. **Type Hints**: Always use type hints for parameters and return values
2. **Docstrings**: Provide clear docstrings for all tool methods
3. **Error Handling**: Implement proper error handling and logging
4. **Validation**: Validate input parameters when necessary
5. **Async/Await**: Use async/await for I/O operations
6. **Logging**: Use `self.logger` for logging within tools
7. **Return Format**: Maintain consistent return format across tools

#### Testing Tools

Before implementing tools, test the underlying commands:

```bash
# Test command execution
hypernode-manage-vhosts --list --format json

# Test error conditions
hypernode-manage-vhosts nonexistent-vhost

# Test with various parameters
pnl --today --limit 10
```

#### Security Considerations

- **Input Validation**: Always validate and sanitize user inputs
- **Command Safety**: Use `CommandExecutor` which includes safety checks
- **Timeout Protection**: Set appropriate timeouts for long-running operations
- **Error Handling**: Don't expose sensitive information in error messages
- **Logging**: Log all operations for audit purposes

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

## Running Tests

This project uses [pytest](https://docs.pytest.org/) for testing. All tests are located in the `tests/` directory, which mirrors the structure of the source code.

### Running Tests Locally (Docker)

To run all tests in the official Hypernode Docker image, use the provided script:

```bash
./runtests.sh
```

This will:
- Start the Docker container (`docker.hypernode.com/byteinternet/hypernode-bookworm-docker-php84-mysql80`)
- Set up a Python virtual environment
- Install all dependencies
- Run the test suite with pytest

### Running Tests Locally (Host Python)

If you have all dependencies installed locally, you can also run:

```bash
pytest tests/
```

### Test Structure
- All tests are in the `tests/` directory, **mirroring the structure of the source code exactly**.
- **Every test file must be placed in a subdirectory that matches the source code path.**
- **Test filenames must include the full path to ensure uniqueness across the entire test suite.**
    - For example:
        - `tools/vhosts/list.py` → `tests/tools/vhosts/test_vhosts_list.py`
        - `tools/vhosts/modify.py` → `tests/tools/vhosts/test_vhosts_modify.py`
        - `tools/incidents/list.py` → `tests/tools/incidents/test_incidents_list.py`
        - `tools/incidents/get.py` → `tests/tools/incidents/test_incidents_get.py`
- Each tool or module should have its own test file with a unique name that includes the category and action.
- Tests are written as **synchronous** functions (no async/await).

### Writing New Tests
- Create a new test file in the appropriate subdirectory under `tests/`.
- Use `pytest` conventions: test files start with `test_`, test classes start with `Test`, and test functions start with `test_`.
- Example:

```python
import pytest
from tools.hello_world import HelloWorldTool

def test_hello_world():
    tool = HelloWorldTool()
    result = tool.tool_hello_world().__await__().__next__()
    assert result["message"] == "Hello World from Hypernode MCP Server!"
```

### Continuous Integration
- All tests are run automatically on each push and pull request to `main` via GitHub Actions using the official Hypernode Docker image.

## License

This project is licensed under the MIT License.

## Contributing

1. Follow the coding standards in `.cursorrules`
2. Add tests for new functionality
3. Update documentation for new tools
4. Ensure all commands are tested before implementation 