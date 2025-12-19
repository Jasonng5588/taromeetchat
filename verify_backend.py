import requests
import sqlite3
import os

print("--- Checking Backend ---")
try:
    r = requests.get("http://localhost:8000/health")
    if r.status_code == 200:
        print("Backend HEALTHY:", r.json())
    else:
        print("Backend returned:", r.status_code, r.text)
except Exception as e:
    print("Backend FAILED:", e)

print("\n--- Checking Database ---")
db_path = "c:/TarotMeet/backend/taromeet.db"
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables found:", [t[0] for t in tables])
        
        # Check users table
        if ('users',) in tables:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print("Users columns:", [c[1] for c in columns])
        conn.close()
    except Exception as e:
        print("Database error:", e)
else:
    print("Database file NOT FOUND")
