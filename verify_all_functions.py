import requests
import json
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test_user_verify@example.com"
TEST_PASSWORD = "password123"
TEST_USERNAME = "TestUserverify"

def print_result(name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {name}: {details}")

def verify_all():
    print("🚀 Starting Comprehensive API Verification...\n")
    
    # 1. Health Check
    try:
        r = requests.get(f"{BASE_URL}/health")
        print_result("Health Check", r.status_code == 200, r.text)
    except Exception as e:
        print_result("Health Check", False, str(e))
        return # Cannot proceed if server is down

    # 2. Authentication (Register/Login)
    token = None
    try:
        # Register
        payload = {"email": TEST_EMAIL, "username": TEST_USERNAME, "password": TEST_PASSWORD}
        r = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if r.status_code == 200:
            print_result("Register", True)
            token = r.json().get("access_token")
        elif r.status_code == 400: # Any 400 likely means user exists or bad request, try login
            print_result("Register", True, f"assuming user exists ({r.status_code})")
            # Login if already exists
            r = requests.post(f"{BASE_URL}/auth/login", data={"username": TEST_EMAIL, "password": TEST_PASSWORD})
            if r.status_code == 200:
                print_result("Login (after exist)", True)
                token = r.json().get("access_token")
            else:
                print_result("Login", False, r.text)
        else:
            print_result("Register", False, r.text)
    except Exception as e:
        print_result("Auth Flow", False, str(e))

    if not token:
        print("\n⚠️ Skipping authenticated tests due to login failure.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Mood Analysis
    try:
        payload = {"mood_text": "I feel happy today because I finished my work."}
        r = requests.post(f"{BASE_URL}/mood/analyze", json=payload, headers=headers)
        print_result("Mood Analysis", r.status_code == 200, "Got response" if r.status_code == 200 else r.text)
    except Exception as e:
        print_result("Mood Analysis", False, str(e))

    # 4. Love Coach
    try:
        payload = {"chat_content": "Him: Hi\nMe: Hello"}
        r = requests.post(f"{BASE_URL}/love/analyze", json=payload, headers=headers)
        print_result("Love Coach", r.status_code == 200, "Got response" if r.status_code == 200 else r.text)
    except Exception as e:
        print_result("Love Coach", False, str(e))

    # 5. Diary Reflection
    try:
        payload = {"content": "Today I learned a lot about coding."}
        r = requests.post(f"{BASE_URL}/diary/reflect", json=payload, headers=headers)
        print_result("Diary Reflection", r.status_code == 200, "Got response" if r.status_code == 200 else r.text)
    except Exception as e:
        print_result("Diary Reflection", False, str(e))

    # 6. Voice Companion
    try:
        payload = {"message": "Hello AI, how are you?"}
        r = requests.post(f"{BASE_URL}/voice/chat", json=payload, headers=headers)
        print_result("Voice Companion", r.status_code == 200, "Got response" if r.status_code == 200 else r.text)
    except Exception as e:
        print_result("Voice Companion", False, str(e))

    # 7. Tarot Draw
    try:
        payload = {"question": "What is my future?", "num_cards": 3}
        r = requests.post(f"{BASE_URL}/tarot/draw", json=payload, headers=headers)
        print_result("Tarot Draw", r.status_code == 200, "Got response" if r.status_code == 200 else r.text)
    except Exception as e:
        print_result("Tarot Draw", False, str(e))
        
    # 8. Payment (Simulate)
    # Note: Complex to test fully without valid receipt, but can check endpoint existence
    try:
        # Just checking if endpoint exists by sending bad data
        r = requests.post(f"{BASE_URL}/payment/verify-receipt", headers=headers)
        # 422 validation error means endpoint exists and pydantic is working
        print_result("Payment Endpoint Exists", r.status_code == 422, "Endpoint reachable")
    except Exception as e:
         print_result("Payment Endpoint", False, str(e))

if __name__ == "__main__":
    verify_all()
