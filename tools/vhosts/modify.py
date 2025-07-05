"""
VHost modification tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class VHostsModifyTool(BaseTool):
    """VHost modification tool implementation."""
    
    async def tool_modify_vhost(self, vhost: str, action: str, value: str) -> Dict[str, Any]:
        """
        Modify vhost settings (enable/disable, change PHP version, etc.).
        
        Args:
            vhost: VHost name to modify
            action: Action to perform (https/type/varnish)
            value: Value for the action (true/false for enable/disable, PHP version for php)
        
        Returns:
            Dict containing the result of the modification
        """
        # Add "no" prefix if action value is "false"
        if value.lower() == "false":
            command = f"hypernode-manage-vhosts {vhost} --disable-{action}"
        elif value.lower() == "true":
            command = f"hypernode-manage-vhosts {vhost} --{action}"
        else:
            # If value is not true/false, add it as a value parameter
            command = f"hypernode-manage-vhosts {vhost} --{action} {value}"
        
        result = await CommandExecutor.execute_command(command)
        
        return {
            "success": result.success,
            "result": result.stdout if result.success and result.stdout else result.stderr,
            "vhost": vhost,
            "action": action,
            "value": value
        }

# Create and register the tool instance automatically
vhosts_modify_tool = VHostsModifyTool()
tool_registry.register_tool(vhosts_modify_tool) 