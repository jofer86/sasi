#!/usr/bin/env python3
"""
Flask API for accessing the SQLite database.
Provides endpoints for querying and accessing database information.
"""

import os
import sqlite3
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

DB_PATH = './data/cursor_agent.db'

def dict_factory(cursor, row):
    """Convert database row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/db/query', methods=['POST'])
def query_database():
    """Execute a query against the database."""
    if not request.json or 'query' not in request.json:
        return jsonify({"error": "No query provided"}), 400
    
    query = request.json['query']
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # If the query modifies data, commit changes
        if query.strip().lower().startswith(('insert', 'update', 'delete', 'create', 'drop', 'alter')):
            conn.commit()
            return jsonify({
                "status": "success",
                "message": "Query executed successfully",
                "rows_affected": cursor.rowcount
            })
        
        # For SELECT queries, return the results
        results = cursor.fetchall()
        conn.close()
        
        return jsonify({
            "status": "success",
            "count": len(results),
            "results": results
        })
        
    except sqlite3.Error as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/db/status', methods=['GET'])
def database_status():
    """Get database status and schema information."""
    if not os.path.exists(DB_PATH):
        return jsonify({
            "status": "error",
            "message": "Database does not exist",
            "exists": False
        }), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get schema for each table
        schema = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [{
                "name": row[1],
                "type": row[2],
                "notnull": row[3],
                "default": row[4],
                "pk": row[5]
            } for row in cursor.fetchall()]
            schema[table] = columns
        
        # Get row counts for each table
        row_counts = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_counts[table] = cursor.fetchone()[0]
        
        # Get database size
        db_size = os.path.getsize(DB_PATH)
        
        # Get last modified time
        last_modified = datetime.fromtimestamp(os.path.getmtime(DB_PATH)).isoformat()
        
        conn.close()
        
        return jsonify({
            "status": "success",
            "exists": True,
            "path": DB_PATH,
            "size_bytes": db_size,
            "last_modified": last_modified,
            "tables": tables,
            "schema": schema,
            "row_counts": row_counts
        })
        
    except sqlite3.Error as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "exists": True
        }), 500

@app.route('/api/docs', methods=['GET'])
def get_documentation():
    """Get API documentation."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        # Get all documentation entries
        cursor.execute("SELECT path, title, created_at, updated_at FROM documentation")
        docs = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "status": "success",
            "count": len(docs),
            "documentation": docs
        })
        
    except sqlite3.Error as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/docs/<path:doc_path>', methods=['GET'])
def get_documentation_content(doc_path):
    """Get specific documentation content."""
    try: