"""
Gianni Data Lab - Servidor Local
Sirve la web portfolio y permite ejecutar proyectos (.bat) desde el navegador.
"""

import http.server
import socketserver
import json
import subprocess
import os
import webbrowser
import threading
import sys

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Registry of launchable projects
PROJECTS = {
    "jugos-sa": {
        "bat": os.path.join(BASE_DIR, "JUGOS SA", "INICIAR_SISTEMA.bat"),
        "cwd": os.path.join(BASE_DIR, "JUGOS SA"),
    }
}


class GianniHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves files and handles project launch requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/launch":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                project_id = data.get("project")
            except (json.JSONDecodeError, AttributeError):
                self._respond(400, {"error": "JSON invalido"})
                return

            project = PROJECTS.get(project_id)
            if not project:
                self._respond(404, {"error": f"Proyecto '{project_id}' no encontrado"})
                return

            bat_path = project["bat"]
            cwd = project["cwd"]

            if not os.path.isfile(bat_path):
                self._respond(404, {"error": f"Archivo no encontrado: {bat_path}"})
                return

            try:
                # Launch the .bat in a new cmd window, non-blocking
                subprocess.Popen(
                    ["cmd", "/c", "start", "", bat_path],
                    cwd=cwd,
                    shell=True,
                )
                self._respond(200, {"ok": True, "message": f"Ejecutando {os.path.basename(bat_path)}"})
            except Exception as e:
                self._respond(500, {"error": str(e)})
            return

        self._respond(404, {"error": "Ruta no encontrada"})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # Suppress default access logs to keep console clean
    def log_message(self, format, *args):
        msg = format % args
        if "POST /api/launch" in msg:
            print(f"  >> {msg}")


def main():
    os.chdir(BASE_DIR)

    with socketserver.TCPServer(("", PORT), GianniHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print()
        print("=" * 50)
        print("  GIANNI DATA LAB - Servidor Local")
        print("=" * 50)
        print(f"  URL: {url}")
        print(f"  Directorio: {BASE_DIR}")
        print()
        print("  Abri tu navegador en la URL de arriba.")
        print("  Para detener: Ctrl+C o cerra esta ventana.")
        print("=" * 50)
        print()

        # Open browser after a short delay
        def open_browser():
            import time
            time.sleep(1)
            webbrowser.open(url)

        threading.Thread(target=open_browser, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            httpd.shutdown()


if __name__ == "__main__":
    main()
