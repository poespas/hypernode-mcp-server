"""
Hypernode MCP Server with HTTP and SSE support using FastMCP 2.0.
"""

from fastmcp import FastMCP
import logging
import os
from typing import Dict, Any, Optional
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Hypernode MCP Server")

# Import command executor utility
from utils.command_executor import CommandExecutor

# Auto-register all tools
from tools import register_all_tools
register_all_tools(mcp)

@mcp.tool
async def list_vhosts() -> Dict[str, Any]:
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

@mcp.tool
async def modify_vhost(vhost: str, action: str, value: str) -> Dict[str, Any]:
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

@mcp.tool
async def list_incidents() -> Dict[str, Any]:
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

@mcp.tool
async def get_incident(date: str, file_pattern: str = "*") -> Dict[str, Any]:
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

@mcp.tool
async def list_attacks() -> Dict[str, Any]:
    """
    List all available attack blocking options on the Hypernode.
    
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

@mcp.tool
async def block_attack(attack_type: str) -> Dict[str, Any]:
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

@mcp.tool
async def analyze_nginx_logs(filter: Optional[str] = None, limit: int = 100, today: bool = False, unique_by_field: Optional[str] = None, query_bots_only: bool = False) -> Dict[str, Any]:
    """
    Analyze nginx logs with optional filters.
    
    Args:
        filter: Filter to apply. Format: <field>=<str> or <field>~<regex> or <field>!~<regex> (optional)
        limit: Number of lines to analyze (default: 100)
        today: Whether to analyze only today's logs (default: False)
        unique_by_field: Field to count and group unique occurrences by (e.g., "remote_addr", "user_agent")
        query_bots_only: Whether to analyze only bot traffic (default: False)
    
    Returns:
        Dict containing the log analysis results
    """
    # Build the base command
    command = "hypernode-parse-nginx-log"
    
    if today:
        command += " --today"
    
    if query_bots_only:
        command += " --bots"
    
    if filter:
        command += f" --filter \"{filter}\""
    
    # If we need to pipe commands, use a temporary script file
    if unique_by_field or limit > 0:
        if unique_by_field:
            command += f" --fields {unique_by_field}"

        # Create a temporary script to handle the piping
        script_content = f"#!/bin/bash\n{command}"
        
        if unique_by_field:
            script_content += f" | sort | uniq -c | sort -nr"
        
        if limit > 0:
            script_content += f" | head -n {limit}"
        
        # Write script to temporary file and execute
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(script_content)
            temp_script = f.name
        
        try:
            # Make script executable and run it
            os.chmod(temp_script, 0o755)
            result = await CommandExecutor.execute_command(f"bash {temp_script}", timeout=120)
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_script)
            except:
                pass
    else:
        result = await CommandExecutor.execute_command(command, timeout=120)
    
    return {
        "success": result.success,
        "result": result.stdout if result.success else result.stderr,
        "filter": filter,
        "limit": limit,
        "today": today,
        "unique_by_field": unique_by_field,
        "query_bots_only": query_bots_only
    }

@mcp.tool
async def analyze_nginx_logs_fields() -> Dict[str, Any]:
    """
    List available fields for nginx log analysis using pnl --list-fields.
    
    Returns:
        Dict containing the list of available fields for nginx log analysis
    """
    command = "hypernode-parse-nginx-log --list-fields"
    
    result = await CommandExecutor.execute_command(command)
    
    if not result.success:
        return {
            "success": False,
            "error": result.stderr,
            "fields": []
        }
    
    # Parse the output to extract field names
    output = result.stdout.strip()
    fields = []
    
    if "Available fields:" in output:
        # Extract fields after "Available fields:"
        fields_part = output.split("Available fields:")[1].strip()
        fields = [field.strip() for field in fields_part.split(", ")]
    
    return {
        "success": True,
        "fields": fields,
        "count": len(fields),
        "raw_output": output
    }

@mcp.tool
async def execute_shell_command(command: str) -> Dict[str, Any]:
    """
    Execute a shell command safely (dangerous commands are blocked).
    
    Args:
        command: Shell command to execute
    
    Returns:
        Dict containing the command execution result
    """
    result = await CommandExecutor.execute_command(command)
    
    return {
        "success": result.success,
        "result": result.stdout if result.success else result.stderr,
        "command": command
    }

if __name__ == "__main__":
    # Run with STDIO transport (FastMCP 2.0 syntax)
    # TODO: add parameters for other transports
    mcp.run(transport="stdio")