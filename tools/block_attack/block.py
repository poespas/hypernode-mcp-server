"""
Attack blocking tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class BlockAttackTool(BaseTool):
    """Attack blocking tool implementation."""
    
    async def tool_block_attack(self, attack_type: str) -> Dict[str, Any]:
        """
        Block a specific attack type using hypernode-systemctl block_attack.
        
        WARNING: This should be run with extreme caution as it can block legitimate traffic
        and affect your website's functionality. Only use when you are certain about the
        attack type and have verified the need for blocking.
        
        Args:
            attack_type: The type of attack to block (e.g., "BlockChinaBruteForce", "BlockAhrefsBot")
        
        Returns:
            Dict containing the result of the blocking operation
        """
        command = f"hypernode-systemctl block_attack {attack_type}"
        
        result = await CommandExecutor.execute_command(command)
        
        return {
            "success": result.success,
            "result": result.stdout if result.success else result.stderr,
            "attack_type": attack_type
        }

# Create and register the tool instance automatically
block_attack_tool = BlockAttackTool()
tool_registry.register_tool(block_attack_tool) 