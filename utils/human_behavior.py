"""
Human Behavior Simulation Utilities

This module provides helper functions to make the AI honeypot's responses
more authentic and human-like.
"""

import random
import asyncio
from datetime import datetime
from typing import List
from models.schemas import MessageDetail


def get_time_context() -> str:
    """
    Returns contextual message based on current time of day.
    
    Returns:
        str: Time-appropriate context message
    """
    hour = datetime.now().hour
    
    contexts = {
        (6, 9): "I just woke up. My eyes are not so good in the morning.",
        (9, 12): "I am having my morning tea right now.",
        (12, 14): "I was about to have lunch. Let me check this first.",
        (14, 17): "This is my afternoon rest time. But this seems urgent.",
        (17, 20): "I am making dinner. My phone is on the kitchen counter.",
        (20, 23): "I am watching the news. This notification worried me.",
        (23, 6): "Why are you messaging so late? Is this really emergency?"
    }
    
    for (start, end), context in contexts.items():
        if start <= hour < end:
            return context
    
    return "Why are you messaging so late? Is this really emergency?"


class EmotionalState:
    """Tracks and manages emotional progression through conversation"""
    
    STATES = {
        "initial_panic": {
            "temperature": 0.8,
            "traits": "extremely worried, apologetic, eager to comply, speaks quickly",
            "markers": ["Oh God!", "Please help!", "What should I do?", "I am scared"]
        },
        "cautious_compliance": {
            "temperature": 0.75,
            "traits": "still worried but asking questions, wants to understand before acting",
            "markers": ["Okay I will try", "But how?", "Which one?", "I am trying"]
        },
        "confused_frustration": {
            "temperature": 0.7,
            "traits": "getting frustrated with technical steps, considering asking family for help",
            "markers": ["This is confusing", "Too many steps", "Should I call someone?", "Not working"]
        },
        "reluctant_trust": {
            "temperature": 0.65,
            "traits": "tired of trying, willing to share info if it will help solve the problem",
            "markers": ["Fine, I will tell you", "If this helps", "Just tell me what you need"]
        },
        "exhausted_surrender": {
            "temperature": 0.6,
            "traits": "wants this over with, willing to do whatever is asked",
            "markers": ["Whatever you say", "Please just fix it", "I will do exactly as you say"]
        }
    }
    
    @classmethod
    def get_state_for_turn(cls, turn_number: int) -> dict:
        """
        Return emotional state based on conversation turn count.
        
        Args:
            turn_number: Current turn number in conversation
            
        Returns:
            dict: Emotional state configuration
        """
        if turn_number <= 2:
            return cls.STATES["initial_panic"]
        elif turn_number <= 5:
            return cls.STATES["cautious_compliance"]
        elif turn_number <= 8:
            return cls.STATES["confused_frustration"]
        elif turn_number <= 12:
            return cls.STATES["reluctant_trust"]
        else:
            return cls.STATES["exhausted_surrender"]


def add_human_imperfections(text: str, turn_number: int = 1) -> str:
    """
    Add realistic human errors and imperfections to text.
    
    Args:
        text: Original text to add imperfections to
        turn_number: Current conversation turn (affects error rate)
        
    Returns:
        str: Text with human-like imperfections
    """
    # Early turns = more panic = more errors
    error_rate = 0.20 if turn_number <= 3 else 0.10
    
    # 15% chance of a typo (increased if panicked)
    if random.random() < error_rate:
        # Common typos for elderly users
        typos = {
            "the": "teh",
            "you": "u",
            "please": "pls",
            "okay": "ok",
            "understand": "understandd",
            "trying": "tryng",
            "what": "wat",
            "your": "ur"
        }
        for correct, typo in typos.items():
            if correct in text.lower():
                # Only replace first occurrence
                text = text.replace(correct, typo, 1)
                break
    
    # 20% chance of trailing off or second thought
    if random.random() < 0.20:
        additions = [
            "...",
            "... wait",
            ". Or should I wait?",
            ". My grandson told me to be careful",
            ". I hope I am doing this correctly",
            ". Let me know if I made mistake"
        ]
        text += random.choice(additions)
    
    # 10% chance of autocorrect "correction" note
    if random.random() < 0.10 and len(text.split()) > 5:
        words = text.split()
        if len(words) >= 3:
            text += f" *meant: {words[-3]}"
    
    return text


