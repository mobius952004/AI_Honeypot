# Agentic Honey-Pot API 🍯🤖

An AI-powered cybersecurity honeypot designed to detect, engage, and analyze online scammers. This system acts as a vulnerable simulated victim ("Alex"), autonomously engaging scammers in multi-turn conversations to extract actionable intelligence (UPI IDs, bank accounts, phone numbers) to report to authorities.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

## 🌟 Key Features

*   **🛡️ Active Scam Detection**: Uses LLM analysis to identify urgency, financial threats, and phishing patterns in incoming messages.
*   **🎭 Autonomous Persona**: "Alex" - a wealthy but tech-illiterate character who keeps scammers talking by asking "stupid" questions.
*   **🧠 Intelligent Extraction**: Automatically parses conversation history for UPI IDs, Phone Numbers, and Phishing Links.
*   **⚡ Resilient Architecture**: Includes a **Hybrid Extraction Engine** that uses LLMs (Primary) and Regex Fallbacks (Backup) to ensure reporting works even if API quotas are exceeded.
*   **📡 Secure Reporting**: Automatically callbacks to the GUVI evaluation platform with structured intelligence.

## 🛠️ Tech Stack

*   **Core**: Python 3.10+, FastAPI, Uvicorn
*   **AI/LLM**: Google Gemini API (`gemini-2.0-flash`, `gemini-flash-latest`)
*   **Tunneling**: `pyngrok` for public internet exposure
*   **Validation**: Pydantic

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher
*   A Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/))

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/mobius952004/AI_Honeypot.git
    cd AI_Honeypot
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```properties
    # Your Secret Key for Incoming Requests
    App_API_KEY=my-secret-key-123

    # Your Google Gemini API Key
    GEMINI_API_KEY=AIzaSy...

    # Reporting Endpoint (Default provided)
    REPORTING_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
    ```

## 🏃‍♂️ Usage

### 1. Run Locally (Public Access)
To expose the API to the internet (required for external testing/hackathons):

```bash
python expose_api.py
```
*   This will start the server and print a public URL like `https://abc-123.ngrok-free.app`.
*   Your API Endpoint is: `https://abc-123.ngrok-free.app/api/message`

### 2. Run Locally (Private)
If you just want to test on localhost:
```bash
.\run.bat
```

## 🧪 Testing

We have included a full flow simulation script that mocks a scammer trying to steal money.

```bash
python test_full_flow.py
```
**What this does:**
1.  Sends a "Block Warning" message (Simulating a scammer).
2.  Agent replies ("Oh no, help me!").
3.  Scammer asks for UPI ID.
4.  Agent asks for clarification.
5.  Scammer provides a UPI ID (`scammer@okicic`).
6.  **System detects the ID and sends a report to the server.**

## 📂 Project Structure

```
AI_Honeypot/
├── core/               # Configuration & Security
├── models/             # Pydantic Schemas (Input/Output)
├── services/
│   ├── llm_engine.py   # Gemini Integration & Logic
│   └── orchestrator.py # Conversation Flow Manager
├── utils/              # Reporting Utilities
├── main.py             # FastAPI Application
├── expose_api.py       # Ngrok Deployment Script
├── test_full_flow.py   # E2E Testing Script
└── PROJECT_REPORT.md   # Detailed Technical Documentation
```

## 📝 License
This project is created for the Agentic Honey-Pot Hackathon.
