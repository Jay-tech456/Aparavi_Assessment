from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from sqlalchemy import create_engine, text
import threading
import time
import datetime

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

DATABASE_URL = ""
engine = create_engine(DATABASE_URL)

@app.route('/data', methods=['GET'])
def get_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM HRCandidates LIMIT 10"))
        rows = [dict(row._mapping) for row in result]
        # Convert datetime objects to strings
        for row in rows:
            for key, value in row.items():
                if isinstance(value, datetime.datetime):
                    row[key] = value.isoformat()  # Convert datetime to ISO 8601 string
    return jsonify(rows)

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit_data()

def emit_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM HRCandidates LIMIT 10"))
        rows = [dict(row._mapping) for row in result]
        # Convert datetime objects to strings
        for row in rows:
            for key, value in row.items():
                if isinstance(value, datetime.datetime):
                    row[key] = value.isoformat()  # Convert datetime to ISO 8601 string
    socketio.emit('data', rows)

def background_thread():
    while True:
        emit_data()
        time.sleep(5) 

# Start background thread
threading.Thread(target=background_thread, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, port=5002, debug=True)
