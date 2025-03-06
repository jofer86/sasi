#!/usr/bin/env python3
"""
Database setup script for Cursor MCP.
Creates the SQLite database and necessary tables for documentation and project status.
"""

import os
import sqlite3
import json
from datetime import datetime

# Ensure scripts directory exists
os.makedirs('./scripts', exist_ok=True)

# Ensure data directory exists
os.makedirs('./data', exist_ok=True)

DB_PATH = './data/cursor_agent.db'

def setup_database():
    """Set up the SQLite database with all required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create documentation table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documentation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        title TEXT,
        content TEXT,
        tags TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    ''')
    
    # Create project status table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT,
        status TEXT,
        message TEXT,
        last_check TIMESTAMP
    )
    ''')
    
    # Create agent knowledge table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agent_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        key TEXT,
        value TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        UNIQUE(category, key)
    )
    ''')
    
    # Create code patterns table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS code_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern_type TEXT,
        language TEXT,
        pattern_name TEXT,
        pattern_example TEXT,
        frequency INTEGER DEFAULT 1,
        last_observed TIMESTAMP,
        UNIQUE(pattern_type, language, pattern_name)
    )
    ''')
    
    # Create interaction history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interaction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        action_type TEXT,
        file_path TEXT,
        description TEXT,
        context TEXT,
        success BOOLEAN
    )
    ''')
    
    # Create a table for project metrics
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        metric_name TEXT,
        metric_value REAL,
        metric_unit TEXT,
        context TEXT
    )
    ''')
    
    # Add some initial status entries
    cursor.execute('''
    INSERT OR IGNORE INTO project_status (component, status, message, last_check)
    VALUES (?, ?, ?, ?)
    ''', ('database', 'active', 'Database initialized', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    print(f"Database setup complete at {DB_PATH}")

if __name__ == "__main__":
    setup_database()
    print("Database initialization complete!")