import uvicorn
import os
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()

def start_server():
    # 1. Open a Ngrok tunnel to port 8000
    # Note: If you have an NGROK_AUTHTOKEN in .env, pyngrok will use it.
    # Otherwise, sessions might expire quickly.
    
    # Check for token in env, set it if present
    ngrok_token = os.getenv("NGROK_AUTHTOKEN")
    if ngrok_token:
        ngrok.set_auth_token(ngrok_token)

    try:
        public_url = ngrok.connect(8000).public_url
        print(f"\n\n[PUBLIC URL] Your API is accessible at: {public_url}")
        print(f"[NOTE] The message endpoint is: {public_url}/api/message\n\n")
    except Exception as e:
        print(f"Could not connect to ngrok: {e}")
        print("Please ensure you don't have other ngrok instances running or strict network policies.")

    # 2. Start Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    start_server()
