import sqlite3
from datetime import datetime

DB_PATH = 'iss_data.db'

def init_database():
    """Initialize the SQLite database with ISS telemetry table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iss_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            altitude REAL NOT NULL,
            velocity REAL NOT NULL,
            timestamp TEXT NOT NULL,
            visibility TEXT,
            footprint REAL,
            daynum REAL,
            solar_lat REAL,
            solar_lon REAL,
            units TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON iss_telemetry(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_altitude ON iss_telemetry(altitude)')
    
    conn.commit()
    conn.close()

def insert_telemetry(data: dict) -> bool:
    """Insert a telemetry record into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO iss_telemetry (
                latitude, longitude, altitude, velocity, timestamp,
                visibility, footprint, daynum, solar_lat, solar_lon, units
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('latitude'),
            data.get('longitude'),
            data.get('altitude'),
            data.get('velocity'),
            datetime.fromtimestamp(data.get('timestamp')).isoformat(),
            data.get('visibility'),
            data.get('footprint'),
            data.get('daynum'),
            data.get('solar_lat'),
            data.get('solar_lon'),
            data.get('units')
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting telemetry:", e)
        return False

def get_last_n_days(n_days=3):
    """Return all telemetry records from the last N days."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM iss_telemetry
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp ASC
        ''', (f'-{n_days} days',))
        rows = cursor.fetchall()
        conn.close()
        data = []
        for r in rows:
            data.append({
                'id': r[0],
                'latitude': r[1],
                'longitude': r[2],
                'altitude': r[3],
                'velocity': r[4],
                'ts_utc': r[5]
            })
        return data
    except Exception as e:
        print("Error fetching last n days:", e)
        return []
