"""
Tool for blocking specific attacks using hypernode-systemctl block_attack.
"""

import asyncio
from typing import Dict, Any
from mcp import Tool
from utils.command_executor import CommandExecutor

async def block_attack_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Block a specific attack using hypernode-systemctl block_attack.
    
    Args:
        attack_name: The name of the attack to block (e.g., BlockChinaBruteForce)
        
    Returns:
        Dict containing the blocking operation result
    """
    attack_name = arguments.get("attack_name")
    
    if not attack_name:
        return {
            "success": False,
            "error": "attack_name parameter is required"
        }
    
    if not CommandExecutor.validate_attack_name(attack_name):
        return {
            "success": False,
            "error": f"Invalid attack name format: {attack_name}. Must start with 'Block'"
        }
    
    command = f"hypernode-systemctl block_attack {attack_name}"
    result = await CommandExecutor.execute_command(command, timeout=60)
    
    return {
        "success": result.success,
        "command": command,
        "attack_name": attack_name,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code
    }

# Tool instance
block_attack = Tool(
    name="block_attack",
    description="Block a specific attack using hypernode-systemctl block_attack",
    inputSchema={
        "type": "object",
        "properties": {
            "attack_name": {"type": "string", "description": "The name of the attack to block (e.g., BlockChinaBruteForce)"}
        },
        "required": ["attack_name"]
    }
) 