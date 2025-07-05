"""
Shell command execution tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class ShellExecuteTool(BaseTool):
    """Shell command execution tool implementation."""
    
    async def tool_execute_shell_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command safely (dangerous commands are blocked).
        
        Args:
            command: Shell command to execute
        
        Returns:
            Dict containing the command execution result
        """
        result = await CommandExecutor.execute_command(command)
        
        return {
            "success": result.success,
            "result": result.stdout if result.success else result.stderr,
            "command": command
        }

# Create and register the tool instance automatically
shell_execute_tool = ShellExecuteTool()
tool_registry.register_tool(shell_execute_tool) 