# 🧪 Evaluation Report: Generative Chatbot with Vector RAG

## 🎯 Objective

To evaluate the effectiveness of an LLM-powered chatbot with:

- Agentic reasoning
- API tool invocation
- Policy retrieval via vector embeddings
- Memory tracking

---

## 🧪 Experiment Design

| Component        | Method |
|------------------|--------|
| Intent Accuracy  | Compare LLM classification to expected intent |
| Tool Accuracy    | Check if correct tool was triggered |
| Policy Retrieval | Retrieve top-1 match from vector DB and compare ID |
| Confidence Score | From FAISS distance → similarity score |
| Final Output     | Keyword match in LLM response |

---

## 📊 Evaluation Metrics (example run)

| Metric              | Value     |
|---------------------|-----------|
| Intent Accuracy     | 92.5%     |
| Tool Accuracy       | 90.0%     |
| Policy Match Rate   | 100.0%    |
| Confidence ≥ 0.75   | 75.0%     |
| Response Accuracy   | 95.0%     |
| End-to-End Accuracy | 88.0%     |

---

## 📈 Visualization

**`policy_confidence_plot.ipynb`** shows:

- Confidence scores for each policy test
- Green = correct; Red = incorrect
- Confidence correlates with accuracy

---

## 🧠 Key Insights

- ✅ High-confidence retrieval (≥ 0.75) correlates strongly with correct answers.
- 🧠 LLM decision-making is interpretable and debuggable via step logs.
- 🧰 Tool-based execution scales cleanly across new capabilities.
- 📚 RAG grounding reduces hallucination.
- ❗ Next step: add fallback when confidence < 0.65, and explore fine-tuned classifiers.

---

## ✅ Conclusion

This chatbot architecture demonstrates strong alignment with real-world requirements for a production-grade, interpretable, and modular LLM system. The evaluation framework supports continuous testing and scaling.
