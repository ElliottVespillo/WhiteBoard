# Wähle ein Basis-Image für Python
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die lokalen Dateien in das Arbeitsverzeichnis im Container
COPY . /app

# Installiere die benötigten Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Exponiere den Port, auf dem die App laufen wird
EXPOSE 5000

# Definiere den Startbefehl, um die Flask-App auszuführen
CMD ["python", "app.py"]
