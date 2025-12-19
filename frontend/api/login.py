from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from datetime import datetime, timedelta

import psycopg2
from jose import jwt
from passlib.context import CryptContext

# Config
DATABASE_URL = "postgresql://postgres.jxregeqaytbcwtrmlweg:55886767%2BaB@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
SECRET_KEY = "taromeet-super-secret-key-2024"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def create_access_token(email):
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        return
    
    def do_POST(self):
        try:
            content_type = self.headers.get('Content-Type', '')
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data or JSON
            if 'application/x-www-form-urlencoded' in content_type:
                parsed = parse_qs(body)
                email = parsed.get('username', [''])[0]
                password = parsed.get('password', [''])[0]
            else:
                data = json.loads(body) if body else {}
                email = data.get('email') or data.get('username', '')
                password = data.get('password', '')
            
            if not email or not password:
                self.send_error_json(400, "缺少邮箱或密码")
                return
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Get user
            cur.execute("SELECT id, email, username, hashed_password, is_premium FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            
            if not row:
                cur.close()
                conn.close()
                self.send_error_json(401, "邮箱或密码错误")
                return
            
            user_id, user_email, username, hashed_password, is_premium = row
            
            if not pwd_context.verify(password, hashed_password):
                cur.close()
                conn.close()
                self.send_error_json(401, "邮箱或密码错误")
                return
            
            cur.close()
            conn.close()
            
            # Create token
            token = create_access_token(email)
            
            response = {
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user_id,
                    "email": user_email,
                    "username": username,
                    "is_premium": is_premium
                }
            }
            
            self.send_json(200, response)
            
        except Exception as e:
            self.send_error_json(500, str(e))
    
    def send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        return
    
    def send_error_json(self, status, message):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"detail": message}).encode())
        return
