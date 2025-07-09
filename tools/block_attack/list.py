"""
Attack listing tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class BlockAttackListTool(BaseTool):
    """Attack listing tool implementation."""
    
    async def tool_list_attacks(self) -> Dict[str, Any]:
        """
        List all available but not necessarily enabled known attack-blocking options on the Hypernode.
        
        Returns:
            Dict containing the list of available attack types
        """
        command = "hypernode-systemctl block_attack --help"
        
        result = await CommandExecutor.execute_command(command)
        
        if not result.success:
            return {
                "success": False,
                "error": result.stderr,
                "attacks": []
            }
        
        # Parse the help output to extract attack names and descriptions
        lines = result.stdout.strip().split('\n')
        attacks = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('usage:') and not line.startswith('The possible values are:') and not line.startswith('options:'):
                # Look for lines that contain attack names and descriptions
                if 'Block' in line and '\t' in line:
                    # Extract attack name and description
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        attack_name = parts[0].strip()
                        description = parts[1].strip()
                        
                        attacks.append({
                            "name": attack_name,
                            "description": description
                        })
        
        return {
            "success": True,
            "attacks": attacks,
            "count": len(attacks),
            "raw_output": result.stdout
        }

# Create and register the tool instance automatically
block_attack_list_tool = BlockAttackListTool()
tool_registry.register_tool(block_attack_list_tool) 