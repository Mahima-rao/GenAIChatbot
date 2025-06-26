
# 🧠 AI Customer Support Chatbot- ZenBot

This project is a fully functional **agentic chatbot**. It demonstrates capabilities in **tool-augmented reasoning**, **LLM orchestration**, **policy-aware interactions**, and **real-world order management simulation**.

---

## 📌 Initial Problem Statement

> Build a generative AI-powered customer support chatbot.  
> It should:
- Respond to user messages
- Follow company policies (e.g., cancellation after 10 days)
- Call tools like `OrderTracking`, `OrderCancellation`
- Support multiple user sessions
- Evaluate how effectively the chatbot follows reasoning steps
- Include a designed experiment to measure performance

---

## ✅ Solution Overview

This project implements:

### 🧠 Agentic Chatbot Core
- Uses a FastAPI backend
- Orchestrates tools using an agent loop (`agent_core.py`)
- Remembers users and order context (via memory module)

### 🛠️ Tools
- `CancelOrder`, `TrackOrder`, `ReturnOrder`, `PasswordReset`,`RefundOrder`
- Each tool verifies conditions before returning structured results
- Tools include company rule checks (e.g., cancellation policy, tracking policy, user match)

### 📚 Company Policy Retrieval
- Policies are stored and embedded into a **vector database**
- Retrieval is done using sentence similarity
- Matched policy is passed to the LLM for grounded response generation

### 🤖 LLM-Guided Conversational Layer
- Classifies user intent (e.g., cancel, track, return, reset)
- Synthesizes tool results and company policies into natural, helpful language
- Maintains context and conversational memory across user turns
- Grounds responses in retrieved policy content and tool outcomes
- Avoids hallucination by deferring to tools and rules
- Converts structured data into human-friendly explanations

### 🧪 Experimentation & Evaluation
- Extensive evaluation with test cases
- Semantic similarity measured using **CrossEncoder**
- Metrics reported: intent accuracy, tool correctness, response quality
- Visualized with histograms, pie charts, and semantic distribution plots

---

## 🧠 Assumptions Made

- Three users exist: `Shashi`, `Jo`, `Magda`
- Each user has predefined orders in memory
- Orders contain fields: `order_date`, `status`, `user_id`
- Orders placed more than 10 days ago cannot be canceled.
- Refunds are processed only after the product is returned.
- Delivered items are eligible for return within 15 days.
- Pre-orders can be cancelled before shipping.
- Password reset links expire after 24 hours.
- Password reset is assumed to always succeed
- No real-time database or persistence used (in-memory demo)

---

## 🚀 How to Run the App

### 1. Clone the Repository

```bash
git clone https://github.com/Mahima-rao/GenAIChatbot.git
cd chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv aichatbot
.\aichatbot\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Backend

```bash
uvicorn main:app --reload
```
### 5. Running the LLM with Ollama (Mistral)

This chatbot uses the open-source **Mistral** model via [Ollama](https://ollama.com/) to generate responses based on tool outputs and company policies.

Run the model
```bash
ollama run mistral
```

### 6. Launch the Chat UI (Gradio)

Lightweight Gradio UI for quick testing and demo purposes

```bash
python chat_ui.py
```

✅ Access at [http://localhost:7860](http://localhost:7860)

---
### The API endpoint exposed:

- `POST /chat` — Main endpoint for handling chatbot conversations.
  - Input: `{"user_id": ..., "message": ...}`
  - Output: `{"response": "..."}`

Used by:
- Postman
- Evaluation scripts
- Gradio UI frontend

## 📊 Evaluation & Experimentation

The evaluation consists of:
- ✅ End-to-end test cases
- ✅ Tool invocation accuracy
- ✅ Semantic similarity using CrossEncoder
- ✅ Policy matching evaluation
- ✅ Metrics:
  - Intent Accuracy
  - Tool Accuracy
  - Semantic Score ≥ Threshold
  - End-to-End Pass Rate

### 📈 Visualizations
- Histograms for semantic similarity
- Policy match confidence bars
- Pie chart of pass/fail
- Full experiment report in `experiment_analysis.ipynb`

---

## 📁 Project Structure

```
chatbot/
├── main.py                # FastAPI app
├── agent/                 # Agent logic + prompt builder
├── data/                  # In-memory order database used by tools
├── tools/                 # Cancel, Track, Return, Reset
├── memory/                # In-memory user context
├── policy/                # Vector DB + retrieval
├── evaluation/            # Test cases, semantic evaluation
├── chat_ui.py             # Gradio-based UI for demo
├── requirements.txt
├── README.md
```

---

## 📚 Example Policy Rules

- Orders placed more than 10 days ago cannot be canceled.
- Refunds are processed only after the product is returned.
- Delivered items are eligible for return within 15 days.
- Pre-orders can be cancelled before shipping.
- Password reset links expire after 24 hours.

---

## 🌐 Deployment Notes

- The UI is Gradio-based and runs locally
- Backend could be exposed via `ngrok` for full demo

---

## ✨ What Makes This Stand Out

- ✅ Agentic LLM orchestration with real tools
- ✅ Vector DB integration for grounded policy retrieval
- ✅ CrossEncoder evaluation for precision
- ✅ Modular architecture, readable and extendable
- ✅ Clean UI demo via Gradio with user switching
- ✅ Insightful metrics and notebook-style analysis

---

## 🚀 Future Scope & Enhancements
Persistent storage integration
- Move from in-memory mock data to real databases (SQL/NoSQL) for user sessions, orders, and policy management, enabling long-term state and real deployment.

Multi-modal input/output: 
- Extend the chatbot to handle images, voice, and video (e.g., sending a picture of a damaged product for return requests).

Expanded policy management: 
- Implement a policy editor UI for non-technical staff to add or modify company rules dynamically.

Agentic multi-tool orchestration: 
- Develop more complex multi-step workflows where the chatbot chains tools and API calls conditionally based on intermediate results.

User authentication and security: 
- Add user authentication, secure session management, and GDPR-compliant data handling.

Real-time integration: 
- Connect the chatbot to live order management and CRM systems for accurate, up-to-date information.

Self-learning feedback loop: 
- Incorporate user feedback to automatically update policy retrieval rankings and improve response accuracy.

Advanced evaluation: 
- Expand experimentation with A/B testing, user satisfaction metrics, and real customer interactions.

Deployment scaling: 
- Containerize the solution and deploy on cloud platforms with autoscaling, monitoring, and analytics.

---

## 👤 About Author
- AI/ML Engineer with 6+ years of experience
- Specialized in Generative AI, NLP, and Recommendation Systems
- Hands-on experience in AI-driven solutions and large-scale deployment
- Passionate about AI innovations and solving complex problems

