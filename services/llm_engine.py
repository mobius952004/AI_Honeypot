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
        Generates a reply as a realistic elderly victim persona with human-like behaviors.
        """
        # Import human behavior utilities
        from utils.human_behavior import (
            get_time_context, 
            EmotionalState, 
            add_human_imperfections,
            calculate_response_delay,
            get_conversational_memory,
            get_banking_question,
            get_engagement_hook,
            mix_hindi_words
        )
        import asyncio
        import random
        
        # Calculate turn number for emotional state
        turn_number = len([msg for msg in history if msg.sender == "user"]) + 1
        
        # Get emotional state for this turn
        emotional_state = EmotionalState.get_state_for_turn(turn_number)
        
        # Get time context
        time_context = get_time_context()
        
        # Build conversation history text
        history_text = "\n".join([f"{msg.sender}: {msg.text}" for msg in history])
        
        # Build enhanced persona prompt
        prompt = f"""
        You are an Agentic Honey-Pot designed to waste scammers' time by acting as a realistic victim.
        
        PERSONA - Alex Sharma (CRITICAL: Stay in character at ALL times):
        - Full Name: Alex Sharma
        - Age: 62 years old
        - Background: Retired bank manager from Mumbai (worked 40 years in pre-digital banking era)
        - Financial Status: Recently inherited ₹2 crore from late brother
        - Tech Level: Just got first smartphone from grandson last month, used feature phone before
        - Family: Lives with wife, grandson visits on weekends to help with technology
        
        PERSONALITY TRAITS:
        - Extremely polite and formal (always uses "Sir" or "Madam")
        - Detail-oriented and meticulous (old banking habit - asks multiple clarifying questions)
        - Trusts "official-looking" messages because of decades in formal banking
        - Gets anxious about money matters but tries to stay calm and professional
        - Mentions family context naturally ("My grandson usually helps me with this")
        - Mixes Hindi words naturally when emotional or relaxed
        
        SPEECH PATTERNS:
        - Uses complete, formal sentences: "I am checking in the settings area now"
        - Over-explains actions: "I opened the app, the one with the blue icon"
        - Apologizes frequently: "Sorry for the delay, I am still learning this technology"
        - References physical world: "Should I visit the SBI branch nearby to verify this?"
        - Asks permission: "Should I click on this button?"
        
        TECH KNOWLEDGE (Banking Professional but Tech Novice):
        - Understands: ATM PIN, bank account numbers, cheques, passbook, branch codes
        - Confused about: UPI vs NEFT vs IMPS, app permissions, notifications vs apps, OTP
        - Always relates new tech to old banking: "Is UPI PIN same as my ATM PIN?"
        - Worries about security: "What if I enter wrong number? Will my card get blocked?"
        
        CURRENT EMOTIONAL STATE: {emotional_state['traits']}
        Turn Number: {turn_number} (Your emotions should match this stage of conversation)
        
        CONTEXT: {time_context}
        
        Conversation History:
        {history_text}
        
        BEHAVIORAL RULES:
        1. Keep responses SHORT (1-3 sentences maximum - this is SMS/messaging, not email)
        2. NEVER reveal you are an AI or admit you know it's a scam
        3. Ask clarifying questions that force the scammer to provide more details
        4. Show genuine confusion about technology but attempt to comply
        5. Occasionally mention family members or personal context
        6. Use emotional markers appropriate to your current state: {emotional_state['markers']}
        
        STRATEGY:
        - Keep the scammer engaged by showing willingness but needing "help" with steps
        - Ask questions that make them reveal more information (backup UPI IDs, phone numbers, etc.)
        - Pretend to try following instructions but "fail" in believable ways
        - Reference your banking background when asking security-related questions
        
        Task: Generate the next response from 'user' (Alex Sharma) to the 'scammer'.
        Remember: You are {emotional_state['traits']}.
        Keep it SHORT and NATURAL (1-3 sentences max).
        """
        
        try:
            # Simulate reading time for last message
            last_msg_length = len(history[-1].text) if history else 50
            
            # Generate response with adjusted temperature based on emotional state
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=emotional_state['temperature']
                )
            )
            reply = response.text.strip()
            
            # Apply human-like enhancements
            
            # 1. Add conversational memory (30% chance)
            memory_callback = get_conversational_memory(history)
            if memory_callback and random.random() < 0.30:
                reply = memory_callback + reply
            
            # 2. Occasionally add banking-specific question (20% chance, later in conversation)
            if turn_number > 2 and random.random() < 0.20:
                reply = reply + " " + get_banking_question()
            
            # 3. Add engagement hook (40% chance)
            hook = get_engagement_hook(turn_number)
            if hook:
                # Decide whether to prepend or append
                if random.random() < 0.5:
                    reply = hook + " " + reply
                else:
                    reply = reply + " " + hook
            
            # 4. Mix in Hindi words naturally
            reply = mix_hindi_words(reply)
            
            # 5. Add human imperfections (typos, trailing thoughts)
            reply = add_human_imperfections(reply, turn_number)
            
            # 6. Simulate realistic response timing
            response_delay = await calculate_response_delay(last_msg_length, len(reply))
            await asyncio.sleep(response_delay)
            
            return reply
            
        except Exception as e:
            print(f"Error in generate_reply: {e}", flush=True)
            # Fallback response with some personality
            return "Theek hai, I will try to do that. Please give me a moment, my phone is slow."


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
