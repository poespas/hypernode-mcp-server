"""
Generic tool base class for Hypernode MCP Server tools.
Provides common functionality that other tools can inherit from.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from utils.command_executor import CommandExecutor, CommandResult

class BaseTool(ABC):
    """
    Base class for all MCP tools in the Hypernode MCP Server.
    Automatically handles MCP registration and provides common functionality.
    """
    
    def __init__(self, mcp=None):
        self.mcp = mcp
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def register(self, mcp):
        """Register this tool with the MCP instance."""
        self.mcp = mcp
        # Get all methods that start with 'tool_'
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and attr_name.startswith('tool_'):
                # Register the method as an MCP tool
                tool_name = attr_name[5:]  # Remove 'tool_' prefix
                self.mcp.tool(attr)
                self.logger.info(f"Registered tool: {tool_name}")


class ToolRegistry:
    """
    Registry for automatically discovering and registering all tools.
    """
    
    def __init__(self):
        self.tools: List[BaseTool] = []
    
    def register_tool(self, tool: BaseTool):
        """Register a tool instance."""
        self.tools.append(tool)
    
    def register_all_tools(self, mcp):
        """Register all tools with the MCP instance."""
        for tool in self.tools:
            tool.register(mcp)

# Global registry instance
tool_registry = ToolRegistry()