"""
Command execution utilities for the Hypernode MCP server.
Provides safe command execution with proper error handling and validation.
"""

import asyncio
import json
import logging
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CommandResult:
    """Result of a command execution."""
    success: bool
    stdout: str
    stderr: str
    return_code: int
    command: str

class CommandExecutor:
    """Safe command executor with validation and error handling."""
    
    # List of dangerous commands that should be blocked
    DANGEROUS_COMMANDS = {
        'rm', 'rmdir', 'del', 'format', 'mkfs', 'dd', 'shred',
        'kill', 'killall', 'pkill', 'halt', 'shutdown', 'reboot'
    }
    
    @classmethod
    def is_dangerous_command(cls, command: str) -> bool:
        """Check if a command is considered dangerous."""
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return False
        
        base_cmd = cmd_parts[0].lower()
        return base_cmd in cls.DANGEROUS_COMMANDS
    
    @classmethod
    async def execute_command(
        cls, 
        command: str, 
        timeout: int = 30,
        cwd: Optional[str] = None
    ) -> CommandResult:
        """
        Execute a command asynchronously with proper error handling.
        
        Args:
            command: The command to execute
            timeout: Timeout in seconds
            cwd: Working directory for the command
            
        Returns:
            CommandResult with execution details
        """
        logger.info(f"Executing command: {command}")
        
        if cls.is_dangerous_command(command):
            return CommandResult(
                success=False,
                stdout="",
                stderr=f"Command '{command}' is blocked for security reasons",
                return_code=1,
                command=command
            )
        
        try:
            # Check if command contains shell features that require shell=True
            shell_features = ['|', '&&', '||', ';', '>', '<', '>>', '<<', '&', '(', ')', '$', '`']
            use_shell = any(feature in command for feature in shell_features)
            
            if use_shell:
                # Use shell=True for commands with pipes, redirects, etc.
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                )
            else:
                # Use subprocess_exec for simple commands (more secure)
                process = await asyncio.create_subprocess_exec(
                    *command.split(),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            result = CommandResult(
                success=process.returncode == 0,
                stdout=stdout.decode('utf-8', errors='ignore'),
                stderr=stderr.decode('utf-8', errors='ignore'),
                return_code=process.returncode,
                command=command
            )
            
            if result.success:
                logger.info(f"Command executed successfully: {command}")
            else:
                logger.warning(f"Command failed: {command}, return code: {process.returncode}")
                
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"Command timed out: {command}")
            return CommandResult(
                success=False,
                stdout="",
                stderr=f"Command timed out after {timeout} seconds",
                return_code=-1,
                command=command
            )
        except Exception as e:
            logger.error(f"Error executing command '{command}': {str(e)}")
            return CommandResult(
                success=False,
                stdout="",
                stderr=f"Error executing command: {str(e)}",
                return_code=-1,
                command=command
            )
    
    @classmethod
    async def execute_json_command(
        cls, 
        command: str, 
        timeout: int = 30
    ) -> Tuple[bool, Any]:
        """
        Execute a command that returns JSON and parse the result.
        
        Args:
            command: The command to execute
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (success, parsed_json_or_error_message)
        """
        result = await cls.execute_command(command, timeout)
        
        if not result.success:
            return False, result.stderr
        
        try:
            parsed_json = json.loads(result.stdout)
            return True, parsed_json
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from command output: {e}")
            return False, f"Invalid JSON output: {result.stdout[:200]}..."
    
    @classmethod
    def validate_vhost_name(cls, vhost_name: str) -> bool:
        """Validate a vhost name format."""
        if not vhost_name or '.' not in vhost_name:
            return False
        return True
    
    @classmethod
    def validate_attack_name(cls, attack_name: str) -> bool:
        """Validate an attack name format."""
        if not attack_name or not attack_name.startswith('Block'):
            return False
        return True 