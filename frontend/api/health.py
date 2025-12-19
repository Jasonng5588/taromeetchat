"""
Health Check API - Vercel Serverless Function
GET /api/health
"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"status": "healthy", "app": "TaroMeet API (Vercel)"}
        self.wfile.write(json.dumps(response).encode())
