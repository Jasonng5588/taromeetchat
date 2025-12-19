import sys
import os

# Add backend to path to allow imports
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    print("1. Importing modules...")
    from backend.database import SessionLocal, init_db, engine
    from backend.models import User
    from passlib.context import CryptContext
    print("   Imports successful.")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def test_hashing():
    print("\n2. Testing Password Hashing...")
    try:
        pw = "password123"
        hashed = pwd_context.hash(pw)
        print(f"   Hashing success: {hashed[:10]}...")
        return hashed
    except Exception as e:
        print(f"❌ Hashing failed: {e}")
        return None

def test_db_insert(hashed_pw):
    print("\n3. Testing DB Insert...")
    try:
        # Initialize tables
        init_db()
        print("   DB Initialized.")
        
        db = SessionLocal()
        email = "debug_user@example.com"
        
        # Check existing
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("   User exists, deleting...")
            db.delete(existing)
            db.commit()
            
        new_user = User(
            email=email,
            username="DebugUser",
            hashed_password=hashed_pw
        )
        db.add(new_user)
        db.commit()
        print(f"   User inserted with ID: {new_user.id}")
        db.close()
    except Exception as e:
        print(f"❌ DB Insert failed: {e}")

if __name__ == "__main__":
    h = test_hashing()
    if h:
        test_db_insert(h)
