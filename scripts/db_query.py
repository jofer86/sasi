#!/usr/bin/env python3
"""
Database query script for Cursor MCP.
Executes SQL queries against the SQLite database and returns results as JSON.
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

DB_PATH = './data/cursor_agent.db'

def dict_factory(cursor, row):
    """Convert database row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def run_query(query):
    """Execute a query and return results as JSON."""
    if not os.path.exists(DB_PATH):
        return json.dumps({
            "error": "Database does not exist. Run db_setup.py first."
        })
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # If the query modifies data, commit changes
        if query.strip().lower().startswith(('insert', 'update', 'delete', 'create', 'drop', 'alter')):
            conn.commit()
            return json.dumps({
                "status": "success",
                "message": "Query executed successfully",
                "rows_affected": cursor.rowcount
            })
        
        # For SELECT queries, return the results
        results = cursor.fetchall()
        conn.close()
        
        return json.dumps({
            "status": "success",
            "count": len(results),
            "results": results
        })
        
    except sqlite3.Error as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "No query provided. Usage: python db_query.py \"SQL QUERY\""
        }))
        sys.exit(1)
    
    query = sys.argv[1]
    result = run_query(query)
    print(result)