import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread
import socket


def is_web_server_running(port: int) -> bool:
    """Check if a web server is running on the specified port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("localhost", port))
        except socket.error:
            # If the bind fails, the port is likely in use
            return True
    return False


def start_web_server(folder, port=8000):
    """Start a simple HTTP server if not already running."""
    if is_web_server_running(port):
        print(f"Web server is already running on port {port}.")
        return

    os.chdir(folder)

    def run_server():
        with TCPServer(("", port), SimpleHTTPRequestHandler) as httpd:
            print(f"Serving HTTP on port {port}...")
            httpd.serve_forever()

    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    print(f"Web server started on http://localhost:{port}, serving {folder}")