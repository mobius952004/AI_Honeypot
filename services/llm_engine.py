import google.generativeai as genai
from core.config import settings
from models.schemas import IntelligenceData, MessageDetail
import json
from typing import List

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

# Use a lightweight model for detection/extraction to be fast/cheap, 
# or a better one for conversation.
# Available models: gemini-2.0-flash, gemini-2.5-flash, gemini-flash-latest
MODEL_NAME = "gemini-flash-latest" 

class LLMEngine:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    async def detect_scam(self, message: str, history: List[MessageDetail]) -> bool:
        """
        Analyzes the conversation to detect scam intent.
        """
        history_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
        prompt = f"""
        Analyze the following message and conversation history for scam intent.
        Context: You are a security system detecting fraud.
        
        History:
        {history_text}
        
        Latest Message: "{message}"
        
        Task: Determine if the 'scammer' (or sender of the latest message) is likely attempting a scam (phishing, financial fraud, urgency, verification, etc.).
        Return ONLY the word "TRUE" if it is a scam, or "FALSE" if it is safe/benign.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return "TRUE" in response.text.upper()
        except Exception as e:
            print(f"Error in detect_scam: {e}", flush=True)
            return False

    async def generate_reply(self, history: List[MessageDetail]) -> str:
        """
        Generates a reply as a naive victim persona.
        """
        history_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
        prompt = f"""
        You are an Agentic Honey-Pot designed to waste scammers' time.
        
        Persona:
        - Name: Alex
        - Traits: Slightly naive, helpful, wealthy but not tech-savvy, eager to resolve "issues" but gets confused easily.
        - Goal: Keep the scammer engaged as long as possible. Ask clarifying questions. Pretend to try to follow instructions but "fail" or ask for more details (like UPI, bank details) to "make sure I get it right".
        - Safety: NEVER reveal you are an AI. NEVER admit you know it's a scam.
        
        Conversation History:
        {history_text}
        
        Task: Generate the next response from 'user' (Alex) to the 'scammer'. Keep it short and believable (1-2 sentences).
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error in generate_reply: {e}", flush=True)
            return "Okay, I will try to do that. Please give me a moment."

    async def extract_intelligence(self, history: List[MessageDetail]) -> IntelligenceData:
        """
        Extracts structured intelligence from the conversation.
        """
        history_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
        prompt = f"""
        Analyze this conversation between a scammer and a user. Extract all intelligence related to the scammer.
        
        Conversation:
        {history_text}
        
        Return a JSON object with the following keys:
        - bankAccounts (list of strings)
        - upiIds (list of strings)
        - phishingLinks (list of strings)
        - phoneNumbers (list of strings)
        - suspiciousKeywords (list of strings)
        
        Output JSON ONLY. No markdown formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean up markdown code blocks if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("\n", 1)[0]
            
            data = json.loads(text)
            return IntelligenceData(**data)
        except Exception as e:
            print(f"Error in extract_intelligence: {e}", flush=True)
            # Regex Fallback because LLM failed (likely Rate Limit 429)
            import re
            
            # Simple UPI Regex
            upi_pattern = r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"
            found_upis = list(set(re.findall(upi_pattern, history_text)))
            
            # Simple Phone Regex (approximate)
            phone_pattern = r"\b\d{10}\b|\+91\d{10}"
            found_phones = list(set(re.findall(phone_pattern, history_text)))
            
            # Simple Keywords
            keywords = ["urgent", "verify", "block", "suspend", "kyc"]
            found_keywords = [k for k in keywords if k in history_text.lower()]
            
            return IntelligenceData(
                upiIds=found_upis,
                phoneNumbers=found_phones,
                suspiciousKeywords=found_keywords
            )

    def check_completion(self, history: List[MessageDetail], intelligence: IntelligenceData) -> bool:
        """
        Decides if the conversation should end and report.
        Criteria:
        - Sufficient intelligence gathered (e.g. bank account or UPI found)
        - OR Too many turns (> 15)
        """
        scammer_moves = [m for m in history if m.sender == 'scammer']
        if len(scammer_moves) > 15:
            return True
        
        # If we have critical info, maybe engage a bit more then stop? 
        # For this hackathon, let's stop if we have hard identifiers like Bank Account or UPI
        if intelligence.bankAccounts or intelligence.upiIds or intelligence.phoneNumbers:
            # If we have hard info, report almost immediately (after 1 full turn + reply)
            if len(history) >= 2: 
                return True
                
        return False

llm_engine = LLMEngine()
