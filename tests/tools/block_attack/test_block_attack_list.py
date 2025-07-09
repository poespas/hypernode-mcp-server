"""
Tests for the Block Attack List tool.
"""

import pytest
import asyncio
from unittest.mock import patch
from tools.block_attack.list import BlockAttackListTool
from utils.command_executor import CommandResult

class TestBlockAttackListTool:
    """Test cases for BlockAttackListTool."""

    @pytest.fixture
    def block_attack_list_tool(self):
        """Create a BlockAttackListTool instance for testing."""
        return BlockAttackListTool()

    def test_block_attack_list_tool_creation(self, block_attack_list_tool):
        """Test that BlockAttackListTool can be instantiated."""
        assert isinstance(block_attack_list_tool, BlockAttackListTool)

    @patch('tools.block_attack.list.CommandExecutor.execute_command')
    def test_list_attacks_success(self, mock_execute_command, block_attack_list_tool):
        """Test successful attack listing."""
        # Mock successful response with attack data
        mock_output = (
            "usage: hypernode-systemctl block_attack [OPTIONS] ATTACK_TYPE\n\n"
            "The possible values are:\n"
            "BlockChinaBruteForce\tBlock brute force attacks from China\n"
            "BlockRussiaBruteForce\tBlock brute force attacks from Russia\n"
            "BlockDDoS\tBlock DDoS attacks\n"
            "options:\n"
            "  --help  Show this message and exit.\n"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack --help"
        )
        
        result = asyncio.run(block_attack_list_tool.tool_list_attacks())
        
        assert result["success"] is True
        assert result["count"] == 3
        assert len(result["attacks"]) == 3
        
        attack_names = [attack["name"] for attack in result["attacks"]]
        assert "BlockChinaBruteForce" in attack_names
        assert "BlockRussiaBruteForce" in attack_names
        assert "BlockDDoS" in attack_names
        
        # Check that descriptions are extracted
        for attack in result["attacks"]:
            assert "name" in attack
            assert "description" in attack
            assert attack["name"].startswith("Block")
        
        mock_execute_command.assert_called_once_with("hypernode-systemctl block_attack --help")

    @patch('tools.block_attack.list.CommandExecutor.execute_command')
    def test_list_attacks_failure(self, mock_execute_command, block_attack_list_tool):
        """Test attack listing failure."""
        # Mock failure response
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Command not found: hypernode-systemctl",
            return_code=127,
            command="hypernode-systemctl block_attack --help"
        )
        
        result = asyncio.run(block_attack_list_tool.tool_list_attacks())
        
        assert result["success"] is False
        assert result["attacks"] == []
        assert "error" in result
        assert result["error"] == "Command not found: hypernode-systemctl"

    @patch('tools.block_attack.list.CommandExecutor.execute_command')
    def test_list_attacks_empty_result(self, mock_execute_command, block_attack_list_tool):
        """Test attack listing with no attacks found."""
        # Mock response with no attack data
        mock_output = (
            "usage: hypernode-systemctl block_attack [OPTIONS] ATTACK_TYPE\n\n"
            "The possible values are:\n"
            "options:\n"
            "  --help  Show this message and exit.\n"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack --help"
        )
        
        result = asyncio.run(block_attack_list_tool.tool_list_attacks())
        
        assert result["success"] is True
        assert result["attacks"] == []
        assert result["count"] == 0
        assert "raw_output" in result

    @patch('tools.block_attack.list.CommandExecutor.execute_command')
    def test_list_attacks_malformed_output(self, mock_execute_command, block_attack_list_tool):
        """Test attack listing with malformed output."""
        # Mock response with malformed data
        mock_output = (
            "usage: hypernode-systemctl block_attack [OPTIONS] ATTACK_TYPE\n\n"
            "The possible values are:\n"
            "BlockChinaBruteForce\n"  # Missing tab separator
            "BlockRussiaBruteForce\tBlock brute force attacks from Russia\n"
            "InvalidLine\t\tToo many tabs\n"
            "options:\n"
            "  --help  Show this message and exit.\n"
        )
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout=mock_output,
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack --help"
        )
        
        result = asyncio.run(block_attack_list_tool.tool_list_attacks())
        
        assert result["success"] is True
        assert result["count"] == 1  # Only the valid line should be parsed
        assert len(result["attacks"]) == 1
        assert result["attacks"][0]["name"] == "BlockRussiaBruteForce"

    def test_block_attack_list_tool_class_attributes(self, block_attack_list_tool):
        """Test that BlockAttackListTool has the expected class structure."""
        assert hasattr(block_attack_list_tool, 'tool_list_attacks')
        assert callable(block_attack_list_tool.tool_list_attacks)

    def test_block_attack_list_tool_return_structure(self, block_attack_list_tool):
        """Test that tool_list_attacks returns the correct data structure."""
        with patch('tools.block_attack.list.CommandExecutor.execute_command') as mock_execute_command:
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="usage: hypernode-systemctl block_attack [OPTIONS] ATTACK_TYPE\n\nThe possible values are:\noptions:\n  --help  Show this message and exit.\n",
                stderr="",
                return_code=0,
                command="hypernode-systemctl block_attack --help"
            )
            
            result = asyncio.run(block_attack_list_tool.tool_list_attacks())
            
            required_keys = {"success", "attacks", "count", "raw_output"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["attacks"], list)
            assert isinstance(result["count"], int)
            assert isinstance(result["raw_output"], str) 