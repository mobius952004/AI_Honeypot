import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API key found")
    exit(1)

genai.configure(api_key=api_key)

models_to_test = ["gemini-flash-latest", "gemini-1.5-flash", "gemini-pro"]

for model_name in models_to_test:
    print(f"\nTesting model: {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, just a test.")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"FAILED. Error: {e}")
