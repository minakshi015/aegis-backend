import requests
import time

BASE_URL = "http://127.0.0.1:8001"

def test_medical():
    print("Testing Medical Agent via Orchestrator (/chat)...")
    
    # Test 1: Medical Symptom
    print("\n1. Testing Medical Intent ('I have a pounding headache and sensitivity to light')")
    try:
        res = requests.post(f"{BASE_URL}/chat", json={"message": "I have a pounding headache and sensitivity to light"})
        print(f"   Status: {res.status_code}")
        if res.status_code != 200:
            print(f"   Error Body: {res.text}")
        else:
            resp = res.json()['response']
            print(f"   Response:\n{resp[:200]}...")
            
            if "migraine" in resp.lower() or "headache" in resp.lower():
                print("   [SUCCESS] AI recognized symptoms.")
            else: 
                print("   [INFO] AI response might be generic or fallback.")
            
    except Exception as e:
        print(f"   [FAIL] {e}")

if __name__ == "__main__":
    test_medical()