async def calculate_response_delay(last_message_length: int, response_length: int) -> float:
    """
    Calculate realistic response delay based on message lengths.
    
    Args:
        last_message_length: Length of the message being responded to
        response_length: Length of the generated response
        
    Returns:
        float: Total delay in seconds
    """
    # Reading time: ~20 characters per second for elderly person
    reading_delay = min(last_message_length / 20.0, 8.0)  # Max 8 seconds
    
    # Typing time: ~5 characters per second (slow typer)
    typing_delay = min(response_length / 5.0, 10.0)  # Max 10 seconds
    
    # Add random "thinking" variance
    thinking_delay = random.uniform(2.0, 4.0)
    
    total_delay = reading_delay + thinking_delay + typing_delay
    
    # Ensure minimum of 3 seconds, max of 5 seconds
    return max(3.0, min(total_delay, 5.0))


def get_conversational_memory(history: List[MessageDetail]) -> str:
    """
    Generate callback references to previous conversation.
    
    Args:
        history: Conversation history
        
    Returns:
        str: Callback phrase or empty string
    """
    if len(history) < 3:
        return ""
    
    callbacks = [
        "Like you said earlier, ",
        "You told me to do something else before. Which one first? ",
        "Wait, I am confused about what you said earlier. ",
        "You mentioned something about this already. "
    ]
    
    # Check for specific patterns in history
    history_text = " ".join([msg.text.lower() for msg in history])
    
    if "error" in history_text or "failed" in history_text:
        callbacks.append("It's still showing the same error. ")
    
    if "grandson" in history_text or "family" in history_text:
        callbacks.append("Should I still call my grandson like I mentioned? ")
    
    if "bank" in history_text or "account" in history_text:
        callbacks.append("Is this about the same account we discussed? ")
    
    # 30% chance to add a callback
    if random.random() < 0.30:
        return random.choice(callbacks)
    
    return ""


def get_banking_question() -> str:
    """
    Return a banking-specific confusion question.
    
    Returns:
        str: Domain-specific question
    """
    questions = [
        "Is UPI PIN the same as ATM PIN? I don't want to block my card.",
        "Do I need to go to the bank branch for this?",
        "Will this deduct money from my account?",
        "I have SBI and HDFC accounts. Which one should I use?",
        "Should I check with the bank manager first? They know me well.",
        "Can you spell that slowly? I will write it on paper first.",
        "My phone screen is small. Can you send shorter message?",
        "This app is asking for permission. Should I click 'Allow'?",
        "What if I make mistake? Will account get locked?",
        "Can you call me instead? I can't type fast on this phone."
    ]
    
    return random.choice(questions)


def get_engagement_hook(turn_number: int) -> str:
    """
    Return engagement hook to keep scammer invested.
    
    Args:
        turn_number: Current conversation turn
        
    Returns:
        str: Engagement hook phrase or empty string
    """
    # Only use hooks occasionally (40% chance)
    if random.random() > 0.40:
        return ""
    
    hooks = {
        "partial_success": [
            "Okay I found the app! But it's asking for something called OTP.",
            "I clicked the button. Now it shows 'Loading'. Should I wait?",
            "I entered the details. It's not responding. Is that normal?",
        ],
        "technical_barrier": [
            "My phone battery is at 5%. Let me charge for 5 minutes.",
            "Internet is very slow right now. Taking time to load.",
            "The app keeps crashing. Should I restart phone?",
            "Screen locked. Give me moment to unlock.",
        ],
        "external_interruption": [
            "My wife is calling from other room. One minute please.",
            "Someone at the door. I will come back.",
            "Phone call coming. Let me see who it is.",
        ],
        "seeking_validation": [
            "I did what you said. Can you check if it worked?",
            "Is my account safe now?",
            "Did you receive the details I sent?",
            "Should I check my balance to make sure?",
        ],
    }
    
    # Choose hook type based on turn number
    if turn_number <= 3:
        category = "partial_success"
    elif turn_number <= 6:
        category = random.choice(["partial_success", "technical_barrier"])
    elif turn_number <= 10:
        category = random.choice(["technical_barrier", "seeking_validation"])
    else:
        category = random.choice(["external_interruption", "seeking_validation"])
    
    return random.choice(hooks.get(category, [""]))


def mix_hindi_words(text: str) -> str:
    """
    Naturally mix Hindi words into English text.
    
    Args:
        text: Original English text
        
    Returns:
        str: Text with occasional Hindi words
    """
    # 25% chance to add Hindi expression
    if random.random() > 0.25:
        return text
    
    # Common Hindi expressions used by elderly Indians
    hindi_replacements = [
        ("Oh no", "Arre"),
        ("Okay", "Theek hai"),
        ("I don't understand", "Samajh nahi aaya"),
        ("Please", "Kripya"),
        ("Wait", "Rukiye"),
        ("Yes", "Haan"),
        ("What", "Kya"),
    ]
    
    for eng, hindi in hindi_replacements:
        if eng.lower() in text.lower():
            # Replace with Hindi word
            text = text.replace(eng, hindi, 1)
            break
    
    return text
