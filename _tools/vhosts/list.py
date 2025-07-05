"""
Tool for listing vhosts using hypernode-manage-vhosts.
"""

import asyncio
from typing import Dict, Any, Optional
from mcp import Tool
from utils.command_executor import CommandExecutor

async def list_vhosts_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    List all vhosts using hypernode-manage-vhosts --list --format json.
    
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

# Tool instance
list_vhosts = Tool(
    name="list_vhosts",
    description="List all vhosts configured on the Hypernode with their settings",
    inputSchema={"type": "object", "properties": {}}
) 