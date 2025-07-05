"""
VHost listing tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class VHostsListTool(BaseTool):
    """VHost listing tool implementation."""
    
    async def tool_list_vhosts(self) -> Dict[str, Any]:
        """
        List all vhosts configured on the Hypernode with their settings.
        
        Returns:
            Dict containing the list of vhosts and their configurations
        """
        command = "hypernode-manage-vhosts --list --format json"
        
        success, result = await CommandExecutor.execute_json_command(command)
        
        if not success:
            return {
                "success": False,
                "error": result,
                "vhosts": {}
            }
        
        return {
            "success": True,
            "vhosts": result,
            "count": len(result) if isinstance(result, dict) else 0
        }

# Create and register the tool instance automatically
vhosts_list_tool = VHostsListTool()
tool_registry.register_tool(vhosts_list_tool) 