"""
Tool for modifying vhosts using hypernode-manage-vhosts.
"""

import asyncio
from typing import Dict, Any, Optional, List
from mcp import Tool
from utils.command_executor import CommandExecutor

async def modify_vhost_handler(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modify vhost configurations using hypernode-manage-vhosts.
    
    Args:
        servername: The vhost name to modify
        action: The action to perform (create, delete, update_ssl, etc.)
        vhost_type: Type of vhost (magento2, wordpress, etc.)
        webroot: Webroot directory path
        https: Enable/disable HTTPS
        force_https: Force HTTPS redirect
        varnish: Enable/disable Varnish
        handler: PHP handler (phpfpm, phpfpm74alt, etc.)
        ssl_config: SSL configuration (modern, intermediate)
        
    Returns:
        Dict containing the operation result
    """
    servername = arguments.get("servername")
    action = arguments.get("action", "create")
    
    if not servername:
        return {
            "success": False,
            "error": "servername is required"
        }
    
    if not CommandExecutor.validate_vhost_name(servername):
        return {
            "success": False,
            "error": f"Invalid vhost name format: {servername}"
        }
    
    # Build command based on action
    command_parts = ["hypernode-manage-vhosts", servername]
    
    if action == "delete":
        command_parts.append("--delete")
        command_parts.append("--yes")  # Auto-confirm deletion
    else:
        # Add type if specified
        vhost_type = arguments.get("vhost_type")
        if vhost_type:
            command_parts.extend(["--type", vhost_type])
        
        # Add webroot if specified
        webroot = arguments.get("webroot")
        if webroot:
            command_parts.extend(["--webroot", webroot])
        
        # Add HTTPS settings
        https = arguments.get("https")
        if https is not None:
            if https:
                command_parts.append("--https")
            else:
                command_parts.append("--disable-https")
        
        # Add force HTTPS
        force_https = arguments.get("force_https")
        if force_https is not None:
            if force_https:
                command_parts.append("--force-https")
            else:
                command_parts.append("--disable-force-https")
        
        # Add Varnish settings
        varnish = arguments.get("varnish")
        if varnish is not None:
            if varnish:
                command_parts.append("--varnish")
            else:
                command_parts.append("--disable-varnish")
        
        # Add PHP handler
        handler = arguments.get("handler")
        if handler:
            command_parts.extend(["--handler", handler])
        
        # Add SSL configuration
        ssl_config = arguments.get("ssl_config")
        if ssl_config:
            command_parts.extend(["--ssl-config", ssl_config])
        
        # Add default server setting
        default_server = arguments.get("default_server")
        if default_server:
            command_parts.append("--default-server")
    
    command = " ".join(command_parts)
    
    result = await CommandExecutor.execute_command(command, timeout=60)
    
    return {
        "success": result.success,
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "return_code": result.return_code,
        "action": action,
        "servername": servername
    }

# Tool instance
modify_vhost = Tool(
    name="modify_vhost",
    description="Modify vhost configurations (create, update, delete, SSL settings, etc.)",
    inputSchema={
        "type": "object",
        "properties": {
            "servername": {"type": "string", "description": "The vhost name to modify"},
            "action": {"type": "string", "description": "The action to perform (create, delete, update_ssl, etc.)", "default": "create"},
            "vhost_type": {"type": "string", "description": "Type of vhost (magento2, wordpress, etc.)"},
            "webroot": {"type": "string", "description": "Webroot directory path"},
            "https": {"type": "boolean", "description": "Enable/disable HTTPS"},
            "force_https": {"type": "boolean", "description": "Force HTTPS redirect"},
            "varnish": {"type": "boolean", "description": "Enable/disable Varnish"},
            "handler": {"type": "string", "description": "PHP handler (phpfpm, phpfpm74alt, etc.)"},
            "ssl_config": {"type": "string", "description": "SSL configuration (modern, intermediate)"},
            "default_server": {"type": "boolean", "description": "Set as default server"}
        },
        "required": ["servername"]
    }
) 