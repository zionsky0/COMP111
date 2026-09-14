# Local web runner for COMP111 Interactive Suite
import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f'Starting COMP111 Interactive Learning Platform at http://localhost:{PORT}...')
webbrowser.open(f'http://localhost:{PORT}')
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    httpd.serve_forever()
