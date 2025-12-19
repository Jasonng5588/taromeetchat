"""
Register API - Vercel Serverless Function
POST /api/register
"""
from http.server import BaseHTTPRequestHandler
import json
from _db import SessionLocal, User, init_db
from _auth import get_password_hash, create_access_token

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            
            if not all([email, username, password]):
                self.send_error_response(400, "缺少必填字段")
                return
            
            db = SessionLocal()
            try:
                # Check if user exists
                existing = db.query(User).filter(User.email == email).first()
                if existing:
                    self.send_error_response(400, "该邮箱已被注册")
                    return
                
                # Create user
                hashed_password = get_password_hash(password)
                new_user = User(
                    email=email,
                    username=username,
                    hashed_password=hashed_password
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                # Create token
                access_token = create_access_token(data={"sub": email})
                
                response = {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": new_user.id,
                        "email": new_user.email,
                        "username": new_user.username,
                        "is_premium": new_user.is_premium
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
