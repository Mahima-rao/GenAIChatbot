import json
import requests
import os
import sys
from sentence_transformers import CrossEncoder

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '..')))

from agent.agent_core import classify_intent

# Load CrossEncoder model
model = CrossEncoder("cross-encoder/stsb-roberta-base")
THRESHOLD = 0.50  # semantic similarity threshold

# Load test cases
with open("evaluation/test_cases.json") as f:
    tests = json.load(f)

results = []
intent_matches = tool_matches = response_passes = high_confidence = e2e_passes = 0

for i, test in enumerate(tests):
    user_id = test["user_id"]
    msg = test["message"]
    expected_intent = test.get("expected_intent")
    expected_tool = test.get("expected_tool")
    expected_policy_id = test.get("expected_policy_id")
    expected_phrases = test.get("expected_phrases", [])

    # Step 1: LLM-based intent prediction (as used in the agent loop)
    predicted_intent = classify_intent(msg)  # Used for reference comparison only
    predicted_tool = predicted_intent.capitalize() + "Order" if predicted_intent != "reset" else "PasswordReset"
    print(f"\n[Test {i+1}] {msg}")
    print(f"→ Expecting intent: {expected_intent}, tool: {expected_tool}")

    # Step 2: Chatbot response
    res = requests.post("http://localhost:8000/chat", json={
        "user_id": user_id,
        "message": msg
    })
    reply = res.json().get("response", "")

    # Step 3: CrossEncoder semantic scoring
    pairs = [[reply, phrase] for phrase in expected_phrases]
    scores = model.predict(pairs)  # numpy array or list

    if len(scores) > 0:
        max_score = max(scores)
        best_match = expected_phrases[scores.argmax()]
    else:
        max_score = None
        best_match = None

    # Step 4: Metric flags
    intent_ok = predicted_intent == expected_intent
    tool_ok = predicted_tool == expected_tool
    response_ok = max_score >= THRESHOLD
    confidence_ok = max_score >= 0.50
    passed = intent_ok and tool_ok and response_ok

    # Count passes
    if intent_ok: intent_matches += 1
    if tool_ok: tool_matches += 1
    if response_ok: response_passes += 1
    if confidence_ok: high_confidence += 1
    if passed: e2e_passes += 1

    # Log result
    results.append({
        "user_id": user_id,
        "message": msg,
        "expected_intent": expected_intent,
        "predicted_intent": predicted_intent,
        "expected_tool": expected_tool,
        "predicted_tool": predicted_tool,
        "expected_phrases": expected_phrases,
        "best_matched_phrase": best_match,
        "semantic_score": float(round(max_score, 3)) if max_score is not None else None,
        "response": reply,
        "intent_ok": bool(intent_ok),
        "tool_ok": bool(tool_ok),
        "response_ok": bool(response_ok),
        "confidence_ok": bool(confidence_ok),
        "passed": bool(passed)
    })

# Save results
with open("evaluation/semantic_eval_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Print metric summary
total = len(tests)
print("\n📊 Evaluation Metrics Summary")
print("| Metric              | Value     |")
print("|---------------------|-----------|")
print(f"| Intent Accuracy     | {intent_matches / total:.2%} |")
print(f"| Tool Accuracy       | {tool_matches / total:.2%} |")
print(f"| Response Accuracy   | {response_passes / total:.2%} |")
print(f"| Confidence ≥ 0.75   | {high_confidence / total:.2%} |")
print(f"| End-to-End Accuracy | {e2e_passes / total:.2%} |")
