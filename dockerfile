# Verwende Python 3 Basis-Image
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere alle Dateien ins Container-Verzeichnis
COPY . .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Exponiere den Port 5000
EXPOSE 5000

# Setze den Startbefehl
CMD ["python3", "app.py"]
