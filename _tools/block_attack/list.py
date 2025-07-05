"""
Tool for listing available attack blocking options.
"""

import asyncio
from typing import Dict, Any, List
from mcp import Tool
from utils.command_executor import CommandExecutor

async def list_attacks_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    List all available attack blocking options.
    
    Returns:
        Dict containing the list of available attack blocking options
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
            if 'Block' in line and 'Attempts to deploy' in line:
                # Extract attack name and description
                parts = line.split()
                if len(parts) >= 2:
                    attack_name = parts[0]
                    description = ' '.join(parts[1:])
                    
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

# Tool instance
list_attacks = Tool(
    name="list_attacks",
    description="List all available attack blocking options from hypernode-systemctl block_attack",
    inputSchema={"type": "object", "properties": {}}
) 