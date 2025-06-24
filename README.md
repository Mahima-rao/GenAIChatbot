# 🤖 Generative Agentic Chatbot (ML Scientist Challenge)

This is a fully agentic, policy-grounded chatbot that:

- 🧠 Uses a local LLM (Mistral via Ollama)
- 📚 Retrieves company policies via vector search (FAISS + MiniLM)
- 🔧 Uses tool-based actions (cancel, track, refund, reset, etc.)
- 🧾 Maintains user context (order IDs, chat history)
- 📊 Evaluated with metrics, logs, and visualizations

## 🚀 Features

| Capability              | Implemented |
|-------------------------|-------------|
| LLM integration (Mistral)   | ✅ |
| Policy RAG (FAISS + ST)     | ✅ |
| Tool abstraction            | ✅ |
| Order validation            | ✅ |
| Persistent memory           | ✅ |
| Confidence scores           | ✅ |
| Evaluation metrics          | ✅ |
| Visualization (matplotlib) | ✅ |

---

## ⚙️ Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run local LLM
ollama run mistral

# Start FastAPI app
uvicorn main:app --reload

# Send a request:
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"user_id": "user1", "message": "Cancel order ORD001"}'
```
## 🧪 Evaluation

```bash
#✅ General Tests
python evaluation/evaluate.py

#✅ Policy Retrieval Tests
python evaluation/eval_policy.py

#✅ Visualize Policy Confidence
Open:
evaluation/policy_confidence_plot.ipynb

```

## 📈 Metrics

| Metric              | Value (example) |
| ------------------- | --------------- |
| Intent Accuracy     | 92.5%           |
| Tool Accuracy       | 90.0%           |
| Policy Match Rate   | 100.0%          |
| Response Accuracy   | 95.0%           |
| End-to-End Accuracy | 88.0%           |


## 📂 Structure

├── agent/            → agent loop, LLM interface
├── tools/            → cancel, track, return, refund, reset
├── api/              → mock order DB
├── memory/           → per-user session memory
├── chatbot/policy/   → policy store + vector DB (FAISS)
├── evaluation/       → test cases, eval scripts, plots
├── main.py           → FastAPI entry


## Notes
This chatbot is fully modular, interpretable, and extensible — ready for production and research.

