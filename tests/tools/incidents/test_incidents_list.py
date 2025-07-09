"""
Tests for the Incidents List tool.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock
from tools.incidents.list import IncidentsListTool
from utils.command_executor import CommandResult

class TestIncidentsListTool:
    """Test cases for IncidentsListTool."""

    @pytest.fixture
    def incidents_list_tool(self):
        """Create an IncidentsListTool instance for testing."""
        return IncidentsListTool()

    @patch('tools.incidents.list.os.path.exists')
    def test_incidents_dir_does_not_exist(self, mock_exists, incidents_list_tool):
        """Test when the incidents directory does not exist."""
        mock_exists.return_value = False
        result = asyncio.run(incidents_list_tool.tool_list_incidents())
        assert result["success"] is True
        assert result["incidents"] == []
        assert result["count"] == 0
        assert "message" in result
        assert result["message"] == "Incidents directory does not exist"

    @patch('tools.incidents.list.os.path.exists')
    @patch('tools.incidents.list.CommandExecutor.execute_command')
    def test_incidents_command_failure(self, mock_execute_command, mock_exists, incidents_list_tool):
        """Test when the command fails to list incidents."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="ls: cannot access '~/incidents': No such file or directory",
            return_code=2,
            command="ls -la ~/incidents"
        )
        result = asyncio.run(incidents_list_tool.tool_list_incidents())
        assert result["success"] is False
        assert result["incidents"] == []
        assert "error" in result

    @patch('tools.incidents.list.os.path.exists')
    @patch('tools.incidents.list.CommandExecutor.execute_command')
    def test_incidents_empty_directory(self, mock_execute_command, mock_exists, incidents_list_tool):
        """Test when the incidents directory is empty (only . and ..)."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="total 0\ndrwxr-xr-x 2 user group 4096 Jan 1 00:00 .\ndrwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n",
            stderr="",
            return_code=0,
            command="ls -la ~/incidents"
        )
        result = asyncio.run(incidents_list_tool.tool_list_incidents())
        assert result["success"] is True
        assert result["incidents"] == []
        assert result["count"] == 0
        assert "directory" in result

    @patch('tools.incidents.list.os.path.exists')
    @patch('tools.incidents.list.CommandExecutor.execute_command')
    def test_incidents_with_files(self, mock_execute_command, mock_exists, incidents_list_tool):
        """Test when the incidents directory contains files and directories."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=(
                "total 8\n"
                "drwxr-xr-x 2 user group 4096 Jan 1 00:00 .\n"
                "drwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n"
                "-rw-r--r-- 1 user group  123 Jan 2 12:34 2024-01-01.log\n"
                "drwxr-xr-x 2 user group 4096 Jan 3 13:45 2024-01-02\n"
                "-rw-r--r-- 1 user group  456 Jan 4 14:56 README.txt\n"
            ),
            stderr="",
            return_code=0,
            command="ls -la ~/incidents"
        )
        result = asyncio.run(incidents_list_tool.tool_list_incidents())
        assert result["success"] is True
        assert result["count"] == 2  # Only 2024-01-01.log and 2024-01-02
        names = [i["name"] for i in result["incidents"]]
        assert "2024-01-01.log" in names
        assert "2024-01-02" in names
        assert "README.txt" not in names
        for incident in result["incidents"]:
            assert "name" in incident
            assert "permissions" in incident
            assert "size" in incident
            assert "date" in incident
            assert "is_directory" in incident

    def test_incidents_list_tool_class_attributes(self, incidents_list_tool):
        """Test that IncidentsListTool has the expected class structure."""
        assert hasattr(incidents_list_tool, 'tool_list_incidents')
        assert callable(incidents_list_tool.tool_list_incidents)

    def test_incidents_list_tool_return_structure(self, incidents_list_tool):
        """Test that tool_list_incidents returns the correct data structure."""
        with patch('tools.incidents.list.os.path.exists') as mock_exists, \
             patch('tools.incidents.list.CommandExecutor.execute_command') as mock_execute_command:
            mock_exists.return_value = True
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="total 0\ndrwxr-xr-x 2 user group 4096 Jan 1 00:00 .\ndrwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n",
                stderr="",
                return_code=0,
                command="ls -la ~/incidents"
            )
            result = asyncio.run(incidents_list_tool.tool_list_incidents())
            required_keys = {"success", "incidents", "count", "directory"}
            assert set(result.keys()).issuperset(required_keys)
            assert isinstance(result["success"], bool)
            assert isinstance(result["incidents"], list)
            assert isinstance(result["count"], int) 