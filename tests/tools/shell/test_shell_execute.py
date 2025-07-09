"""
Tests for the Shell Execute tool.
"""

import pytest
import asyncio
from unittest.mock import patch
from tools.shell.execute import ShellExecuteTool
from utils.command_executor import CommandResult

class TestShellExecuteTool:
    """Test cases for ShellExecuteTool."""

    @pytest.fixture
    def shell_execute_tool(self):
        """Create a ShellExecuteTool instance for testing."""
        return ShellExecuteTool()

    def test_shell_execute_tool_creation(self, shell_execute_tool):
        """Test that ShellExecuteTool can be instantiated."""
        assert isinstance(shell_execute_tool, ShellExecuteTool)

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_success(self, mock_execute_command, shell_execute_tool):
        """Test successful shell command execution."""
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="file1.txt\nfile2.txt\nfile3.txt",
            stderr="",
            return_code=0,
            command="ls -la"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("ls -la"))
        
        assert result["success"] is True
        assert result["result"] == "file1.txt\nfile2.txt\nfile3.txt"
        assert result["command"] == "ls -la"
        mock_execute_command.assert_called_once_with("ls -la")

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_failure(self, mock_execute_command, shell_execute_tool):
        """Test shell command execution failure."""
        # Mock failure response
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="ls: cannot access 'nonexistent': No such file or directory",
            return_code=2,
            command="ls nonexistent"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("ls nonexistent"))
        
        assert result["success"] is False
        assert result["result"] == "ls: cannot access 'nonexistent': No such file or directory"
        assert result["command"] == "ls nonexistent"
        mock_execute_command.assert_called_once_with("ls nonexistent")

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_with_output(self, mock_execute_command, shell_execute_tool):
        """Test shell command with mixed stdout and stderr."""
        # Mock response with both stdout and stderr
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Current directory contents:",
            stderr="Warning: some files may be hidden",
            return_code=0,
            command="ls -la"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("ls -la"))
        
        assert result["success"] is True
        assert result["result"] == "Current directory contents:"  # Should use stdout when successful
        assert result["command"] == "ls -la"

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_permission_denied(self, mock_execute_command, shell_execute_tool):
        """Test shell command with permission denied."""
        # Mock permission denied
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Permission denied",
            return_code=13,
            command="sudo rm -rf /"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("sudo rm -rf /"))
        
        assert result["success"] is False
        assert result["result"] == "Permission denied"
        assert result["command"] == "sudo rm -rf /"

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_not_found(self, mock_execute_command, shell_execute_tool):
        """Test shell command not found."""
        # Mock command not found
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="command not found: nonexistentcommand",
            return_code=127,
            command="nonexistentcommand"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("nonexistentcommand"))
        
        assert result["success"] is False
        assert result["result"] == "command not found: nonexistentcommand"
        assert result["command"] == "nonexistentcommand"

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_with_arguments(self, mock_execute_command, shell_execute_tool):
        """Test shell command with complex arguments."""
        # Mock successful response with complex command
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Total disk usage: 1.2GB",
            stderr="",
            return_code=0,
            command="du -sh /var/log"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("du -sh /var/log"))
        
        assert result["success"] is True
        assert result["result"] == "Total disk usage: 1.2GB"
        assert result["command"] == "du -sh /var/log"
        mock_execute_command.assert_called_once_with("du -sh /var/log")

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_with_pipes(self, mock_execute_command, shell_execute_tool):
        """Test shell command with pipes."""
        # Mock successful response with piped command
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="file1.txt\nfile2.txt",
            stderr="",
            return_code=0,
            command="ls | grep .txt"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("ls | grep .txt"))
        
        assert result["success"] is True
        assert result["result"] == "file1.txt\nfile2.txt"
        assert result["command"] == "ls | grep .txt"
        mock_execute_command.assert_called_once_with("ls | grep .txt")

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_with_quotes(self, mock_execute_command, shell_execute_tool):
        """Test shell command with quoted arguments."""
        # Mock successful response with quoted command
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Found 5 files with 'test' in name",
            stderr="",
            return_code=0,
            command="find . -name '*test*'"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("find . -name '*test*'"))
        
        assert result["success"] is True
        assert result["result"] == "Found 5 files with 'test' in name"
        assert result["command"] == "find . -name '*test*'"
        mock_execute_command.assert_called_once_with("find . -name '*test*'")

    def test_shell_execute_tool_class_attributes(self, shell_execute_tool):
        """Test that ShellExecuteTool has the expected class structure."""
        assert hasattr(shell_execute_tool, 'tool_execute_shell_command')
        assert callable(shell_execute_tool.tool_execute_shell_command)

    def test_shell_execute_tool_return_structure(self, shell_execute_tool):
        """Test that tool_execute_shell_command returns the correct data structure."""
        with patch('tools.shell.execute.CommandExecutor.execute_command') as mock_execute_command:
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="Test result",
                stderr="",
                return_code=0,
                command="test command"
            )
            
            result = asyncio.run(shell_execute_tool.tool_execute_shell_command("test command"))
            
            required_keys = {"success", "result", "command"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["result"], str)
            assert isinstance(result["command"], str)

    @patch('tools.shell.execute.CommandExecutor.execute_command')
    def test_execute_shell_command_empty_output(self, mock_execute_command, shell_execute_tool):
        """Test shell command with empty output."""
        # Mock successful response with empty output
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="",
            stderr="",
            return_code=0,
            command="touch empty_file.txt"
        )
        
        result = asyncio.run(shell_execute_tool.tool_execute_shell_command("touch empty_file.txt"))
        
        assert result["success"] is True
        assert result["result"] == ""
        assert result["command"] == "touch empty_file.txt" 