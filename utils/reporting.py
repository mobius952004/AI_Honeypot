import httpx
from core.config import settings
from models.schemas import FinalReport

async def send_report(report: FinalReport):
    """
    Sends the final intelligence report to the GUVI evaluation endpoint.
    """
    url = settings.REPORTING_URL
    headers = {
        "Content-Type": "application/json"
    }
    payload = report.model_dump()
    
    print(f"Sending report to {url}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            print(f"Report sent successfully! Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to send report: {e}")
