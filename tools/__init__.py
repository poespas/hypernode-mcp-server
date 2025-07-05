"""
Tools package for Hypernode MCP Server.
"""

import importlib
import pkgutil
import os
from pathlib import Path
from .generic import tool_registry

def register_all_tools(mcp):
    """Auto-register all tools from all modules in this package and subpackages."""
    
    # Get the current package directory
    package_dir = Path(__file__).parent
    
    # Recursively find and import all Python modules
    for root, dirs, files in os.walk(package_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                # Get the relative path from the package root
                rel_path = Path(root).relative_to(package_dir)
                module_path = rel_path / file[:-3]  # Remove .py extension
                
                # Convert path to module import string
                module_name = str(module_path).replace(os.sep, '.')
                
                try:
                    # Import the module
                    importlib.import_module(f'.{module_name}', __package__)
                except ImportError as e:
                    # Log import errors but continue with other modules
                    print(f"Warning: Could not import {module_name}: {e}")
    
    # Register all tools with the MCP instance
    tool_registry.register_all_tools(mcp)
