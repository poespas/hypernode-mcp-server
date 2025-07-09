"""
Tests for the VHosts Modify tool.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from tools.vhosts.modify import VHostsModifyTool
from utils.command_executor import CommandResult


class TestVHostsModifyTool:
    """Test cases for VHostsModifyTool."""

    @pytest.fixture
    def vhosts_modify_tool(self):
        """Create a VHostsModifyTool instance for testing."""
        return VHostsModifyTool()

    def test_vhosts_modify_tool_creation(self, vhosts_modify_tool):
        """Test that VHostsModifyTool can be instantiated."""
        assert isinstance(vhosts_modify_tool, VHostsModifyTool)

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_enable_https(self, mock_execute_command, vhosts_modify_tool):
        """Test enabling HTTPS for a vhost."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="HTTPS enabled for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --https"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="https",
            value="true"
        ))
        
        assert result["success"] is True
        assert result["result"] == "HTTPS enabled for example.hypernode.io"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "https"
        assert result["value"] == "true"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --https"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_disable_https(self, mock_execute_command, vhosts_modify_tool):
        """Test disabling HTTPS for a vhost."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="HTTPS disabled for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --disable-https"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="https",
            value="false"
        ))
        
        assert result["success"] is True
        assert result["result"] == "HTTPS disabled for example.hypernode.io"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "https"
        assert result["value"] == "false"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --disable-https"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_change_php_version(self, mock_execute_command, vhosts_modify_tool):
        """Test changing PHP version for a vhost."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="PHP version changed to 8.1 for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --php 8.1"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="php",
            value="8.1"
        ))
        
        assert result["success"] is True
        assert result["result"] == "PHP version changed to 8.1 for example.hypernode.io"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "php"
        assert result["value"] == "8.1"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --php 8.1"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_enable_varnish(self, mock_execute_command, vhosts_modify_tool):
        """Test enabling Varnish for a vhost."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="Varnish enabled for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --varnish"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="varnish",
            value="true"
        ))
        
        assert result["success"] is True
        assert result["result"] == "Varnish enabled for example.hypernode.io"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "varnish"
        assert result["value"] == "true"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --varnish"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_disable_varnish(self, mock_execute_command, vhosts_modify_tool):
        """Test disabling Varnish for a vhost."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="Varnish disabled for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --disable-varnish"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="varnish",
            value="false"
        ))
        
        assert result["success"] is True
        assert result["result"] == "Varnish disabled for example.hypernode.io"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "varnish"
        assert result["value"] == "false"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --disable-varnish"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_failure(self, mock_execute_command, vhosts_modify_tool):
        """Test vhost modification failure."""
        # Mock failure response
        mock_result = CommandResult(
            success=False,
            stdout="",
            stderr="VHost not found: nonexistent.hypernode.io",
            return_code=1,
            command="hypernode-manage-vhosts nonexistent.hypernode.io --https"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="nonexistent.hypernode.io",
            action="https",
            value="true"
        ))
        
        assert result["success"] is False
        assert result["result"] == "VHost not found: nonexistent.hypernode.io"
        assert result["vhost"] == "nonexistent.hypernode.io"
        assert result["action"] == "https"
        assert result["value"] == "true"

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_case_insensitive_values(self, mock_execute_command, vhosts_modify_tool):
        """Test that value comparison is case insensitive."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="HTTPS enabled for example.hypernode.io",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --https"
        )
        mock_execute_command.return_value = mock_result
        
        # Test with uppercase values
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="https",
            value="TRUE"
        ))
        
        assert result["success"] is True
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --https"
        )

    @patch('tools.vhosts.modify.CommandExecutor.execute_command')
    def test_modify_vhost_custom_value(self, mock_execute_command, vhosts_modify_tool):
        """Test vhost modification with custom value."""
        # Mock successful response
        mock_result = CommandResult(
            success=True,
            stdout="Custom setting applied",
            stderr="",
            return_code=0,
            command="hypernode-manage-vhosts example.hypernode.io --custom-setting custom-value"
        )
        mock_execute_command.return_value = mock_result
        
        result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
            vhost="example.hypernode.io",
            action="custom-setting",
            value="custom-value"
        ))
        
        assert result["success"] is True
        assert result["result"] == "Custom setting applied"
        assert result["vhost"] == "example.hypernode.io"
        assert result["action"] == "custom-setting"
        assert result["value"] == "custom-value"
        mock_execute_command.assert_called_once_with(
            "hypernode-manage-vhosts example.hypernode.io --custom-setting custom-value"
        )

    def test_vhosts_modify_tool_class_attributes(self, vhosts_modify_tool):
        """Test that VHostsModifyTool has the expected class structure."""
        assert hasattr(vhosts_modify_tool, 'tool_modify_vhost')
        assert callable(vhosts_modify_tool.tool_modify_vhost)

    def test_vhosts_modify_tool_return_structure(self, vhosts_modify_tool):
        """Test that tool_modify_vhost returns the correct data structure."""
        with patch('tools.vhosts.modify.CommandExecutor.execute_command') as mock_execute_command:
            mock_result = CommandResult(
                success=True,
                stdout="Test result",
                stderr="",
                return_code=0,
                command="hypernode-manage-vhosts test.hypernode.io --test test"
            )
            mock_execute_command.return_value = mock_result
            
            result = asyncio.run(vhosts_modify_tool.tool_modify_vhost(
                vhost="test.hypernode.io",
                action="test",
                value="test"
            ))
            
            required_keys = {"success", "result", "vhost", "action", "value"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["vhost"], str)
            assert isinstance(result["action"], str)
            assert isinstance(result["value"], str) 