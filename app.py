from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimnis!'
socketio = SocketIO(app, cors_allowed_origins="*")

DRAWINGS_FILE = 'drawings.json'

def load_drawings():
    if os.path.exists(DRAWINGS_FILE):
        with open(DRAWINGS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Fehler beim Laden der Zeichnungen.")
                return []
    else:
        return []

def save_drawings(drawings):
    with open(DRAWINGS_FILE, 'w') as file:
        json.dump(drawings, file)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    drawings = load_drawings()
    emit('load_drawings', drawings)

@socketio.on('draw')
def handle_draw(data):
    drawings = load_drawings()
    drawings.append(data)
    save_drawings(drawings)
    emit('draw', data, broadcast=True, include_self=False)

@socketio.on('clear')
def handle_clear():
    save_drawings([])
    emit('clear', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
