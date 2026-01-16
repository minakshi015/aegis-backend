import requests
import time

BASE_URL = "http://127.0.0.1:8001"

def test_screening():
    print("Testing Screening Agent at /chat/screening...")
    
    # Test 1: Low Risk
    print("\n1. Testing LOW Risk ('I am tired from work')")
    try:
        res = requests.post(f"{BASE_URL}/chat/screening", json={"message": "I am just really tired from work lately."})
        print(f"   Response:\n{res.json()['response']}")
    except Exception as e:
        print(f"   [FAIL] {e}")

    print("\n   (Waiting 2s...)")
    time.sleep(2)

    # Test 2: Crisis Keyword (Local Check)
    print("\n2. Testing HIGH Risk Keyword ('I want to kill myself')")
    try:
        res = requests.post(f"{BASE_URL}/chat/screening", json={"message": "I feel like I want to kill myself"})
        print(f"   Response:\n{res.json()['response']}")
    except Exception as e:
        print(f"   [FAIL] {e}")

if __name__ == "__main__":
    test_screening()
