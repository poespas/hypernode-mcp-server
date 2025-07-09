"""
Tests for the Incidents Get tool.
"""

import pytest
import asyncio
from unittest.mock import patch, mock_open, MagicMock
from tools.incidents.get import IncidentsGetTool
from utils.command_executor import CommandResult

class TestIncidentsGetTool:
    """Test cases for IncidentsGetTool."""

    @pytest.fixture
    def incidents_get_tool(self):
        """Create an IncidentsGetTool instance for testing."""
        return IncidentsGetTool()

    @patch('tools.incidents.get.os.path.exists')
    def test_incident_dir_does_not_exist(self, mock_exists, incidents_get_tool):
        """Test when the incident directory does not exist."""
        mock_exists.return_value = False
        result = asyncio.run(incidents_get_tool.tool_get_incident('2024-01-01'))
        assert result["success"] is False
        assert "error" in result
        assert "incident_path" in result

    @patch('tools.incidents.get.os.path.exists')
    @patch('tools.incidents.get.CommandExecutor.execute_command')
    def test_incident_command_failure(self, mock_execute_command, mock_exists, incidents_get_tool):
        """Test when the command fails to list files."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="ls: cannot access '~/incidents/2024-01-01': No such file or directory",
            return_code=2,
            command="ls -la ~/incidents/2024-01-01/*"
        )
        result = asyncio.run(incidents_get_tool.tool_get_incident('2024-01-01'))
        assert result["success"] is False
        assert "error" in result
        assert "incident_path" in result

    @patch('tools.incidents.get.os.path.exists')
    @patch('tools.incidents.get.CommandExecutor.execute_command')
    def test_incident_empty_directory(self, mock_execute_command, mock_exists, incidents_get_tool):
        """Test when the incident directory is empty (only . and ..)."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="total 0\ndrwxr-xr-x 2 user group 4096 Jan 1 00:00 .\ndrwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n",
            stderr="",
            return_code=0,
            command="ls -la ~/incidents/2024-01-01/*"
        )
        result = asyncio.run(incidents_get_tool.tool_get_incident('2024-01-01'))
        assert result["success"] is True
        assert result["files"] == []
        assert result["count"] == 0
        assert result["incident_date"] == '2024-01-01'

    @patch('tools.incidents.get.os.path.exists')
    @patch('tools.incidents.get.CommandExecutor.execute_command')
    @patch('builtins.open', new_callable=mock_open, read_data='file content')
    def test_incident_with_files(self, mock_file, mock_execute_command, mock_exists, incidents_get_tool):
        """Test when the incident directory contains files."""
        mock_exists.return_value = True
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=(
                "total 8\n"
                "drwxr-xr-x 2 user group 4096 Jan 1 00:00 .\n"
                "drwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n"
                "-rw-r--r-- 1 user group  123 Jan 2 12:34 test.log\n"
                "drwxr-xr-x 2 user group 4096 Jan 3 13:45 subdir\n"
            ),
            stderr="",
            return_code=0,
            command="ls -la ~/incidents/2024-01-01/*"
        )
        # Patch os.path.join to return a fake path
        with patch('tools.incidents.get.os.path.join', side_effect=lambda *args: '/'.join(args)):
            result = asyncio.run(incidents_get_tool.tool_get_incident('2024-01-01'))
        assert result["success"] is True
        assert result["count"] == 2
        names = [f["name"] for f in result["files"]]
        assert "test.log" in names
        assert "subdir" in names
        for file in result["files"]:
            assert "name" in file
            assert "permissions" in file
            assert "size" in file
            assert "date" in file
            assert "is_directory" in file
            assert "full_path" in file
            if not file["is_directory"]:
                assert "content" in file
                assert file["content"] == 'file content'

    def test_incidents_get_tool_class_attributes(self, incidents_get_tool):
        """Test that IncidentsGetTool has the expected class structure."""
        assert hasattr(incidents_get_tool, 'tool_get_incident')
        assert callable(incidents_get_tool.tool_get_incident)

    def test_incidents_get_tool_return_structure(self, incidents_get_tool):
        """Test that tool_get_incident returns the correct data structure."""
        with patch('tools.incidents.get.os.path.exists') as mock_exists, \
             patch('tools.incidents.get.CommandExecutor.execute_command') as mock_execute_command:
            mock_exists.return_value = True
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="total 0\ndrwxr-xr-x 2 user group 4096 Jan 1 00:00 .\ndrwxr-xr-x 3 user group 4096 Jan 1 00:00 ..\n",
                stderr="",
                return_code=0,
                command="ls -la ~/incidents/2024-01-01/*"
            )
            result = asyncio.run(incidents_get_tool.tool_get_incident('2024-01-01'))
            required_keys = {"success", "incident_date", "incident_path", "files", "count", "file_pattern"}
            assert set(result.keys()).issuperset(required_keys)
            assert isinstance(result["success"], bool)
            assert isinstance(result["files"], list)
            assert isinstance(result["count"], int) 