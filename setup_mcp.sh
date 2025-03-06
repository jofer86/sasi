#!/bin/bash

# Setup MCP System
# This script runs the MCP setup process

# Set colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting MCP Setup Process${NC}"
echo -e "${BLUE}=========================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo -e "${YELLOW}Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if scripts directory exists
if [ ! -d "scripts" ]; then
    echo -e "${RED}Error: scripts directory not found.${NC}"
    echo -e "${YELLOW}Please make sure you're running this script from the project root directory.${NC}"
    exit 1
fi

# Make the setup script executable
chmod +x scripts/mcp_setup.py

# Run the MCP setup script
echo -e "${BLUE}Running MCP setup script...${NC}"
python3 scripts/mcp_setup.py

# Check if setup was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}MCP Setup completed successfully!${NC}"
    echo -e "${BLUE}You can now continue working on your project with enhanced AI assistance.${NC}"
else
    echo -e "${RED}MCP Setup encountered issues.${NC}"
    echo -e "${YELLOW}Please check the error messages above and try again.${NC}"
    exit 1
fi 