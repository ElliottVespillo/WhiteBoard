from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimnis!'  # Dein Geheimschlüssel
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

DRAWINGS_FILE = 'drawings.json'  # Dateiname für die Zeichnungen

def load_drawings():
    """Lädt die gespeicherten Zeichnungen aus der JSON-Datei."""
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
    """Speichert die Zeichnungen in der JSON-Datei."""
    with open(DRAWINGS_FILE, 'w') as file:
        json.dump(drawings, file)

@app.route('/')
def index():
    """Lädt die Hauptseite (index.html)."""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Wird aufgerufen, wenn der Client eine Verbindung herstellt."""
    drawings = load_drawings()  # Zeichnungen laden
    emit('load_drawings', drawings)  # Zeichnungen an den Client senden

@socketio.on('draw')
def handle_draw(data):
    """Wird aufgerufen, wenn der Client eine Zeichnung sendet."""
    drawings = load_drawings()  # Zeichnungen laden
    drawings.append(data)  # Neue Zeichnung hinzufügen
    save_drawings(drawings)  # Zeichnungen speichern
    emit('draw', data, broadcast=True, include_self=False)  # Zeichnung an alle Clients senden

@socketio.on('clear')
def handle_clear():
    """Wird aufgerufen, wenn der Client den Bildschirm löschen möchte."""
    save_drawings([])  # Alle Zeichnungen löschen
    emit('clear', broadcast=True)  # Allen Clients mitteilen, dass der Bildschirm gelöscht wurde

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)  # Render setzt den Port automatisch
    socketio.run(app, host='0.0.0.0', port=port)  # Server starten
