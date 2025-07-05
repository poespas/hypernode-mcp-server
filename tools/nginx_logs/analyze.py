"""
Nginx log analysis tool for Hypernode MCP Server.
"""

import tempfile
import os
from typing import Dict, Any, Optional
from ..generic import BaseTool, tool_registry
from utils.command_executor import CommandExecutor

class NginxLogsAnalyzeTool(BaseTool):
    """Nginx log analysis tool implementation."""
    
    async def tool_analyze_nginx_logs(self, filter: Optional[str] = None, limit: int = 100, today: bool = False, unique_by_field: Optional[str] = None, query_bots_only: bool = False) -> Dict[str, Any]:
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

# Create and register the tool instance automatically
nginx_logs_analyze_tool = NginxLogsAnalyzeTool()
tool_registry.register_tool(nginx_logs_analyze_tool) 