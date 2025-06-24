# import json
# import requests
# from chatbot.policy.vector_search import get_relevant_policies

# with open("evaluation/test_policy_cases.json") as f:
#     tests = json.load(f)

# correct_response = 0
# log = []

# for i, test in enumerate(tests):
#     user_id = test["user_id"]
#     msg = test["message"]
#     expected_phrases = test["expected_phrases"]

#     res = requests.post("http://localhost:8000/chat", json={
#         "user_id": user_id,
#         "message": msg
#     })
#     reply = res.json()["response"]

#     retrieved = get_relevant_policies(msg, top_k=1)
#     top_policy = retrieved[0]["id"]
#     similarity = retrieved[0]["similarity"]

#     matched = any(phrase.lower() in reply.lower() for phrase in expected_phrases)

#     log.append({
#         "user_id": user_id,
#         "message": msg,
#         "retrieved_policy_id": top_policy,
#         "similarity": similarity,
#         "expected_phrases": expected_phrases,
#         "response": reply,
#         "response_ok": matched
#     })

#     if matched:
#         correct_response += 1

# with open("evaluation/policy_eval_results.json", "w") as f:
#     json.dump(log, f, indent=2)

# print(f"✅ Policy-Based Conversational Accuracy: {correct_response}/{len(tests)}")
import json
import requests
from chatbot.policy.vector_search import get_relevant_policies
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def is_semantic_match(predicted, expected_phrases, threshold=0.85):
    pred_emb = model.encode(predicted, convert_to_tensor=True)
    max_score = 0.0
    for phrase in expected_phrases:
        phrase_emb = model.encode(phrase, convert_to_tensor=True)
        score = util.cos_sim(pred_emb, phrase_emb).item()
        max_score = max(max_score, score)
    return max_score >= threshold, max_score

with open("evaluation/test_policy_cases.json") as f:
    tests = json.load(f)

correct = 0
log = []

for test in tests:
    user_id = test["user_id"]
    msg = test["message"]
    expected_phrases = test["expected_phrases"]

    res = requests.post("http://localhost:8000/chat", json={"user_id": user_id, "message": msg})
    reply = res.json()["response"]

    retrieved = get_relevant_policies(msg, top_k=1)
    top_policy = retrieved[0]["id"]
    similarity = retrieved[0]["similarity"]

    matched, score = is_semantic_match(reply, expected_phrases)

    log.append({
        "user_id": user_id,
        "message": msg,
        "expected_phrases": expected_phrases,
        "retrieved_policy_id": top_policy,
        "retrieval_similarity": similarity,
        "response": reply,
        "semantic_score": round(score, 3),
        "response_ok": matched
    })

    if matched:
        correct += 1

with open("evaluation/policy_eval_semantic.json", "w") as f:
    json.dump(log, f, indent=2)

print(f"✅ Semantic Policy-Based Accuracy: {correct}/{len(tests)}")
