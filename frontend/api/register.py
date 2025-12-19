from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Supabase connection
import psycopg2
from datetime import datetime, timedelta
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
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            email = data.get('email', '')
            username = data.get('username', '')
            password = data.get('password', '')
            
            if not all([email, username, password]):
                self.send_error_json(400, "缺少必填字段")
                return
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Check if user exists
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                cur.close()
                conn.close()
                self.send_error_json(400, "该邮箱已被注册")
                return
            
            # Create user
            hashed = pwd_context.hash(password)
            cur.execute(
                "INSERT INTO users (email, username, hashed_password, is_premium, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (email, username, hashed, False, datetime.utcnow())
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            # Create token
            token = create_access_token(email)
            
            response = {
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": user_id,
                    "email": email,
                    "username": username,
                    "is_premium": False
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
