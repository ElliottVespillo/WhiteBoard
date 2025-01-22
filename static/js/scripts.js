<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zeichenbrett</title>
    <style>
        /* Stil für die Zeichenfläche */
        canvas {
            border: 1px solid black;
            cursor: crosshair;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/socket.io-client@4.0.1/dist/socket.io.min.js"></script>
</head>
<body>
    <h1>Gemeinsam Zeichnen</h1>
    <canvas id="drawingCanvas" width="800" height="600"></canvas>
    <script>
        const canvas = document.getElementById('drawingCanvas');
        const ctx = canvas.getContext('2d');
        const socket = io.connect(location.origin);

        let drawing = false;
        let lastX = 0;
        let lastY = 0;

        // Wenn der Benutzer beginnt zu zeichnen
        canvas.addEventListener('mousedown', (e) => {
            drawing = true;
            lastX = e.offsetX;
            lastY = e.offsetY;
        });

        // Wenn der Benutzer den Stift bewegt
        canvas.addEventListener('mousemove', (e) => {
            if (!drawing) return;
            const x = e.offsetX;
            const y = e.offsetY;

            // Zeichnen der Linie
            drawLine(lastX, lastY, x, y);
            lastX = x;
            lastY = y;

            // Senden der Zeichnungsdaten an den Server
            socket.emit('draw', { x1: lastX, y1: lastY, x2: x, y2: y, color: 'black', size: 2 });
        });

        // Wenn der Benutzer die Maus loslässt
        canvas.addEventListener('mouseup', () => {
            drawing = false;
        });

        // Wenn der Benutzer die Maus verlässt
        canvas.addEventListener('mouseleave', () => {
            drawing = false;
        });

        // Funktion zum Zeichnen auf der Leinwand
        function drawLine(x1, y1, x2, y2, color = 'black', size = 2) {
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.strokeStyle = color;
            ctx.lineWidth = size;
            ctx.stroke();
        }

        // Wenn eine Zeichnung von einem anderen Client empfangen wird
        socket.on('draw', (data) => {
            drawLine(data.x1, data.y1, data.x2, data.y2, data.color, data.size);
        });

        // Zeichnungen aus der JSON-Datei beim Laden der Seite anzeigen
        const initialDrawings = {{ drawings | tojson }};
        initialDrawings.forEach((data) => {
            drawLine(data.x1, data.y1, data.x2, data.y2, data.color, data.size);
        });
    </script>
</body>
</html>
