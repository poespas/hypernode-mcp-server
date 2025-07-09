"""
Tests for the VHosts List tool.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from tools.vhosts.list import VHostsListTool


class TestVHostsListTool:
    """Test cases for VHostsListTool."""

    @pytest.fixture
    def vhosts_list_tool(self):
        """Create a VHostsListTool instance for testing."""
        return VHostsListTool()

    def test_vhosts_list_tool_creation(self, vhosts_list_tool):
        """Test that VHostsListTool can be instantiated."""
        assert isinstance(vhosts_list_tool, VHostsListTool)

    @patch('tools.vhosts.list.CommandExecutor.execute_json_command')
    def test_list_vhosts_success(self, mock_execute_json, vhosts_list_tool):
        """Test successful vhost listing."""
        # Mock successful response
        mock_vhosts = {
            "example.hypernode.io": {
                "default_server": False,
                "force_https": True,
                "https": True,
                "ssl_config": "intermediate",
                "type": "magento2",
                "varnish": False
            }
        }
        mock_execute_json.return_value = (True, mock_vhosts)
        
        result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
        
        assert result["success"] is True
        assert result["vhosts"] == mock_vhosts
        assert result["count"] == 1
        mock_execute_json.assert_called_once_with("hypernode-manage-vhosts --list --format json")

    @patch('tools.vhosts.list.CommandExecutor.execute_json_command')
    def test_list_vhosts_failure(self, mock_execute_json, vhosts_list_tool):
        """Test vhost listing failure."""
        # Mock failure response
        mock_execute_json.return_value = (False, "Command failed")
        
        result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
        
        assert result["success"] is False
        assert result["error"] == "Command failed"
        assert result["vhosts"] == {}
        mock_execute_json.assert_called_once_with("hypernode-manage-vhosts --list --format json")

    @patch('tools.vhosts.list.CommandExecutor.execute_json_command')
    def test_list_vhosts_empty_result(self, mock_execute_json, vhosts_list_tool):
        """Test vhost listing with empty result."""
        # Mock empty response
        mock_execute_json.return_value = (True, {})
        
        result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
        
        assert result["success"] is True
        assert result["vhosts"] == {}
        assert result["count"] == 0

    @patch('tools.vhosts.list.CommandExecutor.execute_json_command')
    def test_list_vhosts_multiple_vhosts(self, mock_execute_json, vhosts_list_tool):
        """Test vhost listing with multiple vhosts."""
        # Mock multiple vhosts response
        mock_vhosts = {
            "site1.hypernode.io": {"type": "magento2", "https": True},
            "site2.hypernode.io": {"type": "wordpress", "https": False},
            "site3.hypernode.io": {"type": "custom", "https": True}
        }
        mock_execute_json.return_value = (True, mock_vhosts)
        
        result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
        
        assert result["success"] is True
        assert result["vhosts"] == mock_vhosts
        assert result["count"] == 3

    @patch('tools.vhosts.list.CommandExecutor.execute_json_command')
    def test_list_vhosts_non_dict_result(self, mock_execute_json, vhosts_list_tool):
        """Test vhost listing with non-dict result."""
        # Mock non-dict response
        mock_execute_json.return_value = (True, "not a dict")
        
        result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
        
        assert result["success"] is True
        assert result["vhosts"] == "not a dict"
        assert result["count"] == 0

    def test_vhosts_list_tool_class_attributes(self, vhosts_list_tool):
        """Test that VHostsListTool has the expected class structure."""
        assert hasattr(vhosts_list_tool, 'tool_list_vhosts')
        assert callable(vhosts_list_tool.tool_list_vhosts)

    def test_vhosts_list_tool_return_structure(self, vhosts_list_tool):
        """Test that tool_list_vhosts returns the correct data structure."""
        with patch('tools.vhosts.list.CommandExecutor.execute_json_command') as mock_execute_json:
            mock_execute_json.return_value = (True, {})
            result = asyncio.run(vhosts_list_tool.tool_list_vhosts())
            
            required_keys = {"success", "vhosts", "count"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["count"], int) 