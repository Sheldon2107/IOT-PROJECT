from flask import Flask, jsonify, send_from_directory
from db import fetch_last_days
from pathlib import Path

app = Flask(__name__, static_folder="static")

# Serve index.html
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# API endpoint to fetch last 3 days of ISS telemetry
@app.route("/api/last3days")
def last_3_days():
    data = fetch_last_days(days=3)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
