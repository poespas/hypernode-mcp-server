"""
Tool for getting incident files from ~/incidents/[date]/*.
"""

import asyncio
import os
from typing import Dict, Any, List
from mcp import Tool
from utils.command_executor import CommandExecutor

async def get_incident_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get files from a specific incident directory.
    
    Args:
        date: The incident date/directory name
        file_pattern: Optional file pattern to filter files (e.g., "*.log")
        
    Returns:
        Dict containing the incident files and their contents
    """
    date = arguments.get("date")
    file_pattern = arguments.get("file_pattern", "*")
    
    if not date:
        return {
            "success": False,
            "error": "date parameter is required"
        }
    
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
    list_result = await CommandExecutor.execute_command(list_command)
    
    if not list_result.success:
        return {
            "success": False,
            "error": f"Failed to list files: {list_result.stderr}",
            "incident_path": incident_path
        }
    
    # Parse the ls output to get file details
    lines = list_result.stdout.strip().split('\n')
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

# Tool instance
get_incident = Tool(
    name="get_incident",
    description="Get files from a specific incident directory ~/incidents/[date]/*",
    inputSchema={
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "The incident date/directory name"},
            "file_pattern": {"type": "string", "description": "Optional file pattern to filter files (e.g., '*.log')", "default": "*"}
        },
        "required": ["date"]
    }
) 