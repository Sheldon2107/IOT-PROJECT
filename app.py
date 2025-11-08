# app.py
from flask import Flask, jsonify, send_from_directory
from threading import Thread
import time
from fetch_iss import fetch_iss_data
from db import init_db, insert_telemetry, DB_FILE
import sqlite3

RATE_LIMIT = 1  # seconds
app = Flask(__name__, static_folder="static")

# --- Background Collector Thread ---
def collector():
    init_db()
    while True:
        data = fetch_iss_data()
        insert_telemetry(data)
        if data:
            print(f"{data['ts_utc']} | lat={data['latitude']:.4f} lon={data['longitude']:.4f} alt={data['altitude']:.2f}")
        time.sleep(RATE_LIMIT)

collector_thread = Thread(target=collector, daemon=True)
collector_thread.start()

# --- API Endpoints ---
@app.route("/api/current")
def current():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM telemetry ORDER BY timestamp_unix DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return jsonify(dict(row) if row else {})

@app.route("/api/data")
def data():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT latitude, longitude, altitude, ts_utc FROM telemetry ORDER BY timestamp_unix ASC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/analytics")
def analytics():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT MIN(longitude) as min_lon, MAX(longitude) as max_lon, MIN(altitude) as min_alt, MAX(altitude) as max_alt FROM telemetry")
    summary = dict(c.fetchone())
    # largest altitude jumps
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
    return jsonify({"summary": summary, "top_jumps": jumps})

# --- Frontend ---
@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

