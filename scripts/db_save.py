#!/usr/bin/env python3
"""
Database save script for Cursor MCP.
Saves JSON data to the specified table in the SQLite database.
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

DB_PATH = './data/cursor_agent.db'

def save_to_database(table, data_json):
    """Save JSON data to the specified table."""
    if not os.path.exists(DB_PATH):
        return json.dumps({
            "error": "Database does not exist. Run db_setup.py first."
        })
    
    try:
        # Parse the JSON data
        data = json.loads(data_json)
        
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Handle different tables
        if table == "documentation":
            return save_documentation(cursor, conn, data)
        elif table == "project_status":
            return save_project_status(cursor, conn, data)
        elif table == "agent_knowledge":
            return save_agent_knowledge(cursor, conn, data)
        elif table == "code_patterns":
            return save_code_pattern(cursor, conn, data)
        elif table == "interaction_history":
            return save_interaction_history(cursor, conn, data)
        elif table == "project_metrics":
            return save_project_metric(cursor, conn, data)
        else:
            return json.dumps({
                "status": "error",
                "message": f"Unknown table: {table}"
            })
    
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "Invalid JSON data"
        })
    except sqlite3.Error as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

def save_documentation(cursor, conn, data):
    """Save documentation data."""
    now = datetime.now().isoformat()
    
    # Check if record exists
    cursor.execute("SELECT id FROM documentation WHERE path = ?", (data.get('path'),))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing record
        cursor.execute('''
        UPDATE documentation 
        SET title = ?, content = ?, tags = ?, updated_at = ?
        WHERE path = ?
        ''', (
            data.get('title'), 
            data.get('content'), 
            data.get('tags', ''), 
            now,
            data.get('path')
        ))
    else:
        # Insert new record
        cursor.execute('''
        INSERT INTO documentation (path, title, content, tags, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('path'), 
            data.get('title'), 
            data.get('content'), 
            data.get('tags', ''),
            now, 
            now
        ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Documentation saved successfully",
        "operation": "update" if existing else "insert"
    })

def save_project_status(cursor, conn, data):
    """Save project status data."""
    now = datetime.now().isoformat()
    
    # Check if component exists
    cursor.execute("SELECT id FROM project_status WHERE component = ?", (data.get('component'),))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing component
        cursor.execute('''
        UPDATE project_status 
        SET status = ?, message = ?, last_check = ?
        WHERE component = ?
        ''', (
            data.get('status'), 
            data.get('message'), 
            now,
            data.get('component')
        ))
    else:
        # Insert new component
        cursor.execute('''
        INSERT INTO project_status (component, status, message, last_check)
        VALUES (?, ?, ?, ?)
        ''', (
            data.get('component'), 
            data.get('status'), 
            data.get('message'), 
            now
        ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Project status saved successfully",
        "operation": "update" if existing else "insert"
    })

def save_agent_knowledge(cursor, conn, data):
    """Save agent knowledge data."""
    now = datetime.now().isoformat()
    
    # Check if knowledge exists
    cursor.execute("SELECT id FROM agent_knowledge WHERE category = ? AND key = ?", 
                  (data.get('category'), data.get('key')))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing knowledge
        cursor.execute('''
        UPDATE agent_knowledge 
        SET value = ?, updated_at = ?
        WHERE category = ? AND key = ?
        ''', (
            data.get('value'), 
            now,
            data.get('category'),
            data.get('key')
        ))
    else:
        # Insert new knowledge
        cursor.execute('''
        INSERT INTO agent_knowledge (category, key, value, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('category'), 
            data.get('key'), 
            data.get('value'), 
            now,
            now
        ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Agent knowledge saved successfully",
        "operation": "update" if existing else "insert"
    })

def save_code_pattern(cursor, conn, data):
    """Save code pattern data."""
    now = datetime.now().isoformat()
    
    # Check if pattern exists
    cursor.execute(
        "SELECT id, frequency FROM code_patterns WHERE pattern_type = ? AND language = ? AND pattern_name = ?", 
        (data.get('pattern_type'), data.get('language'), data.get('pattern_name'))
    )
    existing = cursor.fetchone()
    
    if existing:
        # Update existing pattern and increment frequency
        pattern_id, frequency = existing
        cursor.execute('''
        UPDATE code_patterns 
        SET pattern_example = ?, frequency = ?, last_observed = ?
        WHERE id = ?
        ''', (
            data.get('pattern_example'), 
            frequency + 1,
            now,
            pattern_id
        ))
    else:
        # Insert new pattern
        cursor.execute('''
        INSERT INTO code_patterns (pattern_type, language, pattern_name, pattern_example, last_observed)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('pattern_type'), 
            data.get('language'), 
            data.get('pattern_name'), 
            data.get('pattern_example'), 
            now
        ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Code pattern saved successfully",
        "operation": "update" if existing else "insert"
    })

def save_interaction_history(cursor, conn, data):
    """Save interaction history data."""
    now = datetime.now().isoformat()
    
    # Insert new interaction record
    cursor.execute('''
    INSERT INTO interaction_history (timestamp, action_type, file_path, description, context, success)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        now,
        data.get('action_type'), 
        data.get('file_path'), 
        data.get('description'), 
        data.get('context', ''),
        data.get('success', True)
    ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Interaction history saved successfully"
    })

def save_project_metric(cursor, conn, data):
    """Save project metric data."""
    now = datetime.now().isoformat()
    
    # Insert new metric
    cursor.execute('''
    INSERT INTO project_metrics (timestamp, metric_name, metric_value, metric_unit, context)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        now,
        data.get('metric_name'), 
        data.get('metric_value'), 
        data.get('metric_unit', ''),
        data.get('context', '')
    ))
    
    conn.commit()
    conn.close()
    
    return json.dumps({
        "status": "success",
        "message": "Project metric saved successfully"
    })

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "status": "error",
            "message": "Missing arguments. Usage: python db_save.py \"table_name\" '{\"json\": \"data\"}'"
        }))
        sys.exit(1)
    
    table = sys.argv[1]
    data = sys.argv[2]
    
    result = save_to_database(table, data)
    print(result)