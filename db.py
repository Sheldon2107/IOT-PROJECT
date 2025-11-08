import sqlite3

DB_NAME = "iss_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS iss_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts_utc TEXT,
            latitude REAL,
            longitude REAL,
            altitude REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_position(ts_utc, latitude, longitude, altitude):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO iss_positions (ts_utc, latitude, longitude, altitude) VALUES (?,?,?,?)",
              (ts_utc, latitude, longitude, altitude))
    conn.commit()
    conn.close()

def fetch_last_n_positions(n=1000):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT ts_utc, latitude, longitude, altitude FROM iss_positions ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return [{"ts_utc": r[0], "latitude": r[1], "longitude": r[2], "altitude": r[3]} for r in reversed(rows)]
