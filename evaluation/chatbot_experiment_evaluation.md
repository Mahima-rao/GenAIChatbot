# 🤖 Chatbot Experiment & Evaluation Notebook

This notebook evaluates chatbot performance based on:
- ✅ Intent classification and tool invocation
- ✅ Policy matching accuracy
- ✅ Semantic similarity between expected vs generated responses
- ✅ End-to-end reasoning accuracy

---

## 📥 Load Evaluation Results

```python
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load semantic evaluation results
with open("evaluation/semantic_eval_results.json") as f:
    sem = pd.DataFrame(json.load(f))

# Load policy-level crossencoder evaluation
with open("evaluation/policy_eval_semantic.json") as f:
    pol = pd.DataFrame(json.load(f))
```
---

## 📊 1. Semantic Score Distribution (LLM response accuracy)

```python
plt.figure(figsize=(8, 4))
plt.hist(sem["semantic_score"], bins=10, color="lightblue", edgecolor="black")
plt.axvline(0.50, color="red", linestyle="--", label="Threshold = 0.50")
plt.title("LLM Semantic Score Distribution")
plt.xlabel("Cosine Similarity")
plt.ylabel("Number of Test Cases")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```
---

## ✅ 2. Overall Metrics

```python
metrics = {
    "Intent Accuracy": sem["intent_ok"].mean(),
    "Tool Accuracy": sem["tool_ok"].mean(),
    "Response Accuracy": sem["response_ok"].mean(),
    "Confidence ≥ 0.50": sem["confidence_ok"].mean(),
    "End-to-End Accuracy": sem["passed"].mean()
}

plt.figure(figsize=(8, 4))
plt.bar(metrics.keys(), [v * 100 for v in metrics.values()], color="seagreen")
plt.ylabel("Accuracy (%)")
plt.title("End-to-End Evaluation Metrics")
plt.xticks(rotation=45)
plt.ylim(0, 110)
plt.grid(axis="y")
plt.tight_layout()
plt.show()

metrics
```
---

## 📈 3. Policy Match Confidence (CrossEncoder)

```python
labels = [f"Test {i+1}" for i in range(len(pol))]
colors = ['green' if r else 'red' for r in pol["response_ok"]]

plt.figure(figsize=(10, 4))
plt.bar(labels, pol["crossencoder_score"], color=colors)
plt.axhline(0.50, linestyle='--', color='gray', label="Semantic Threshold (0.50)")
plt.title("Policy Response Semantic Confidence")
plt.xlabel("Test Case")
plt.ylabel("Cosine Similarity")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
```
---

## ❌ 4. Failure Cases Breakdown

```python
failed_cases = sem[~sem["passed"]]
failed_cases[["message", "predicted_intent", "predicted_tool", "semantic_score", "best_matched_phrase"]]
```
---

## 📋 5. Detailed Case Summary

```python
for i, row in sem.iterrows():
    print(f"--- Test {i+1} ---")
    print(f"Message: {row['message']}")
    print(f"Predicted Intent → {row['predicted_intent']}")
    print(f"Tool Used        → {row['predicted_tool']}")
    print(f"Matched Phrase   → {row['best_matched_phrase']}")
    print(f"Semantic Score   → {row['semantic_score']:.2f}")
    print(f"Passed           → {'✅' if row['passed'] else '❌'}\n")
```
---

## 🔍 Summary & Insights

```markdown
**Performance Highlights:**
- ✅ High intent classification and tool routing accuracy
- ✅ Semantic responses were strong in 5/6 user-level tests
- ⚠️ One LLM reply had semantic drift or extra explanation

**Policy-level Evaluation:**
- All 5 policies matched correctly
- One response had semantic mismatch, score < 0.5

**Recommendations:**
- Avoid overly verbose responses during scoring
- Improve matching by fine-tuning or response templating
- Consider fuzzy phrase-level or embedding-based validation
```