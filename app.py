from flask import Flask, jsonify, request
import sqlite3
import os
import json

app = Flask(__name__)
DB_PATH = './data/cursor_agent.db'

def dict_factory(cursor, row):
    """Convert database row to dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/db/query', methods=['POST'])
def query_db():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    if not os.path.exists(DB_PATH):
        return jsonify({'error': 'Database does not exist'}), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        if query.strip().lower().startswith(('insert', 'update', 'delete', 'create', 'drop', 'alter')):
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': 'Query executed successfully',
                'rows_affected': cursor.rowcount
            })
        
        results = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'results': results
        })
        
    except sqlite3.Error as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/db/status', methods=['GET'])
def db_status():
    if not os.path.exists(DB_PATH):
        return jsonify({'status': 'disconnected', 'message': 'Database file not found'}), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get database size
        db_size = os.path.getsize(DB_PATH)
        
        conn.close()
        
        return jsonify({
            'status': 'connected',
            'tables': tables,
            'size_bytes': db_size,
            'db_path': DB_PATH
        })
        
    except sqlite3.Error as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 