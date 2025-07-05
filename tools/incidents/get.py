"""
Incident retrieval tool for Hypernode MCP Server.
"""

import os
from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class IncidentsGetTool(BaseTool):
    """Incident retrieval tool implementation."""
    
    async def tool_get_incident(self, date: str, file_pattern: str = "*") -> Dict[str, Any]:
        """
        Get files from a specific incident directory.
        
        Args:
            date: The incident date/directory name
            file_pattern: Optional file pattern to filter files (e.g., "*.log")
        
        Returns:
            Dict containing the incident files and their contents
        """
        incidents_dir = os.path.expanduser("~/incidents")
        incident_path = os.path.join(incidents_dir, date)
        
        # Check if incident directory exists
        if not os.path.exists(incident_path):
            return {
                "success": False,
                "error": f"Incident directory does not exist: {incident_path}",
                "incident_path": incident_path
            }
        
        # List files in the incident directory
        list_command = f"ls -la {incident_path}/{file_pattern}"
        result = await CommandExecutor.execute_command(list_command)
        
        if not result.success:
            return {
                "success": False,
                "error": f"Failed to list files: {result.stderr}",
                "incident_path": incident_path
            }
        
        # Parse the ls output to get file details
        lines = result.stdout.strip().split('\n')
        files = []
        
        for line in lines[1:]:  # Skip the total line
            if line.strip():
                parts = line.split()
                if len(parts) >= 9:
                    permissions = parts[0]
                    size = parts[4]
                    date_str = f"{parts[5]} {parts[6]} {parts[7]}"
                    name = parts[8]
                    
                    # Skip . and .. directories
                    if name in ['.', '..']:
                        continue
                    
                    file_info = {
                        "name": name,
                        "permissions": permissions,
                        "size": size,
                        "date": date_str,
                        "is_directory": permissions.startswith('d'),
                        "full_path": os.path.join(incident_path, name)
                    }
                    
                    # Get file content if it's a regular file and not too large
                    if not file_info["is_directory"] and int(size) < 1024 * 1024:  # Less than 1MB
                        try:
                            with open(file_info["full_path"], 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                file_info["content"] = content[:10000]  # Limit to first 10KB
                                file_info["content_truncated"] = len(content) > 10000
                        except Exception as e:
                            file_info["content_error"] = str(e)
                    
                    files.append(file_info)
        
        return {
            "success": True,
            "incident_date": date,
            "incident_path": incident_path,
            "files": files,
            "count": len(files),
            "file_pattern": file_pattern
        }

# Create and register the tool instance automatically
incidents_get_tool = IncidentsGetTool()
tool_registry.register_tool(incidents_get_tool) 