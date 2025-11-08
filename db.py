import sqlite3
from datetime import datetime

DB_FILE = "iss_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        ts_utc TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_position(lat, lon, alt, ts_utc=None):
    if ts_utc is None:
        ts_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO positions (latitude, longitude, altitude, ts_utc) VALUES (?, ?, ?, ?)",
              (lat, lon, alt, ts_utc))
    conn.commit()
    conn.close()

def fetch_last_n_positions(n):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT latitude, longitude, altitude, ts_utc FROM positions ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    # Return in chronological order
    return [{"latitude": r[0], "longitude": r[1], "altitude": r[2], "ts_utc": r[3]} for r in reversed(rows)]
