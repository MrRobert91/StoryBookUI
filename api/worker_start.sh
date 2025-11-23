#!/bin/bash

# Definir el puerto (usa la variable de entorno PORT o 8000 por defecto)
PORT="${PORT:-8000}"

# Crear un pequeño servidor HTTP en Python en segundo plano para el healthcheck
# Responde 200 OK a cualquier GET request
python3 -c "
import http.server
import socketserver

PORT = $PORT
Handler = http.server.SimpleHTTPRequestHandler

# Sobrescribir log_message para que no llene los logs de basura
def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(b'OK')

Handler.do_GET = do_GET

with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f'Healthcheck server listening on port {PORT}')
    httpd.serve_forever()
" &

# Guardar el PID del servidor HTTP para matarlo si el script termina (opcional)
HTTP_PID=$!

# Iniciar el worker de Celery
# Usamos 'exec' para que Celery sea el proceso principal (PID 1) después del script
# Generar un hostname único usando el hostname del contenedor (que suele ser único o aleatorio)
HOSTNAME=$(hostname)
echo "Starting Celery worker with hostname: celery@$HOSTNAME"

exec celery -A api.tasks worker --loglevel=info --pool=solo -n "celery@$HOSTNAME"