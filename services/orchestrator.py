from fastapi import BackgroundTasks
from models.schemas import MessageInput, AgentResponse, MessageDetail, FinalReport
from services.llm_engine import llm_engine
from utils.reporting import send_report

async def analyze_and_report_task(session_id: str, history: list[MessageDetail]):
    """
    Background task to analyze conversation and potentially send a report.
    """
    # Extract intelligence
    intelligence = await llm_engine.extract_intelligence(history)
    
    # Check if we should end/report
    if llm_engine.check_completion(history, intelligence):
        report = FinalReport(
            sessionId=session_id,
            scamDetected=True,
            totalMessagesExchanged=len(history),
            extractedIntelligence=intelligence,
            agentNotes="Scammer engaged. Intelligence extracted. Stopping now."
        )
        await send_report(report)

async def process_message(data: MessageInput, background_tasks: BackgroundTasks) -> AgentResponse:
    # 1. Reconstruct full history (previous + current)
    # The current message is in data.message. Add it to history list for processing.
    # Note: data.conversationHistory is strictly PREVIOUS messages.
    previous_history = data.conversationHistory or []
    full_history = previous_history + [data.message]
    
    # 2. Determine State
    # Heuristic: If we have responded before (sender='user' in history), we are engaged.
    # Otherwise, check for scam.
    has_prior_engagement = any(msg.sender == 'user' for msg in previous_history)
    
    is_scam = False
    
    if has_prior_engagement:
        # We assume we are already in a scam conversation
        is_scam = True
    else:
        # Detect
        is_scam = await llm_engine.detect_scam(data.message.text, data.conversationHistory)

    # 3. Action
    reply_text = ""
    status = "success"
    
    if is_scam:
        # Generate Agent Reply
        reply_text = await llm_engine.generate_reply(full_history)
        
        # Add our reply to the history for analysis (this is "future" history effectively)
        # We need to model our own reply as a MessageDetail for the analyzer
        import time
        my_reply_msg = MessageDetail(
            sender="user", 
            text=reply_text, 
            timestamp=int(time.time() * 1000)
        )
        history_for_analysis = full_history + [my_reply_msg]
        
        # Schedule Background Analysis
        background_tasks.add_task(analyze_and_report_task, data.sessionId, history_for_analysis)
        
    else:
        # If not scam, what to do? The prompt implies we only activate agent if detected.
        # But we must return a JSON.
        # We can return a neutral message or empty.
        # Let's return a safe neutral message.
        reply_text = "Message received."
        status = "ignored" # Or keep success? Spec says "Active an autonomous AI Agent" if scam.
        # Let's keep status success but a boring reply so we don't engage.

    return AgentResponse(status=status, reply=reply_text)
