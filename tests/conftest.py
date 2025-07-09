"""
Pytest configuration and shared fixtures for Hypernode MCP Server tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Return the project root path."""
    return project_root


@pytest.fixture(scope="session")
def test_data_path():
    """Return the path to test data directory."""
    return project_root / "tests" / "data"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test."""
    # Add any test environment setup here
    pass


@pytest.fixture(autouse=True)
def cleanup_test_environment():
    """Clean up test environment after each test."""
    yield
    # Add any test environment cleanup here
    pass 