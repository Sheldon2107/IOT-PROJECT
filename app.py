from flask import Flask, jsonify, send_from_directory
from db import init_db, fetch_last_n_positions

app = Flask(__name__)
init_db()  # Initialize DB if not exists

# Serve index.html from static folder
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# API endpoint to get last 3 days (or last N entries)
@app.route("/api/last3days")
def last3days():
    # Example: fetching last 4320 positions (~1 per minute for 3 days)
    data = fetch_last_n_positions(4320)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
