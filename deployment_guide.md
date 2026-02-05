# Deployment Guide: Agentic Honeypot API

This guide explains how to deploy your API to the cloud so it's accessible 24/7 without needing your laptop or `ngrok`.

## Option 1: Google Cloud Run (Recommended - Easiest & Cheapest)

Google Cloud Run is perfect for this project because it scales to zero (costs $0 when no one uses it) and handles all the server management for you.

### Prerequisites
1.  A Google Cloud Account.
2.  **Google Cloud CLI** installed on your computer.

### Steps

1.  **Login to Google Cloud**:
    Open your terminal/powershell in `e:\AI_Honeypot` and run:
    ```powershell
    gcloud auth login
    gcloud config set project [YOUR_PROJECT_ID]
    ```

2.  **Deploy using Source Command**:
    This single command builds your container and deploys it.
    ```powershell
    gcloud run deploy agentic-honeypot --source . --region us-central1 --allow-unauthenticated
    ```

3.  **Set Environment Variables**:
    During deployment (or in the dashboard), you MUST set your secrets:
    *   `GEMINI_API_KEY`: [Your Google Gemini Key]
    *   `App_API_KEY`: `secret-key-123` (or your chosen key)
    *   `REPORTING_URL`: `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

4.  **Get your URL**:
    Once finished, it will print a URL like: `https://agentic-honeypot-xyz123-uc.a.run.app`.
    *   **API Endpoint**: `https://agentic-honeypot-.../api/message`
    *   **Health Check**: `https://agentic-honeypot-.../`

---

## Option 2: AWS App Runner (Easiest AWS Method)

If you prefer AWS, App Runner is the equivalent of Cloud Run.

1.  **Push to GitHub**:
    *   Upload your code to a GitHub repository.

2.  **Create App Runner Service**:
    *   Go to AWS Console -> App Runner -> Create Service.
    *   **Source**: Select "Source Code Repository" -> Connect your GitHub.
    *   **Runtime**: Select "Python 3" (or Docker if you prefer).
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`

3.  **Environment Variables**:
    *   Add `GEMINI_API_KEY`, `App_API_KEY`, etc. in the Configuration section.

4.  **Deploy**:
    *   Click "Create & Deploy". You will get a default domain.

---

## Checklist Before Deploying
*   [ ] **Dockerfile**: Created in your project root.
*   [ ] **requirements.txt**: Checked and ready.
*   [ ] **.dockerignore**: Recommended to add (I will create this for you).
*   [ ] **API Keys**: Have them ready to copy-paste into the cloud console.


---

## Option 3: Render (Simplest Direct-from-Repo)

Render is extremely popular because it connects directly to your GitHub repo and updates automatically when you push code.

### Steps

1.  **Push your code to GitHub**:
    *   Initialize git (`git init`), add files, and push to a new public or private repository.

2.  **Create Web Service**:
    *   Go to [dashboard.render.com](https://dashboard.render.com).
    *   Click **New +** -> **Web Service**.
    *   Select "Build and deploy from a Git repository".
    *   Connect your new repository.

3.  **Configure Settings**:
    *   **Runtime**: Select **Python 3**.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *(Render automatically sets the `$PORT` variable)*

4.  **Environment Variables**:
    *   Scroll down to "Environment Variables" and add:
        *   `GEMINI_API_KEY`: [Your Key]
        *   `App_API_KEY`: `secret-key-123`
        *   `REPORTING_URL`: `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`
        *   `PYTHON_VERSION`: `3.10.12` (Optional, ensures compatibility)

5.  **Deploy**:
    *   Click **Create Web Service**.
    *   Render will install dependencies and start your app.
    *   Your URL will be something like: `https://agentic-honeypot.onrender.com`.

### Docker Option on Render (Alternative)
If you prefer using the Dockerfile we created:
1.  Select **Docker** instead of Python 3 runtime.
2.  Render will automatically find the `Dockerfile` and build it.
3.  You still need to set the Environment Variables.

