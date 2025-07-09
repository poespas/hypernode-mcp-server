"""
Tests for the Nginx Logs Fields tool.
"""

import pytest
import asyncio
from unittest.mock import patch
from tools.nginx_logs.fields import NginxLogsFieldsTool
from utils.command_executor import CommandResult

class TestNginxLogsFieldsTool:
    """Test cases for NginxLogsFieldsTool."""

    @pytest.fixture
    def nginx_logs_fields_tool(self):
        """Create a NginxLogsFieldsTool instance for testing."""
        return NginxLogsFieldsTool()

    def test_nginx_logs_fields_tool_creation(self, nginx_logs_fields_tool):
        """Test that NginxLogsFieldsTool can be instantiated."""
        assert isinstance(nginx_logs_fields_tool, NginxLogsFieldsTool)

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_success(self, mock_execute_command, nginx_logs_fields_tool):
        """Test successful field listing."""
        # Mock successful response with field data
        mock_output = (
            "hypernode-parse-nginx-log --list-fields\n\n"
            "Available fields: remote_user, ssl_protocol, referer, user_agent, "
            "remote_addr, ssl_cipher, body_bytes_sent, country, status, time, "
            "request_time, port, request, server_name, host, handler"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is True
        assert result["count"] == 16
        assert len(result["fields"]) == 16
        
        expected_fields = [
            "remote_user", "ssl_protocol", "referer", "user_agent",
            "remote_addr", "ssl_cipher", "body_bytes_sent", "country",
            "status", "time", "request_time", "port", "request",
            "server_name", "host", "handler"
        ]
        
        for field in expected_fields:
            assert field in result["fields"]
        
        mock_execute_command.assert_called_once_with("hypernode-parse-nginx-log --list-fields")

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_failure(self, mock_execute_command, nginx_logs_fields_tool):
        """Test field listing failure."""
        # Mock failure response
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Command not found: hypernode-parse-nginx-log",
            return_code=127,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is False
        assert result["fields"] == []
        assert "error" in result
        assert result["error"] == "Command not found: hypernode-parse-nginx-log"

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_empty_result(self, mock_execute_command, nginx_logs_fields_tool):
        """Test field listing with no fields found."""
        # Mock response with no field data
        mock_output = "hypernode-parse-nginx-log --list-fields\n\nNo fields available."
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is True
        assert result["fields"] == []
        assert result["count"] == 0
        assert "raw_output" in result

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_malformed_output(self, mock_execute_command, nginx_logs_fields_tool):
        """Test field listing with malformed output."""
        # Mock response with malformed data
        mock_output = (
            "hypernode-parse-nginx-log --list-fields\n\n"
            "Some other output without Available fields section"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is True
        assert result["fields"] == []
        assert result["count"] == 0

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_partial_output(self, mock_execute_command, nginx_logs_fields_tool):
        """Test field listing with partial field data."""
        # Mock response with partial field data
        mock_output = (
            "hypernode-parse-nginx-log --list-fields\n\n"
            "Available fields: remote_addr, status, request"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is True
        assert result["count"] == 3
        assert len(result["fields"]) == 3
        
        expected_fields = ["remote_addr", "status", "request"]
        for field in expected_fields:
            assert field in result["fields"]

    @patch('tools.nginx_logs.fields.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_fields_with_extra_whitespace(self, mock_execute_command, nginx_logs_fields_tool):
        """Test field listing with extra whitespace in output."""
        # Mock response with extra whitespace
        mock_output = (
            "hypernode-parse-nginx-log --list-fields\n\n"
            "Available fields:  remote_user ,  ssl_protocol ,  referer  ,  user_agent  "
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-parse-nginx-log --list-fields"
        )
        
        result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
        
        assert result["success"] is True
        assert result["count"] == 4
        assert len(result["fields"]) == 4
        
        expected_fields = ["remote_user", "ssl_protocol", "referer", "user_agent"]
        for field in expected_fields:
            assert field in result["fields"]

    def test_nginx_logs_fields_tool_class_attributes(self, nginx_logs_fields_tool):
        """Test that NginxLogsFieldsTool has the expected class structure."""
        assert hasattr(nginx_logs_fields_tool, 'tool_analyze_nginx_logs_fields')
        assert callable(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields)

    def test_nginx_logs_fields_tool_return_structure(self, nginx_logs_fields_tool):
        """Test that tool_analyze_nginx_logs_fields returns the correct data structure."""
        with patch('tools.nginx_logs.fields.CommandExecutor.execute_command') as mock_execute_command:
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="Available fields: remote_addr, status",
                stderr="",
                return_code=0,
                command="hypernode-parse-nginx-log --list-fields"
            )
            
            result = asyncio.run(nginx_logs_fields_tool.tool_analyze_nginx_logs_fields())
            
            required_keys = {"success", "fields", "count", "raw_output"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["fields"], list)
            assert isinstance(result["count"], int)
            assert isinstance(result["raw_output"], str) 