# Verwende ein Python-Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere alle Dateien ins Container-Verzeichnis
COPY . .

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Port-Expose
EXPOSE 5000

# Startbefehl für die Flask-App
CMD ["python", "app.py"]
