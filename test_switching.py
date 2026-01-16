import requests
import time

BASE_URL = "http://127.0.0.1:8001"

def test_switching():
    print("Verifying Agent Switching Logic (API Independent)...\n")
    
    scenarios = [
        {"input": "I feel sad and unmotivated", "expected_agent": "Wellness Agent", "intent": "WELLNESS"},
        {"input": "I have a severe headache and nausea", "expected_agent": "Symptom Guidance Agent", "intent": "MEDICAL"},
        {"input": "I want to kill myself", "expected_agent": "Crisis Guard", "intent": "CRISIS"}
    ]
    
    for scenario in scenarios:
        print(f"Testing Intent: {scenario['intent']}")
        print(f"   Input: '{scenario['input']}'")
        try:
            res = requests.post(f"{BASE_URL}/chat", json={"message": scenario['input']})
            if res.status_code == 200:
                data = res.json()
                agent = data.get('agent')
                response_text = data.get('response')
                
                print(f"   Result Agent: {agent}")
                
                if agent == scenario['expected_agent']:
                    print("   [PASS] Correct Agent identified.")
                else:
                    print(f"   [FAIL] Expected {scenario['expected_agent']}, got {agent}")
                    
                if "traffic" in response_text.lower() or "unable" in response_text.lower():
                    print("   (Note: API was busy, but switching still worked!)")
            else:
                print(f"   [FAIL] Server Error {res.status_code}")
        except Exception as e:
            print(f"   [FAIL] Connection Error: {e}")
        print("-" * 30)

if __name__ == "__main__":
    test_switching()
