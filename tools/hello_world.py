"""
VHost management tool that inherits from GenericTool.
Demonstrates how to create MCP tools using the base class.
"""

from typing import Dict, Any, Optional
from .generic import GenericTool, ToolCollection

class HelloWorldTool(GenericTool):
    """
    Tool for managing vhosts on Hypernode.
    Inherits from GenericTool to get common functionality.
    """
    
    def __init__(self):
        """Initialize the VHost tool."""
        super().__init__("VHostTool")
    
    @mcp.tool(
        name="hello_world",
        description="Hello World Tool",
    )
    async def execute(self, **kwargs) -> ToolResult:
        return "Hello World"

tool_collection = ToolCollection()
tool_collection.add_tool(HelloWorldTool())