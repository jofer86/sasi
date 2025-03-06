#!/usr/bin/env python3
"""
Knowledge store script for Cursor MCP.
Stores agent learnings in the SQLite database.
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

DB_PATH = './data/cursor_agent.db'

def store_knowledge(category, key, value_json):
    """Store knowledge in the agent_knowledge table."""
    if not os.path.exists(DB_PATH):
        return json.dumps({
            "error": "Database does not exist. Run db_setup.py first."
        })
    
    try:
        # Parse the JSON value
        value = value_json
        now = datetime.now().isoformat()
        
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if knowledge exists
        cursor.execute("SELECT id FROM agent_knowledge WHERE category = ? AND key = ?", 
                      (category, key))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing knowledge
            cursor.execute('''
            UPDATE agent_knowledge 
            SET value = ?, updated_at = ?
            WHERE category = ? AND key = ?
            ''', (
                value, 
                now,
                category,
                key
            ))
        else:
            # Insert new knowledge
            cursor.execute('''
            INSERT INTO agent_knowledge (category, key, value, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                category, 
                key, 
                value, 
                now,
                now
            ))
        
        conn.commit()
        conn.close()
        
        return json.dumps({
            "status": "success",
            "message": "Knowledge stored successfully",
            "operation": "update" if existing else "insert",
            "category": category,
            "key": key
        })
        
    except sqlite3.Error as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({
            "status": "error",
            "message": "Missing arguments. Usage: python store_knowledge.py \"category\" \"key\" 'value_json'"
        }))
        sys.exit(1)
    
    category = sys.argv[1]
    key = sys.argv[2]
    value = sys.argv[3]
    
    result = store_knowledge(category, key, value)
    print(result)