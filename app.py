from flask import Flask, jsonify, render_template
from flask_cors import CORS
from db import init_database, get_last_n_days

app = Flask(__name__, template_folder='.')
CORS(app)

# Initialize database on startup
init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/last3days')
def last_3_days():
    data = get_last_n_days(3)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
