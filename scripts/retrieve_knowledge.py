#!/usr/bin/env python3
"""
Knowledge retrieve script for Cursor MCP.
Retrieves agent learnings from the SQLite database.
"""

import os
import sys
import sqlite3
import json

DB_PATH = './data/cursor_agent.db'

def dict_factory(cursor, row):
    """Convert database row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def retrieve_knowledge(category, key=""):
    """Retrieve knowledge from the agent_knowledge table."""
    if not os.path.exists(DB_PATH):
        return json.dumps({
            "error": "Database does not exist. Run db_setup.py first."
        })
    
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        if key:
            # Retrieve specific knowledge
            cursor.execute("""
            SELECT category, key, value, created_at, updated_at
            FROM agent_knowledge
            WHERE category = ? AND key = ?
            """, (category, key))
            
            result = cursor.fetchone()
            
            if not result:
                return json.dumps({
                    "status": "success",
                    "message": f"No knowledge found for category '{category}' and key '{key}'",
                    "result": None
                })
            
            return json.dumps({
                "status": "success",
                "result": result
            })
        else:
            # Retrieve all knowledge in category
            cursor.execute("""
            SELECT category, key, value, created_at, updated_at
            FROM agent_knowledge
            WHERE category = ?
            ORDER BY updated_at DESC
            """, (category,))
            
            results = cursor.fetchall()
            
            if not results:
                return json.dumps({
                    "status": "success",
                    "message": f"No knowledge found for category '{category}'",
                    "results": []
                })
            
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
            "message": "Missing category. Usage: python retrieve_knowledge.py \"category\" [\"key\"]"
        }))
        sys.exit(1)
    
    category = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else ""
    
    result = retrieve_knowledge(category, key)
    print(result)