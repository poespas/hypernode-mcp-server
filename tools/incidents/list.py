"""
Incident listing tool for Hypernode MCP Server.
"""

import os
from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class IncidentsListTool(BaseTool):
    """Incident listing tool implementation."""
    
    async def tool_list_incidents(self) -> Dict[str, Any]:
        """
        List all incidents in the ~/incidents directory.
        
        Returns:
            Dict containing the list of incidents
        """
        incidents_dir = os.path.expanduser("~/incidents")
        
        # Check if incidents directory exists
        if not os.path.exists(incidents_dir):
            return {
                "success": True,
                "incidents": [],
                "count": 0,
                "message": "Incidents directory does not exist"
            }
        
        command = f"ls -la {incidents_dir}"
        result = await CommandExecutor.execute_command(command)
        
        if not result.success:
            return {
                "success": False,
                "error": result.stderr,
                "incidents": []
            }
        
        # Parse the ls output to get file details
        lines = result.stdout.strip().split('\n')
        incidents = []
        
        for line in lines[1:]:  # Skip the total line
            if line.strip():
                parts = line.split()
                if len(parts) >= 9:
                    permissions = parts[0]
                    size = parts[4]
                    date = f"{parts[5]} {parts[6]} {parts[7]}"
                    name = parts[8]
                    
                    # Skip . and .. directories and README.txt
                    if name in ['.', '..', 'README.txt']:
                        continue
                    
                    incidents.append({
                        "name": name,
                        "permissions": permissions,
                        "size": size,
                        "date": date,
                        "is_directory": permissions.startswith('d')
                    })
        
        return {
            "success": True,
            "incidents": incidents,
            "count": len(incidents),
            "directory": incidents_dir
        }

# Create and register the tool instance automatically
incidents_list_tool = IncidentsListTool()
tool_registry.register_tool(incidents_list_tool) 