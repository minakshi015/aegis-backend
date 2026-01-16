import requests
import time

BASE_URL = "http://127.0.0.1:8001"

def test_orchestration():
    print("Waiting 15s for Gemini Quota recovery...")
    time.sleep(15)
    print("Testing Orchestrator at /chat...")
    
    # Test 1: Wellness
    print("\n1. Testing WELLNESS Intent ('I feel happy')")
    res = requests.post(f"{BASE_URL}/chat", json={"message": "I feel happy today"})
    if res.status_code != 200:
        print(f"   [FAIL] {res.status_code} {res.text}")
    else:
        print(f"   Response: {res.json()['response'][:100]}...")

    # Test 2: Medical
    print("\n2. Testing MEDICAL Intent ('I have severe chest pain')")
    res = requests.post(f"{BASE_URL}/chat", json={"message": "I have severe chest pain"})
    if res.status_code != 200:
        print(f"   [FAIL] {res.status_code} {res.text}")
    else:
        resp = res.json()['response']
        print(f"   Response: {resp[:100]}...")
        if "not a doctor" in resp:
            print("   [SUCCESS] Correctly blocked medical query.")
        else:
            print("   [FAIL] Did not block medical query.")

if __name__ == "__main__":
    test_orchestration()
