from flask import Flask, jsonify, send_from_directory
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder="static")
DB_PATH = "iss_data.db"

def get_last_3days():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    three_days_ago = int((datetime.utcnow() - timedelta(days=3)).timestamp())
    cur.execute("SELECT latitude, longitude, altitude, ts_utc FROM iss_positions WHERE ts_utc >= ? ORDER BY ts_utc ASC", (three_days_ago,))
    rows = cur.fetchall()
    conn.close()
    return [{
        "latitude": r[0],
        "longitude": r[1],
        "altitude": r[2],
        "ts_utc": datetime.utcfromtimestamp(r[3]).strftime("%Y-%m-%d %H:%M:%S")
    } for r in rows]

@app.route("/api/last3days")
def last_3days():
    return jsonify(get_last_3days())

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
