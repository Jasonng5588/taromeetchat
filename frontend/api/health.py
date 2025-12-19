from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add api folder to path for imports
sys.path.insert(0, os.path.dirname(__file__))

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"status": "healthy", "app": "TaroMeet API"}
        self.wfile.write(json.dumps(response).encode())
        return
