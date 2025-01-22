from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimnis!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Der absolute Pfad zur Datei, sicherstellen, dass der Pfad stimmt
DRAWINGS_FILE = os.path.join(os.getcwd(), 'drawings.json')

def load_drawings():
    try:
        # Überprüfe, ob die Datei existiert und lade sie
        if os.path.exists(DRAWINGS_FILE):
            with open(DRAWINGS_FILE, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Fehler beim Laden der Zeichnungen.")
                    return []
        else:
            print(f"{DRAWINGS_FILE} existiert nicht, eine neue Datei wird erstellt.")
            return []
    except Exception as e:
        print(f"Fehler beim Laden der Datei {DRAWINGS_FILE}: {e}")
        return []

def save_drawings(drawings):
    try:
        # Speichern der Zeichnungen in der JSON-Datei
        with open(DRAWINGS_FILE, 'w') as file:
            json.dump(drawings, file)
    except Exception as e:
        print(f"Fehler beim Speichern der Zeichnungen: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Laden der Zeichnungen beim ersten Verbindungsaufbau
    drawings = load_drawings()
    emit('load_drawings', drawings)

@socketio.on('draw')
def handle_draw(data):
    # Zeichnungen empfangen und speichern
    drawings = load_drawings()
    drawings.append(data)
    save_drawings(drawings)
    emit('draw', data, broadcast=True, include_self=False)

@socketio.on('clear')
def handle_clear():
    # Alle Zeichnungen löschen
    save_drawings([])
    emit('clear', broadcast=True)

if __name__ == '__main__':
    # Holen des Ports aus der Umgebung (Render setzt diesen Port automatisch)
    port = os.environ.get("PORT", 5000)  # Falls kein Port gesetzt ist, benutze 5000 als Fallback
    socketio.run(app, host='0.0.0.0', port=port)  # Host auf 0.0.0.0 setzen, damit es überall zugänglich ist
