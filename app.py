from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import init_database, get_last_3days

app = Flask(__name__, static_folder="public")
CORS(app)

# Initialize DB
init_database()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/last3days')
def last_3days():
    data = get_last_3days()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
