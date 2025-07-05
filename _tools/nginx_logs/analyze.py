"""
Tool for analyzing nginx logs using pnl (hypernode-parse-nginx-log).
"""

import asyncio
from typing import Dict, Any, List, Optional
from mcp import Tool
from utils.command_executor import CommandExecutor

async def analyze_nginx_logs_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze nginx logs using pnl with various options.
    
    Args:
        date_range: Date range to analyze (today, yesterday, days_ago, date)
        days_ago: Number of days ago (if date_range is days_ago)
        specific_date: Specific date in YYYY-MM-DD format (if date_range is date)
        fields: Comma-separated list of fields to display
        filters: List of filter conditions (field=value, field~regex, field!~regex)
        format: Output format string
        php_only: Filter for PHP requests only
        bots_only: Filter for bot requests only
        limit: Limit number of results
        filename: Specific log file to analyze
        
    Returns:
        Dict containing the log analysis results
    """
    # Build command parts
    command_parts = ["pnl"]
    
    # Add date range
    date_range = arguments.get("date_range")
    if date_range:
        if date_range == "today":
            command_parts.append("--today")
        elif date_range == "yesterday":
            command_parts.append("--yesterday")
        elif date_range == "days_ago":
            days_ago = arguments.get("days_ago", 1)
            command_parts.extend(["--days-ago", str(days_ago)])
        elif date_range == "date":
            specific_date = arguments.get("specific_date")
            if specific_date:
                command_parts.extend(["--date", specific_date])
    
    # Add specific filename if provided
    filename = arguments.get("filename")
    if filename:
        command_parts.extend(["--filename", filename])
    
    # Add fields
    fields = arguments.get("fields")
    if fields:
        command_parts.extend(["--fields", fields])
    
    # Add filters
    filters = arguments.get("filters", [])
    for filter_condition in filters:
        command_parts.extend(["--filter", filter_condition])
    
    # Add format
    format_str = arguments.get("format")
    if format_str:
        command_parts.extend(["--format", format_str])
    
    # Add PHP only filter
    php_only = arguments.get("php_only", False)
    if php_only:
        command_parts.append("--php")
    
    # Add bots only filter
    bots_only = arguments.get("bots_only", False)
    if bots_only:
        command_parts.append("--bots")
    
    # Add verbose output
    verbose = arguments.get("verbose", False)
    if verbose:
        command_parts.append("--verbose")
    
    # Add NCSA format
    ncsa_format = arguments.get("ncsa_format", False)
    if ncsa_format:
        command_parts.append("--ncsa")
    
    command = " ".join(command_parts)
    
    # Execute the command
    result = await CommandExecutor.execute_command(command, timeout=120)
    
    # Parse the output
    if result.success:
        lines = result.stdout.strip().split('\n')
        log_entries = []
        
        for line in lines:
            if line.strip():
                log_entries.append(line.strip())
        
        return {
            "success": True,
            "command": command,
            "log_entries": log_entries,
            "count": len(log_entries),
            "raw_output": result.stdout
        }
    else:
        return {
            "success": False,
            "command": command,
            "error": result.stderr,
            "return_code": result.return_code
        }

# Tool instance
analyze_nginx_logs = Tool(
    name="analyze_nginx_logs",
    description="Analyze nginx logs using pnl with filters, date ranges, and field selection",
    inputSchema={
        "type": "object",
        "properties": {
            "date_range": {"type": "string", "description": "Date range to analyze (today, yesterday, days_ago, date)"},
            "days_ago": {"type": "integer", "description": "Number of days ago (if date_range is days_ago)"},
            "specific_date": {"type": "string", "description": "Specific date in YYYY-MM-DD format (if date_range is date)"},
            "fields": {"type": "string", "description": "Comma-separated list of fields to display"},
            "filters": {"type": "array", "items": {"type": "string"}, "description": "List of filter conditions (field=value, field~regex, field!~regex)"},
            "format": {"type": "string", "description": "Output format string"},
            "php_only": {"type": "boolean", "description": "Filter for PHP requests only"},
            "bots_only": {"type": "boolean", "description": "Filter for bot requests only"},
            "limit": {"type": "integer", "description": "Limit number of results"},
            "filename": {"type": "string", "description": "Specific log file to analyze"},
            "verbose": {"type": "boolean", "description": "Verbose output"},
            "ncsa_format": {"type": "boolean", "description": "NCSA format output"}
        }
    }
) 