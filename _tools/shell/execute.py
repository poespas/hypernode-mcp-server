"""
Tool for executing shell commands with safety restrictions.
"""

import asyncio
from typing import Dict, Any, Optional
from mcp import Tool
from utils.command_executor import CommandExecutor

async def execute_shell_command_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a shell command with safety restrictions.
    
    Args:
        command: The shell command to execute
        timeout: Timeout in seconds (default: 30)
        working_directory: Working directory for the command
        
    Returns:
        Dict containing the command execution result
    """
    command = arguments.get("command")
    timeout = arguments.get("timeout", 30)
    working_directory = arguments.get("working_directory")
    
    if not command:
        return {
            "success": False,
            "error": "command parameter is required"
        }
    
    # Check if command is dangerous
    if CommandExecutor.is_dangerous_command(command):
        return {
            "success": False,
            "error": f"Command '{command}' is blocked for security reasons. Dangerous commands are not allowed.",
            "blocked_commands": list(CommandExecutor.DANGEROUS_COMMANDS)
        }
    
    # Execute the command
    result = await CommandExecutor.execute_command(
        command, 
        timeout=timeout,
        cwd=working_directory
    )
    
    return {
        "success": result.success,
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code,
        "timeout": timeout,
        "working_directory": working_directory
    }

# Tool instance
execute_shell_command = Tool(
    name="execute_shell_command",
    description="Execute shell commands with safety restrictions (dangerous commands like rm are blocked)",
    inputSchema={
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The shell command to execute"},
            "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30},
            "working_directory": {"type": "string", "description": "Working directory for the command"}
        },
        "required": ["command"]
    }
) 