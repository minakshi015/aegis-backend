import os
from app.gemini_service import generate_response
from dotenv import load_dotenv

load_dotenv()

print("Triggering Gemini Service...")
res = generate_response("Hello")
print("Result:", res)
