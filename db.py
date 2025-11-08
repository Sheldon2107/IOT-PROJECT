import sqlite3

DB_PATH = "iss_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS iss_positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        altitude REAL,
        ts_utc INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert_position(lat, lon, alt, ts_utc):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO iss_positions (latitude, longitude, altitude, ts_utc) VALUES (?, ?, ?, ?)",
                (lat, lon, alt, ts_utc))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
