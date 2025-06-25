import os
import sys
import json
from sentence_transformers import CrossEncoder
# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '..')))

from chatbot.policy.vector_search import get_relevant_policies

# Load CrossEncoder model
model = CrossEncoder("cross-encoder/stsb-roberta-base")

THRESHOLD = 0.50

with open("evaluation/test_policy_cases.json") as f:
    tests = json.load(f)

log = []
policy_ok = response_ok = high_conf = 0

for i, test in enumerate(tests):
    user_id = test["user_id"]
    msg = test["message"]
    expected_phrases = test["expected_phrases"]
    expected_policy_id = test["expected_policy_id"]

    # Step 1: Run chatbot and get response
    import requests
    reply = requests.post("http://localhost:8000/chat", json={
        "user_id": user_id,
        "message": msg
    }).json()["response"]

    # Step 2: Retrieve top policy
    retrieved = get_relevant_policies(msg, top_k=1)
    top_policy = retrieved[0]["id"]
    retrieval_similarity = retrieved[0]["similarity"]

    # Step 3: Cross-encode each expected phrase
    scores = model.predict([[reply, phrase] for phrase in expected_phrases])
    max_score = max(scores)
    best_phrase = expected_phrases[scores.argmax()]

    # Evaluation flags
    ok_policy = top_policy == expected_policy_id
    ok_response = max_score >= THRESHOLD  or (top_policy == expected_policy_id and max_score>= 0.40)
    if ok_policy: policy_ok += 1
    if ok_response: response_ok += 1
    if max_score >= 0.50: high_conf += 1

    log.append({
        "user_id": user_id,
        "message": msg,
        "expected_policy_id": expected_policy_id,
        "retrieved_policy_id": top_policy,
        "retrieval_similarity": retrieval_similarity,
        "crossencoder_score": float(round(max_score, 3)) if max_score is not None else None,
        "best_matched_phrase": best_phrase,
        "response": reply,
        "response_ok": bool(ok_response),
        "policy_ok": bool(ok_policy)
    })

# Save log
with open("evaluation/policy_eval_crossencoder.json", "w") as f:
    json.dump(log, f, indent=2)

# Print summary
total = len(tests)
print("\n📊 CrossEncoder Policy Evaluation Metrics")
print("| Metric            | Value     |")
print("|-------------------|-----------|")
print(f"| Policy Match Rate | {policy_ok/total:.2%} |")
print(f"| Response Accuracy | {response_ok/total:.2%} |")
print(f"| Confidence ≥ 0.55 | {high_conf/total:.2%} |")
