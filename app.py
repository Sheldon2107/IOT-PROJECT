from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import get_last_3_days

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for JS frontend

# Serve index.html from static
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# API endpoint to fetch last 3 days of ISS data
@app.route('/api/last3days')
def last_3_days():
    data = get_last_3_days()
    return jsonify(data)

if __name__ == "__main__":
    # Run on 0.0.0.0 for deployment, port 5000
    app.run(host='0.0.0.0', port=5000)
