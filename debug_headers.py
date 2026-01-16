import os
import google.generativeai as genai
from dotenv import load_dotenv
import pprint

load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")

def inspect_gemini():
    if not KEY:
        print("No Key")
        return

    genai.configure(api_key=KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    print("Sending request...")
    try:
        response = model.generate_content("Hello")
        # Inspect available attributes
        print("\n--- Response Attributes ---")
        print(dir(response))
        
        # Check if there's any metadata or result object that holds headers
        # Often hidden in _result or similar, but we want public if possible.
        # However, for this task, we just need to find WHERE it is.
        
        if hasattr(response, 'usage_metadata'):
            print("\nUsage Metadata:")
            print(response.usage_metadata)
            
    except Exception as e:
        print(f"Error: {e}")
        # Check if exception has headers
        if hasattr(e, 'response'):
             print("Exception has response")

if __name__ == "__main__":
    inspect_gemini()
