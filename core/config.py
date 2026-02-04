import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_API_KEY = os.getenv("App_API_KEY", "secret")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    REPORTING_URL = os.getenv("REPORTING_URL", "https://hackathon.guvi.in/api/updateHoneyPotFinalResult")

settings = Settings()
