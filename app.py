from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import get_last_3_days

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/last3days')
def last_3_days():
    data = get_last_3_days()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
