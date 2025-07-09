#!/bin/bash

# Hypernode MCP Server Test Runner
# This script runs the test suite in the Hypernode Docker container

set -e

echo "🚀 Starting Hypernode MCP Server tests..."
echo "📦 Using Docker image: docker.hypernode.com/byteinternet/hypernode-bookworm-docker-php84-mysql80"
echo ""

# Run tests in Docker container
docker run --rm \
  -v "$(pwd):/workspace" \
  -w /workspace \
  docker.hypernode.com/byteinternet/hypernode-bookworm-docker-php84-mysql80 \
  bash -c "
    set -e

    cd /workspace
    
    echo '🐍 Setting up Python virtual environment...'
    python -m virtualenv venv
    source venv/bin/activate
    
    echo '📦 Installing Python packages...'
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    
    echo '🧪 Running tests...'
    python -m pytest tests/ -v
    
    echo '✅ Tests completed!'
    echo '📊 Coverage report generated in htmlcov/ directory'
  "

echo ""
echo "🎉 Test run completed!"
echo "📊 Coverage report available in htmlcov/index.html" 