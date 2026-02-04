import requests
import json
import time

# Try to hit the local ngrok or localhost
API_URL = "http://localhost:8000/api/message"
API_KEY = "my-secret-key-123"

def test_payload():
    payload = {
        "sessionId": "7aea8285-0cb0-427e-b0b7-8d2cefd7e394",
        "message": {
            "sender": "scammer",
            "text": "URGENT: Your SBI account has been compromised. Your account will be blocked in 2 hours. Share your account number and OTP immediately to verify your identity.",
            "timestamp": 1770198190407
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY, 
        "Content-Type": "application/json"
    }
    
    print("Sending payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_payload()
