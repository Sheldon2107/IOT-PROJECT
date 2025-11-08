from flask import Flask, jsonify
from db import init_db, fetch_last_n_positions

app = Flask(__name__)

init_db()

@app.route("/api/last3days")
def last3days():
    # Fetch last 4320 records (~3 days at 1 record per minute)
    data = fetch_last_n_positions(4320)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
