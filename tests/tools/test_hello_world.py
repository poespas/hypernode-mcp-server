"""
Tests for the Hello World tool.
"""

import pytest
import asyncio
from tools.hello_world import HelloWorldTool


class TestHelloWorldTool:
    """Test cases for HelloWorldTool."""

    @pytest.fixture
    def hello_world_tool(self):
        """Create a HelloWorldTool instance for testing."""
        return HelloWorldTool()

    def test_hello_world_tool_creation(self, hello_world_tool):
        """Test that HelloWorldTool can be instantiated."""
        assert isinstance(hello_world_tool, HelloWorldTool)

    def test_hello_world_tool_method(self, hello_world_tool):
        """Test the tool_hello_world method returns expected data."""
        result = asyncio.run(hello_world_tool.tool_hello_world())
        assert isinstance(result, dict)
        assert "message" in result
        assert "status" in result
        assert result["message"] == "Hello World from Hypernode MCP Server!"
        assert result["status"] == "success"

    def test_hello_world_tool_method_structure(self, hello_world_tool):
        """Test that the tool_hello_world method returns the correct data structure."""
        result = asyncio.run(hello_world_tool.tool_hello_world())
        required_keys = {"message", "status"}
        assert set(result.keys()) == required_keys
        assert isinstance(result["message"], str)
        assert isinstance(result["status"], str)

    def test_hello_world_tool_class_attributes(self, hello_world_tool):
        """Test that HelloWorldTool has the expected class structure."""
        assert hasattr(hello_world_tool, 'tool_hello_world')
        assert callable(hello_world_tool.tool_hello_world)

    def test_hello_world_tool_consistency(self, hello_world_tool):
        """Test that multiple calls to tool_hello_world return consistent results."""
        result1 = asyncio.run(hello_world_tool.tool_hello_world())
        result2 = asyncio.run(hello_world_tool.tool_hello_world())
        assert result1 == result2
        assert result1["message"] == result2["message"]
        assert result1["status"] == result2["status"] 