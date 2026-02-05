from fastapi import FastAPI, Depends, BackgroundTasks
from core.security import get_api_key
from models.schemas import MessageInput, AgentResponse
from services.orchestrator import process_message

app = FastAPI(title="Agentic Honey-Pot API", version="1.0")

from fastapi import Request
import json

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print(f"\n[INCOMING BODY]: {body.decode()}\n", flush=True)
    # Reset body stream for next dependency
    async def get_body():
        return body
    request._receive = get_body
    response = await call_next(request)
    
    # Capture response body
    resp_body = [section async for section in response.body_iterator]
    
    # Print the body for debugging
    print(f"\n[OUTGOING RESPONSE]: {b''.join(resp_body).decode()}\n", flush=True)
    
    # Re-create the async iterator
    async def async_generator():
        for chunk in resp_body:
            yield chunk
            
    response.body_iterator = async_generator()
    
    response.body_iterator = async_generator()
    
    return response

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()
    print(f"\n[VALIDATION ERROR]: {error_details}\n")
    return JSONResponse(
        status_code=422,
        content={"detail": error_details, "body": str(exc.body)},
    )

@app.post("/api/message", response_model=AgentResponse)
async def handle_message(
    data: MessageInput, 
    background_tasks: BackgroundTasks, 
    api_key: str = Depends(get_api_key)
):
    """
    Endpoint to receive messages, detect scams, and return agent responses.
    """
    return await process_message(data, background_tasks)

@app.get("/")
def health_check():
    return {"status": "running", "service": "Agentic Honey-Pot"}

# Reload trigger
