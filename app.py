from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'iss_data.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/data')
def get_current_data():
    """Get recent ISS positions (last 100 records)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, latitude, longitude, altitude, velocity, timestamp as ts_utc
            FROM iss_telemetry
            ORDER BY timestamp DESC
            LIMIT 100
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'id': row['id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'altitude': row['altitude'],
                'velocity': row['velocity'],
                'ts_utc': row['ts_utc']
            })
        
        # Reverse to show oldest first
        data.reverse()
        return jsonify(data)
    
    except Exception as e:
        print(f"Error in /api/data: {e}")
        return jsonify([])

@app.route('/api/last3days')
def get_last_3_days():
    """Get ISS data from the last 3 days"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get data from last 3 days
        three_days_ago = (datetime.now() - timedelta(days=3)).isoformat()
        
        cursor.execute('''
            SELECT id, latitude, longitude, altitude, velocity, timestamp as ts_utc
            FROM iss_telemetry
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
        ''', (three_days_ago,))
        
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'id': row['id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'altitude': row['altitude'],
                'velocity': row['velocity'],
                'ts_utc': row['ts_utc']
            })
        
        return jsonify(data)
    
    except Exception as e:
        print(f"Error in /api/last3days: {e}")
        return jsonify([])

@app.route('/api/analytics')
def get_analytics():
    """Compute analytics on stored data"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get summary statistics
        cursor.execute('''
            SELECT 
                MIN(longitude) as min_lon,
                MAX(longitude) as max_lon,
                MIN(altitude) as min_alt,
                MAX(altitude) as max_alt,
                COUNT(*) as total_records
            FROM iss_telemetry
        ''')
        
        summary = cursor.fetchone()
        
        # Get top altitude changes
        cursor.execute('''
            SELECT 
                t1.timestamp as t1,
                t1.altitude as a1,
                t2.timestamp as t2,
                t2.altitude as a2,
                ABS(t2.altitude - t1.altitude) as delta
            FROM iss_telemetry t1
            JOIN iss_telemetry t2 ON t2.id = t1.id + 1
            ORDER BY delta DESC
            LIMIT 10
        ''')
        
        jumps = cursor.fetchall()
        conn.close()
        
        analytics = {
            'summary': {
                'min_lon': summary['min_lon'] or 0,
                'max_lon': summary['max_lon'] or 0,
                'min_alt': summary['min_alt'] or 0,
                'max_alt': summary['max_alt'] or 0,
                'total_records': summary['total_records'] or 0
            },
            'top_jumps': []
        }
        
        for jump in jumps:
            analytics['top_jumps'].append({
                't1': jump['t1'],
                'a1': jump['a1'],
                't2': jump['t2'],
                'a2': jump['a2'],
                'delta': jump['delta']
            })
        
        return jsonify(analytics)
    
    except Exception as e:
        print(f"Error in /api/analytics: {e}")
        return jsonify({
            'summary': {'min_lon': 0, 'max_lon': 0, 'min_alt': 0, 'max_alt': 0, 'total_records': 0},
            'top_jumps': []
        })

@app.route('/api/stats')
def get_stats():
    """Get overall system statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total records
        cursor.execute('SELECT COUNT(*) as total FROM iss_telemetry')
        total = cursor.fetchone()['total']
        
        # Date range
        cursor.execute('SELECT MIN(timestamp) as first, MAX(timestamp) as last FROM iss_telemetry')
        dates = cursor.fetchone()
        
        # Altitude statistics
        cursor.execute('''
            SELECT 
                AVG(altitude) as avg_alt,
                MIN(altitude) as min_alt,
                MAX(altitude) as max_alt
            FROM iss_telemetry
        ''')
        alt_stats = cursor.fetchone()
        
        conn.close()
        
        # Calculate duration
        duration_days = 0
        if dates['first'] and dates['last']:
            first_dt = datetime.fromisoformat(dates['first'])
            last_dt = datetime.fromisoformat(dates['last'])
            duration_days = (last_dt - first_dt).total_seconds() / 86400
        
        return jsonify({
            'total_records': total,
            'first_record': dates['first'],
            'last_record': dates['last'],
            'duration_days': round(duration_days, 2),
            'avg_altitude': round(alt_stats['avg_alt'], 2) if alt_stats['avg_alt'] else 0,
            'min_altitude': round(alt_stats['min_alt'], 2) if alt_stats['min_alt'] else 0,
            'max_altitude': round(alt_stats['max_alt'], 2) if alt_stats['max_alt'] else 0
        })
    
    except Exception as e:
        print(f"Error in /api/stats: {e}")
        return jsonify({
            'total_records': 0,
            'duration_days': 0,
            'avg_altitude': 0,
            'min_altitude': 0,
            'max_altitude': 0
        })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
