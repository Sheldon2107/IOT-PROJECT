# db.py
import sqlite3
from datetime import datetime

DB_FILE = "iss_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sat_id INTEGER,
            name TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL,
            velocity REAL,
            timestamp_unix INTEGER,
            ts_utc TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_telemetry(data):
    if not data:
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    ts = data.get("timestamp") or int(datetime.utcnow().timestamp())
    ts_utc = datetime.utcfromtimestamp(ts).isoformat() + "Z"
    c.execute("""
        INSERT INTO telemetry (sat_id, name, latitude, longitude, altitude, velocity, timestamp_unix, ts_utc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("id"),
        data.get("name"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("altitude"),
        data.get("velocity"),
        ts,
        ts_utc
    ))
    conn.commit()
    conn.close()
