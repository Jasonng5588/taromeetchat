"""
Login API - Vercel Serverless Function
POST /api/login
"""
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from _db import SessionLocal, User
from _auth import verify_password, create_access_token

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_type = self.headers.get('Content-Type', '')
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data or JSON
            if 'application/x-www-form-urlencoded' in content_type:
                parsed = parse_qs(body)
                email = parsed.get('username', [''])[0]  # OAuth2 uses 'username' field
                password = parsed.get('password', [''])[0]
            else:
                data = json.loads(body)
                email = data.get('email') or data.get('username')
                password = data.get('password')
            
            if not email or not password:
                self.send_error_response(400, "缺少邮箱或密码")
                return
            
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.email == email).first()
                
                if not user or not verify_password(password, user.hashed_password):
                    self.send_error_response(401, "邮箱或密码错误")
                    return
                
                access_token = create_access_token(data={"sub": email})
                
                response = {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "is_premium": user.is_premium
                    }
                }
                
                self.send_json_response(200, response)
            finally:
                db.close()
                
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def send_json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, status, message):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"detail": message}).encode())
