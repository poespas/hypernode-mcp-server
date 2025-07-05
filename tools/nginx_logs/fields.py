"""
Nginx log fields tool for Hypernode MCP Server.
"""

from typing import Dict, Any
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class NginxLogsFieldsTool(BaseTool):
    """Nginx log fields tool implementation."""
    
    async def tool_analyze_nginx_logs_fields(self) -> Dict[str, Any]:
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

# Create and register the tool instance automatically
nginx_logs_fields_tool = NginxLogsFieldsTool()
tool_registry.register_tool(nginx_logs_fields_tool) 