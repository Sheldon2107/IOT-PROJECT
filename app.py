from flask import Flask, jsonify, send_from_directory
from db import init_db, fetch_last_n_positions

app = Flask(__name__)
init_db()  # Create DB if not exists

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/last3days")
def last3days():
    # Fetch last 4320 entries (~1 per minute for 3 days)
    data = fetch_last_n_positions(4320)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
