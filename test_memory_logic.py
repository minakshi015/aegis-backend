import requests
import time
import uuid

BASE_URL = "http://127.0.0.1:8001"

def test_memory_logic():
    # Generate a random name to ensure we aren't hitting cached/old data
    test_name = f"User_{uuid.uuid4().hex[:6]}"
    
    print(f"1. Telling AI my name is {test_name}...")
    payload_1 = {"message": f"Hi, my name is {test_name}. Please remember it."}
    try:
        res1 = requests.post(f"{BASE_URL}/chat/wellness", json=payload_1)
        res1.raise_for_status()
        print(f"   AI Response 1: {res1.json()['response'][:100]}...")
    except Exception as e:
        print(f"FAILED Step 1: {e}")
        return

    print("   (Waiting 2 seconds for DB write...)")
    time.sleep(2)

    print(f"2. Asking AI 'What is my name?'...")
    payload_2 = {"message": "What is my name?"}
    try:
        res2 = requests.post(f"{BASE_URL}/chat/wellness", json=payload_2)
        res2.raise_for_status()
        response_text = res2.json()['response']
        print(f"   AI Response 2: {response_text}")
        
        if test_name in response_text:
            print("\n[SUCCESS] Memory works! The AI recalled the name.")
        else:
            print("\n[FAIL] Memory failed. The AI did not mention the name.")
            print(f"Expected: {test_name}")
            print(f"Got: {response_text}")

    except Exception as e:
        print(f"FAILED Step 2: {e}")

if __name__ == "__main__":
    test_memory_logic()
