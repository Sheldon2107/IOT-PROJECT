import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'iss_data.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS iss_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            velocity REAL,
            timestamp INTEGER,
            ts_utc TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(lat, lon, alt, vel, ts, ts_utc):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO iss_telemetry (latitude, longitude, altitude, velocity, timestamp, ts_utc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (lat, lon, alt, vel, ts, ts_utc))
    conn.commit()
    conn.close()

def get_last_3_days():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    c.execute('''
        SELECT latitude, longitude, altitude, velocity, timestamp, ts_utc 
        FROM iss_telemetry
        WHERE created_at >= ?
        ORDER BY timestamp ASC
    ''', (three_days_ago.isoformat(),))
    rows = c.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append({
            'latitude': row[0],
            'longitude': row[1],
            'altitude': row[2],
            'velocity': row[3],
            'timestamp': row[4],
            'ts_utc': row[5]
        })
    return data

# Initialize table on module load
create_table()
