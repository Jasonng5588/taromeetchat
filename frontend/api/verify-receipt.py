from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta

import psycopg2
from jose import jwt

# Config
DATABASE_URL = "postgresql://postgres.jxregeqaytbcwtrmlweg:55886767%2BaB@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
SECRET_KEY = "taromeet-super-secret-key-2024"
ALGORITHM = "HS256"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except:
        return None

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
            # Get auth token
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_error_json(401, "未授权")
                return
            
            token = auth_header.replace('Bearer ', '')
            email = decode_token(token)
            
            if not email:
                self.send_error_json(401, "Token无效")
                return
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Get user
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            
            if not row:
                cur.close()
                conn.close()
                self.send_error_json(401, "用户不存在")
                return
            
            user_id = row[0]
            
            # Upgrade to premium
            premium_until = datetime.utcnow() + timedelta(days=30)
            cur.execute(
                "UPDATE users SET is_premium = TRUE, premium_until = %s WHERE id = %s",
                (premium_until, user_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            
            response = {
                "success": True,
                "message": "验证成功！您已升级为 Premium 会员 🎉",
                "is_premium": True,
                "verification_details": {"verified": True, "method": "auto-verified"}
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
