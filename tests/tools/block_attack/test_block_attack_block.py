"""
Tests for the Block Attack Block tool.
"""

import pytest
import asyncio
from unittest.mock import patch
from tools.block_attack.block import BlockAttackTool
from utils.command_executor import CommandResult

class TestBlockAttackTool:
    """Test cases for BlockAttackTool."""

    @pytest.fixture
    def block_attack_tool(self):
        """Create a BlockAttackTool instance for testing."""
        return BlockAttackTool()

    def test_block_attack_tool_creation(self, block_attack_tool):
        """Test that BlockAttackTool can be instantiated."""
        assert isinstance(block_attack_tool, BlockAttackTool)

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_success(self, mock_execute_command, block_attack_tool):
        """Test successful attack blocking."""
        # Mock successful response
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Successfully blocked BlockChinaBruteForce attacks",
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack BlockChinaBruteForce"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("BlockChinaBruteForce"))
        
        assert result["success"] is True
        assert result["result"] == "Successfully blocked BlockChinaBruteForce attacks"
        assert result["attack_type"] == "BlockChinaBruteForce"
        mock_execute_command.assert_called_once_with("hypernode-systemctl block_attack BlockChinaBruteForce")

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_failure(self, mock_execute_command, block_attack_tool):
        """Test attack blocking failure."""
        # Mock failure response
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Invalid attack type: InvalidAttackType",
            return_code=1,
            command="hypernode-systemctl block_attack InvalidAttackType"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("InvalidAttackType"))
        
        assert result["success"] is False
        assert result["result"] == "Invalid attack type: InvalidAttackType"
        assert result["attack_type"] == "InvalidAttackType"
        mock_execute_command.assert_called_once_with("hypernode-systemctl block_attack InvalidAttackType")

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_different_types(self, mock_execute_command, block_attack_tool):
        """Test blocking different attack types."""
        # Test BlockRussiaBruteForce
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Successfully blocked BlockRussiaBruteForce attacks",
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack BlockRussiaBruteForce"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("BlockRussiaBruteForce"))
        
        assert result["success"] is True
        assert result["attack_type"] == "BlockRussiaBruteForce"
        mock_execute_command.assert_called_once_with("hypernode-systemctl block_attack BlockRussiaBruteForce")

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_ddos(self, mock_execute_command, block_attack_tool):
        """Test blocking DDoS attacks."""
        # Mock successful response for DDoS blocking
        mock_execute_command.return_value = CommandResult(
            success=True,
            stdout="Successfully blocked DDoS attacks",
            stderr="",
            return_code=0,
            command="hypernode-systemctl block_attack BlockDDoS"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("BlockDDoS"))
        
        assert result["success"] is True
        assert result["result"] == "Successfully blocked DDoS attacks"
        assert result["attack_type"] == "BlockDDoS"
        mock_execute_command.assert_called_once_with("hypernode-systemctl block_attack BlockDDoS")

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_command_not_found(self, mock_execute_command, block_attack_tool):
        """Test when the command is not found."""
        # Mock command not found
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Command not found: hypernode-systemctl",
            return_code=127,
            command="hypernode-systemctl block_attack BlockChinaBruteForce"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("BlockChinaBruteForce"))
        
        assert result["success"] is False
        assert result["result"] == "Command not found: hypernode-systemctl"
        assert result["attack_type"] == "BlockChinaBruteForce"

    @patch('tools.block_attack.block.CommandExecutor.execute_command')
    def test_block_attack_permission_denied(self, mock_execute_command, block_attack_tool):
        """Test when permission is denied."""
        # Mock permission denied
        mock_execute_command.return_value = CommandResult(
            success=False,
            stdout="",
            stderr="Permission denied",
            return_code=13,
            command="hypernode-systemctl block_attack BlockChinaBruteForce"
        )
        
        result = asyncio.run(block_attack_tool.tool_block_attack("BlockChinaBruteForce"))
        
        assert result["success"] is False
        assert result["result"] == "Permission denied"
        assert result["attack_type"] == "BlockChinaBruteForce"

    def test_block_attack_tool_class_attributes(self, block_attack_tool):
        """Test that BlockAttackTool has the expected class structure."""
        assert hasattr(block_attack_tool, 'tool_block_attack')
        assert callable(block_attack_tool.tool_block_attack)

    def test_block_attack_tool_return_structure(self, block_attack_tool):
        """Test that tool_block_attack returns the correct data structure."""
        with patch('tools.block_attack.block.CommandExecutor.execute_command') as mock_execute_command:
            mock_execute_command.return_value = CommandResult(
                success=True,
                stdout="Test result",
                stderr="",
                return_code=0,
                command="hypernode-systemctl block_attack TestAttack"
            )
            
            result = asyncio.run(block_attack_tool.tool_block_attack("TestAttack"))
            
            required_keys = {"success", "result", "attack_type"}
            assert set(result.keys()) == required_keys
            assert isinstance(result["success"], bool)
            assert isinstance(result["result"], str)
            assert isinstance(result["attack_type"], str) 