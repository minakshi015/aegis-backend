import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8001"

def test_health():
    print(f"Checking {BASE_URL}/health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        print(f"[OK] Health Check Passed: {response.json()}", flush=True)
    except Exception as e:
        print(f"[FAIL] Health Check Failed: {e}", flush=True)
        sys.exit(1)

def test_create_conversation():
    print(f"\nCreating conversation at {BASE_URL}/conversations...", flush=True)
    try:
        payload = {"message": "Hello from Python Test Script"}
        response = requests.post(f"{BASE_URL}/conversations", json=payload)
        response.raise_for_status()
        print(f"[OK] Create Conversation Passed: {response.json()}", flush=True)
    except Exception as e:
        print(f"[FAIL] Create Conversation Failed: {e}", flush=True)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}", flush=True)

def test_get_conversations():
    print(f"\nFetching conversations from {BASE_URL}/conversations...", flush=True)
    try:
        response = requests.get(f"{BASE_URL}/conversations")
        response.raise_for_status()
        data = response.json()
        print(f"[OK] Get Conversations Passed: Retrieved {len(data)} records", flush=True)
        print(json.dumps(data, indent=2), flush=True)
    except Exception as e:
        print(f"[FAIL] Get Conversations Failed: {e}", flush=True)

def test_llm():
    print(f"\nTesting LLM at {BASE_URL}/llm/test...", flush=True)
    payload = {"prompt": "Say hello to the reviewer"}
    try:
        response = requests.post(f"{BASE_URL}/llm/test", json=payload)
        response.raise_for_status()
        print(f"[OK] LLM Test Passed: {response.json()}", flush=True)
    except Exception as e:
        print(f"[FAIL] LLM Test Failed: {e}", flush=True)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}", flush=True)

def test_wellness():
    print(f"\nTesting Wellness Agent at {BASE_URL}/chat/wellness...", flush=True)
    payload = {"message": "I am feeling a bit tired today"}
    try:
        response = requests.post(f"{BASE_URL}/chat/wellness", json=payload)
        response.raise_for_status()
        print(f"[OK] Wellness Test Passed: {response.json()}", flush=True)
    except Exception as e:
        print(f"[FAIL] Wellness Test Failed: {e}", flush=True)
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}", flush=True)

if __name__ == "__main__":
    import time
    print("Starting tests...", flush=True)
    time.sleep(1) # Give server a moment if just started
    
    test_health()
    test_create_conversation()
    test_get_conversations()
    test_llm()
    test_wellness()
