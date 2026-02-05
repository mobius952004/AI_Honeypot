# System Architecture & Concepts Guide

This document explains how your **Agentic Honeypot** works under the hood and defines the key concepts used.

## 1. How the System Works (The "Flow")

Imagine your system as a **digital receptionist** that sits on your computer but can talk to the whole world.

### The Steps:
1.  **The Entry Point (Ngrok)**:
    *   Since your computer is hidden behind a home router, the outside internet (like the Hackathon tester) cannot see it.
    *   **Ngrok** creates a secure "tunnel" from a public URL (`https://...ngrok-free.dev`) directly to your specific computer.
2.  **The Web Server (Uvicorn)**:
    *   On your computer, a program called **Uvicorn** is listening for data on a specific "door" (Port 8000).
    *   When Ngrok receives a message, it forwards it to `localhost:8000`.
3.  **The App (FastAPI)**:
    *   **FastAPI** is the brain. It takes the raw data, checks if it follows the rules (JSON format), and checks your ID (API Key).
4.  **The Logic (Orchestrator)**:
    *   The `orchestrator.py` acts as the manager. It decides: "Is this a new scam? Or are we already talking to them?"
5.  **The Intelligence (GenAI/LLM)**:
    *   If a response is needed, the system sends the conversation history to **Google Gemini** (the LLM).
    *   Gemini pretends to be "Alex" (the persona) and writes a reply.
6.  **The Response**:
    *   The reply travels all the way back: FastAPI -> Uvicorn -> Ngrok -> The Scammer/Tester.

---

## 2. Key Concepts

### ⚡ FastAPI
*   **What it is**: A modern framework for building APIs with Python.
*   **In this project**: It defines the "routes" (like `/api/message`). When someone visits that address, FastAPI runs your specific Python function `handle_message`.

### 🌐 RESTful API (Representational State Transfer)
*   **What it is**: A set of rules for how computers talk to each other over the web.
*   **Key Rule**: Use standard HTTP methods.
    *   **GET**: Ask for data (e.g., loading a webpage).
    *   **POST**: Send data to be processed (e.g., sending the scam message).
*   **In this project**: Your API is "RESTful" because it accepts JSON data via POST requests and returns JSON data.

### 🧠 GenAI (Generative AI)
*   **What it is**: AI that can *create* new content, not just analyze it.
*   **In this project**: We use it for two things:
    1.  **Generation**: Creating unique, human-like replies for "Alex".
    2.  **Extraction**: Reading messy text and pulling out structured data (like UPI IDs).

### 🔑 API Key
*   **What it is**: A secret password that identifies *who* is calling your API.
*   **Why use it?**: To prevent strangers from using up your AI credits or spamming your server.
*   **How it works**: The caller sends a header `x-api-key: secret-123`. Your code checks: `if input_key == my_saved_key: allow() else: block()`.

### 🏠 Localhost
*   **What it is**: A nickname for "This Computer". Technically, it maps to the IP address `127.0.0.1`.
*   **How Python runs it**: Python starts a process that "binds" to a port (8000). This means the operating system sends any network traffic tagged for Port 8000 directly to your Python program.

---

## 3. ChatGPT Learning Prompt

Use this prompt to get a deeper dive into any of these topics:

> "I am a beginner Python developer building an API. I have built a project using **FastAPI**, **Uvicorn**, and **Google Gemini** for an AI agent.
>
> Please act as a senior engineer mentor and explain the following concepts to me in simple terms, using analogies where possible:
>
> 1.  **FastAPI vs. Flask/Django**: Why is FastAPI considered 'modern' and fast?
> 2.  **REST API Structure**: What makes an API 'RESTful' and why do we use JSON?
> 3.  **The Request-Response Cycle**: Explain exactly what happens from the moment a client sends a request to when my Python function returns a result.
> 4.  **Generative AI Integration**: How does an API 'talk' to an LLM like Gemini? What is the difference between an API call and a function call?
>
> Please explain how these pieces fit together to make a working application."
