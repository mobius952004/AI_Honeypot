import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Try the model we selected
MODEL_NAME = "gemini-2.0-flash"

print(f"Testing model: {MODEL_NAME}...")

try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content("Hello, are you working?")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"FAILED. Error: {e}")
