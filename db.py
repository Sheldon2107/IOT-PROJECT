import sqlite3
from datetime import datetime

DB_PATH = 'iss_data.db'

def init_database():
    """Initialize the database and tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER,
            ts_utc TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            velocity REAL
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON telemetry(timestamp)')
    conn.commit()
    conn.close()
    print("✅ Database initialized.")

def insert_telemetry(data):
    """Insert a new ISS telemetry record."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ts_utc = datetime.utcfromtimestamp(data['timestamp']).isoformat()
        cursor.execute('''
            INSERT INTO telemetry (timestamp, ts_utc, latitude, longitude, altitude, velocity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['timestamp'], ts_utc, data['latitude'], data['longitude'], data['altitude'], data['velocity']))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def get_last_3days():
    """Return all telemetry from last 3 days."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        three_days_ago = int(datetime.utcnow().timestamp()) - 3*24*3600
        cursor.execute('''
            SELECT * FROM telemetry WHERE timestamp >= ? ORDER BY timestamp ASC
        ''', (three_days_ago,))
        rows = cursor.fetchall()
        conn.close()
        # Convert rows to dict list
        return [
            {
                "id": r[0],
                "timestamp": r[1],
                "ts_utc": r[2],
                "latitude": r[3],
                "longitude": r[4],
                "altitude": r[5],
                "velocity": r[6]
            } for r in rows
        ]
    except Exception as e:
        print(f"❌ Error fetching last 3 days: {e}")
        return []
