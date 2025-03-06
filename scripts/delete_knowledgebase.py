#!/usr/bin/env python3
"""
Script to delete the Cursor MCP knowledgebase.
This will remove all stored knowledge from the SQLite database.
"""

import os
import sqlite3
import sys

DB_PATH = './data/cursor_agent.db'

def delete_knowledgebase():
    """Delete the knowledgebase by truncating all tables or deleting the DB file."""
    
    if not os.path.exists(DB_PATH):
        print(f"Database file not found at {DB_PATH}. Nothing to delete.")
        return
    
    # Option 1: Delete the entire database file
    try:
        os.remove(DB_PATH)
        print(f"Database file {DB_PATH} has been deleted.")
        return
    except Exception as e:
        print(f"Warning: Could not delete database file: {e}")
        print("Attempting to truncate tables instead...")
    
    # Option 2: Truncate all tables if file deletion failed
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Truncate each table
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Skip internal SQLite tables
                cursor.execute(f"DELETE FROM {table_name};")
                print(f"Table '{table_name}' has been truncated.")
        
        conn.commit()
        conn.close()
        print("All knowledgebase tables have been truncated.")
    except Exception as e:
        print(f"Error truncating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Deleting Cursor MCP knowledgebase...")
    delete_knowledgebase()
    print("Knowledgebase deletion complete!") 