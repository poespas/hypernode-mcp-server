"""
Tests for the Nginx Logs Analyze tool.
"""

import pytest
import asyncio
from unittest.mock import patch, mock_open, MagicMock
from tools.nginx_logs.analyze import NginxLogsAnalyzeTool
from utils.command_executor import CommandResult

class TestNginxLogsAnalyzeTool:
    """Test cases for NginxLogsAnalyzeTool."""

    @pytest.fixture
    def nginx_logs_analyze_tool(self):
        """Create a NginxLogsAnalyzeTool instance for testing."""
        return NginxLogsAnalyzeTool()

    def test_nginx_logs_analyze_tool_creation(self, nginx_logs_analyze_tool):
        """Test that NginxLogsAnalyzeTool can be instantiated."""
        assert isinstance(nginx_logs_analyze_tool, NginxLogsAnalyzeTool)

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_basic(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test basic nginx log analysis without filters."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="192.168.1.1 - - [01/Jan/2024:00:00:00 +0000] \"GET / HTTP/1.1\" 200 1234",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs())
        
        assert result["success"] is True
        assert result["filter"] is None
        assert result["limit"] == 100
        assert result["today"] is False
        assert result["unique_by_field"] is None
        assert result["query_bots_only"] is False
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_with_filter(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis with a filter."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="192.168.1.1 - - [01/Jan/2024:00:00:00 +0000] \"GET / HTTP/1.1\" 404 1234",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(filter="status=404"))
        
        assert result["success"] is True
        assert result["filter"] == "status=404"
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_today_only(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis for today only."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Today's logs: 192.168.1.1 - - [01/Jan/2024:00:00:00 +0000] \"GET / HTTP/1.1\" 200 1234",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(today=True))
        
        assert result["success"] is True
        assert result["today"] is True
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_bots_only(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis for bots only."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Bot traffic: Googlebot - - [01/Jan/2024:00:00:00 +0000] \"GET / HTTP/1.1\" 200 1234",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(query_bots_only=True))
        
        assert result["success"] is True
        assert result["query_bots_only"] is True
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_with_unique_field(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis with unique_by_field."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="      5 192.168.1.1\n      3 192.168.1.2\n      1 192.168.1.3",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(unique_by_field="remote_addr"))
        
        assert result["success"] is True
        assert result["unique_by_field"] == "remote_addr"
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_with_limit(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis with limit."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="192.168.1.1 - - [01/Jan/2024:00:00:00 +0000] \"GET / HTTP/1.1\" 200 1234\n192.168.1.2 - - [01/Jan/2024:00:00:01 +0000] \"GET / HTTP/1.1\" 200 1234",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(limit=50))
        
        assert result["success"] is True
        assert result["limit"] == 50
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_failure(self, mock_execute_command, nginx_logs_analyze_tool):
        """Test nginx log analysis failure."""
        # Mock failure response
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Command not found: hypernode-parse-nginx-log",
            return_code=127,
            command="hypernode-parse-nginx-log"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs())
        
        assert result["success"] is False
        assert result["result"] == "Command not found: hypernode-parse-nginx-log"

    @patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile')
    @patch('tools.nginx_logs.analyze.os.chmod')
    @patch('tools.nginx_logs.analyze.os.unlink')
    @patch('tools.nginx_logs.analyze.CommandExecutor.execute_command')
    def test_analyze_nginx_logs_complex_filter(self, mock_execute_command, mock_unlink, mock_chmod, mock_tempfile, nginx_logs_analyze_tool):
        """Test nginx log analysis with complex filter."""
        # Mock temporary file
        mock_temp_file = MagicMock()
        mock_temp_file.name = "/tmp/test_script.sh"
        mock_tempfile.return_value.__enter__.return_value = mock_temp_file
        
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Filtered results for IP range 192.168",
            stderr="",
            return_code=0,
            command="bash /tmp/test_script.sh"
        )
        
        result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs(filter="remote_addr~192.168"))
        
        assert result["success"] is True
        assert result["filter"] == "remote_addr~192.168"
        mock_chmod.assert_called_once_with("/tmp/test_script.sh", 0o755)
        mock_execute_command.assert_called_once_with("bash /tmp/test_script.sh", timeout=120)
        mock_unlink.assert_called_once_with("/tmp/test_script.sh")

    def test_nginx_logs_analyze_tool_class_attributes(self, nginx_logs_analyze_tool):
        """Test that NginxLogsAnalyzeTool has the expected class structure."""
        assert hasattr(nginx_logs_analyze_tool, 'tool_analyze_nginx_logs')
        assert callable(nginx_logs_analyze_tool.tool_analyze_nginx_logs)

    def test_nginx_logs_analyze_tool_return_structure(self, nginx_logs_analyze_tool):
        """Test that tool_analyze_nginx_logs returns the correct data structure."""
        with patch('tools.nginx_logs.analyze.tempfile.NamedTemporaryFile') as mock_tempfile, \
             patch('tools.nginx_logs.analyze.os.chmod') as mock_chmod, \
             patch('tools.nginx_logs.analyze.os.unlink') as mock_unlink, \
             patch('tools.nginx_logs.analyze.CommandExecutor.execute_command') as mock_execute_command:
            
            # Mock temporary file
            mock_temp_file = MagicMock()
            mock_temp_file.name = "/tmp/test_script.sh"
            mock_tempfile.return_value.__enter__.return_value = mock_temp_file
            
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="Test result",
                stderr="",
                return_code=0,
                command="bash /tmp/test_script.sh"
            )
            
            result = asyncio.run(nginx_logs_analyze_tool.tool_analyze_nginx_logs())
            
            required_keys = {"success", "result", "filter", "limit", "today", "unique_by_field", "query_bots_only"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["result"], str)
            assert isinstance(result["limit"], int)
            assert isinstance(result["today"], bool)
            assert isinstance(result["query_bots_only"], bool) 