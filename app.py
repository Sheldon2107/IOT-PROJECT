from flask import Flask, jsonify, send_from_directory
from threading import Thread
import time
from fetch_iss import fetch_iss_data
from db import init_db, insert_telemetry, fetch_all_data, fetch_latest, compute_analytics, fetch_last_3_days

RATE_LIMIT = 1  # 1 request/sec
app = Flask(__name__, static_folder="static")

# Background collector
def collector():
    init_db()
    while True:
        data = fetch_iss_data()
        insert_telemetry(data)
        time.sleep(RATE_LIMIT)

Thread(target=collector, daemon=True).start()

# API endpoints
@app.route("/api/current")
def current():
    return jsonify(fetch_latest() or {})

@app.route("/api/data")
def data():
    return jsonify(fetch_all_data())

@app.route("/api/analytics")
def analytics():
    return jsonify(compute_analytics())

@app.route("/api/last3days")
def last3days():
    return jsonify(fetch_last_3_days())

# Serve dashboard
@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
