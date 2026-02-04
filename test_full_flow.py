import requests
import json
import time

API_URL = "http://localhost:8000/api/message"
API_KEY = "my-secret-key-123"

def send_message(session_id, history, current_msg):
    payload = {
        "sessionId": session_id,
        "message": current_msg,
        "conversationHistory": history,
        "metadata": {"channel": "SMS", "language": "en", "locale": "US"}
    }
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    
    try:
        # Simple retry logic
        for attempt in range(3):
            try:
                resp = requests.post(API_URL, json=payload, headers=headers)
                break
            except requests.exceptions.ConnectionError:
                if attempt < 2:
                    time.sleep(2)
                    continue
                raise

        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    return None

def main():
    session_id = f"test-flow-{int(time.time())}"
    history = []
    
    # Simulation: Scammer wants UPI ID
    scammer_lines = [
        "URGENT: Block warning! Verify immediately.",
        "Share your UPI ID to stop blocking.",
        "Yes, send me your UPI ID: scammer@okicic",
        "Also need your PIN for verification."
    ]
    
    print(f"--- Starting Full Flow Test: {session_id} ---")
    
    for i, line in enumerate(scammer_lines):
        # 1. Scammer speaks
        msg = {
            "sender": "scammer", "text": line, "timestamp": int(time.time() * 1000)
        }
        print(f"\n[Turn {i+1}] Scammer: {line}")
        
        resp = send_message(session_id, history, msg)
        
        if resp:
            print(f"Agent ({resp.get('status')}): {resp.get('reply')}")
            
            # Add to history
            history.append(msg)
            if resp.get('reply'):
                history.append({
                    "sender": "user", 
                    "text": resp.get('reply'), 
                    "timestamp": int(time.time() * 1000)
                })
        
        time.sleep(8) # Increase wait to avoid 429 Rate Limits

if __name__ == "__main__":
    main()
