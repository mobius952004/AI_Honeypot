from typing import List, Optional, Any
from pydantic import BaseModel

class MessageDetail(BaseModel):
    sender: str  # "scammer" or "user"
    text: str
    timestamp: int

class MessageMetadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

class MessageInput(BaseModel):
    sessionId: str
    message: MessageDetail
    conversationHistory: Optional[List[MessageDetail]] = None
    metadata: Optional[MessageMetadata] = None

class AgentResponse(BaseModel):
    status: str
    reply: str

class IntelligenceData(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class FinalReport(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: IntelligenceData
    agentNotes: str
