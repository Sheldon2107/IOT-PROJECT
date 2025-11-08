import sqlite3
from pathlib import Path

DB_PATH = Path("iss_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS iss_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            velocity REAL,
            timestamp INTEGER,
            ts_utc TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(latitude, longitude, altitude, velocity, timestamp, ts_utc):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO iss_telemetry (latitude, longitude, altitude, velocity, timestamp, ts_utc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (latitude, longitude, altitude, velocity, timestamp, ts_utc))
    conn.commit()
    conn.close()

def fetch_last_days(days=3):
    from datetime import datetime, timedelta
    cutoff = int((datetime.utcnow() - timedelta(days=days)).timestamp())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT latitude, longitude, altitude, velocity, timestamp, ts_utc
        FROM iss_telemetry
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    ''', (cutoff,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "latitude": row[0],
            "longitude": row[1],
            "altitude": row[2],
            "velocity": row[3],
            "timestamp": row[4],
            "ts_utc": row[5]
        } for row in rows
    ]

# Initialize DB automatically
init_db()
