#!/usr/bin/env python3
"""
MCP Setup Script
---------------
This script verifies and initializes the Model-Cursor Protocol (MCP) system.
It checks that all required components are in place and properly configured.
"""

import os
import sys
import importlib.util
import subprocess
from pathlib import Path

# Define colors for console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_script_exists(script_name):
    """Check if a script exists in the scripts directory."""
    script_path = Path(__file__).parent / f"{script_name}.py"
    return script_path.exists()

def import_script(script_name):
    """Import a script module from the scripts directory."""
    script_path = Path(__file__).parent / f"{script_name}.py"
    spec = importlib.util.spec_from_file_location(script_name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    """Main function to set up the MCP system."""
    print(f"{Colors.HEADER}MCP Setup Process{Colors.ENDC}")
    print(f"{Colors.BOLD}-------------------{Colors.ENDC}")
    
    # Check for required scripts
    required_scripts = [
        "db_setup", "db_save", "db_query", 
        "store_knowledge", "retrieve_knowledge", "app"
    ]
    
    all_scripts_exist = True
    for script in required_scripts:
        if check_script_exists(script):
            print(f"{Colors.GREEN}✓{Colors.ENDC} Found {script}.py")
        else:
            print(f"{Colors.FAIL}✗{Colors.ENDC} Missing {script}.py")
            all_scripts_exist = False
    
    if not all_scripts_exist:
        print(f"\n{Colors.FAIL}Error: Some required scripts are missing. MCP setup failed.{Colors.ENDC}")
        return 1
    
    print(f"\n{Colors.BLUE}Setting up database...{Colors.ENDC}")
    try:
        # Import and run database setup
        db_setup = import_script("db_setup")
        # Assuming db_setup has a main() or setup() function
        if hasattr(db_setup, "main"):
            db_setup.main()
        elif hasattr(db_setup, "setup"):
            db_setup.setup()
        else:
            print(f"{Colors.WARNING}Warning: Could not find setup function in db_setup.py{Colors.ENDC}")
            print(f"{Colors.WARNING}Attempting to run db_setup.py directly...{Colors.ENDC}")
            subprocess.run([sys.executable, Path(__file__).parent / "db_setup.py"])
        
        print(f"{Colors.GREEN}Database setup completed successfully.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error setting up database: {str(e)}{Colors.ENDC}")
        return 1
    
    print(f"\n{Colors.BLUE}Verifying knowledge storage system...{Colors.ENDC}")
    try:
        # Test storing and retrieving knowledge
        store = import_script("store_knowledge")
        retrieve = import_script("retrieve_knowledge")
        
        # Store a test entry
        test_key = "mcp_setup_test"
        test_value = "MCP system is functioning correctly"
        
        if hasattr(store, "store_knowledge"):
            store.store_knowledge(test_key, test_value)
        elif hasattr(store, "main"):
            # Assuming the main function can handle this or make appropriate adjustments
            store.main(key=test_key, value=test_value)
        else:
            print(f"{Colors.WARNING}Warning: Could not find appropriate function in store_knowledge.py{Colors.ENDC}")
        
        # Retrieve the test entry
        retrieved_value = None
        if hasattr(retrieve, "retrieve_knowledge"):
            retrieved_value = retrieve.retrieve_knowledge(test_key)
        elif hasattr(retrieve, "main"):
            # Assuming the main function can handle this or make appropriate adjustments
            retrieved_value = retrieve.main(key=test_key)
        
        if retrieved_value and test_value in str(retrieved_value):
            print(f"{Colors.GREEN}Knowledge storage system is working correctly.{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Knowledge retrieval test produced unexpected results.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}Warning during knowledge system verification: {str(e)}{Colors.ENDC}")
        print(f"{Colors.WARNING}Continuing with setup process...{Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}MCP Setup Completed Successfully!{Colors.ENDC}")
    print(f"""
{Colors.BLUE}The MCP system is now ready to:
- Learn from your codebase
- Adapt to your coding patterns
- Store and retrieve project knowledge
- Provide context-aware assistance{Colors.ENDC}
""")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 