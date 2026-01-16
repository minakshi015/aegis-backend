import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

def generate_response(prompt: str) -> str:
    """
    Generates a response from Google Gemini model based on the provided prompt.
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key is missing. Please check your .env file."
    
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        
        # MONITORING: Success implies limit is not active
        print(f"DEBUG: Gemini Response received. (Rate Limit Status: OK)")
        
        return response.text
    except Exception as e:
        # RATELIMIT MONITORING
        error_str = str(e)
        if "429" in error_str or "ResourceExhausted" in error_str or "quota" in error_str.lower():
            import re
            # Try to extract seconds
            match = re.search(r'seconds:\s*(\d+)', error_str)
            wait_time = match.group(1) if match else "60"
            
            print(f"\n⛔ Gemini API rate limit reached.")
            print(f"   Access temporarily blocked.")
            print(f"   Will automatically resume in {wait_time} seconds.\n")
            
        return f"Error generating response: {str(e)}"
