"""
Tools package for Hypernode MCP Server.
"""

import importlib
import pkgutil
from .generic import tool_registry

def register_all_tools(mcp):
    """Auto-register all tools from all modules in this package."""
    
    # Import all modules in this package
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        if module_name != '__init__':
            importlib.import_module(f'.{module_name}', __package__)
    
    # Register all tools with the MCP instance
    tool_registry.register_all_tools(mcp)
