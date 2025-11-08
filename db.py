import sqlite3
from datetime import datetime, timedelta

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

def fetch_all_data():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT latitude, longitude, altitude, ts_utc FROM telemetry ORDER BY timestamp_unix ASC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def fetch_latest():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM telemetry ORDER BY timestamp_unix DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def compute_analytics():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT MIN(longitude) as min_lon, MAX(longitude) as max_lon,
               MIN(altitude) as min_alt, MAX(altitude) as max_alt
        FROM telemetry
    """)
    summary = dict(c.fetchone())
    
    # Top altitude jumps
    c.execute("""
        SELECT t1.ts_utc as t1, t1.altitude as a1, t2.ts_utc as t2, t2.altitude as a2,
               ABS(t2.altitude - t1.altitude) as delta
        FROM telemetry t1
        JOIN telemetry t2 ON t2.id = t1.id + 1
        ORDER BY delta DESC
        LIMIT 5
    """)
    jumps = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"summary": summary, "top_jumps": jumps}

def fetch_last_3_days(limit_per_day=20):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    three_days_ago = int((datetime.utcnow() - timedelta(days=3)).timestamp())
    c.execute("SELECT * FROM telemetry WHERE timestamp_unix >= ? ORDER BY timestamp_unix ASC", (three_days_ago,))
    rows = [dict(r) for r in c.fetchall()]
    # sample 20 per day (assuming data recorded every sec, take every n-th row)
    sampled = []
    day_counts = {}
    for r in rows:
        day = r['ts_utc'][:10]
        if day not in day_counts:
            day_counts[day] = 0
        if day_counts[day] < limit_per_day:
            sampled.append(r)
            day_counts[day] += 1
    conn.close()
    return sampled
