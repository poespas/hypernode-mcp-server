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
