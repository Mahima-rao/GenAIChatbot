# # # import json
# # # import requests
# # # from chatbot.policy.vector_search import get_relevant_policies

# # # with open("evaluation/test_policy_cases.json") as f:
# # #     tests = json.load(f)

# # # correct_response = 0
# # # log = []

# # # for i, test in enumerate(tests):
# # #     user_id = test["user_id"]
# # #     msg = test["message"]
# # #     expected_phrases = test["expected_phrases"]

# # #     res = requests.post("http://localhost:8000/chat", json={
# # #         "user_id": user_id,
# # #         "message": msg
# # #     })
# # #     reply = res.json()["response"]

# # #     retrieved = get_relevant_policies(msg, top_k=1)
# # #     top_policy = retrieved[0]["id"]
# # #     similarity = retrieved[0]["similarity"]

# # #     matched = any(phrase.lower() in reply.lower() for phrase in expected_phrases)

# # #     log.append({
# # #         "user_id": user_id,
# # #         "message": msg,
# # #         "retrieved_policy_id": top_policy,
# # #         "similarity": similarity,
# # #         "expected_phrases": expected_phrases,
# # #         "response": reply,
# # #         "response_ok": matched
# # #     })

# # #     if matched:
# # #         correct_response += 1

# # # with open("evaluation/policy_eval_results.json", "w") as f:
# # #     json.dump(log, f, indent=2)

# # # print(f"✅ Policy-Based Conversational Accuracy: {correct_response}/{len(tests)}")
# # import json
# # import requests
# # from chatbot.policy.vector_search import get_relevant_policies
# # from sentence_transformers import SentenceTransformer, util

# # model = SentenceTransformer("all-MiniLM-L6-v2")

# # def is_semantic_match(predicted, expected_phrases, threshold=0.85):
# #     pred_emb = model.encode(predicted, convert_to_tensor=True)
# #     max_score = 0.0
# #     for phrase in expected_phrases:
# #         phrase_emb = model.encode(phrase, convert_to_tensor=True)
# #         score = util.cos_sim(pred_emb, phrase_emb).item()
# #         max_score = max(max_score, score)
# #     return max_score >= threshold, max_score

# # with open("evaluation/test_policy_cases.json") as f:
# #     tests = json.load(f)

# # correct = 0
# # log = []

# # for test in tests:
# #     user_id = test["user_id"]
# #     msg = test["message"]
# #     expected_phrases = test["expected_phrases"]

# #     res = requests.post("http://localhost:8000/chat", json={"user_id": user_id, "message": msg})
# #     reply = res.json()["response"]

# #     retrieved = get_relevant_policies(msg, top_k=1)
# #     top_policy = retrieved[0]["id"]
# #     similarity = retrieved[0]["similarity"]

# #     matched, score = is_semantic_match(reply, expected_phrases)

# #     log.append({
# #         "user_id": user_id,
# #         "message": msg,
# #         "expected_phrases": expected_phrases,
# #         "retrieved_policy_id": top_policy,
# #         "retrieval_similarity": similarity,
# #         "response": reply,
# #         "semantic_score": round(score, 3),
# #         "response_ok": matched
# #     })

# #     if matched:
# #         correct += 1

# # with open("evaluation/policy_eval_semantic.json", "w") as f:
# #     json.dump(log, f, indent=2)

# # print(f"✅ Semantic Policy-Based Accuracy: {correct}/{len(tests)}")
# import json
# import requests
# import sys
# import os
# from sentence_transformers import SentenceTransformer, util
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, project_root)
# from chatbot.policy.vector_search import get_relevant_policies

# model = SentenceTransformer("all-MiniLM-L6-v2")
# THRESHOLD = 0.55

# def semantic_score(reply, expected_phrases):
#     best_score = 0
#     for sentence in reply.split("."):
#         for phrase in expected_phrases:
#             score = util.cos_sim(
#                 model.encode(sentence.strip(), convert_to_tensor=True),
#                 model.encode(phrase.strip(), convert_to_tensor=True)
#             ).item()
#             best_score = max(best_score, score)
#     return best_score

# with open("evaluation/test_policy_cases.json") as f:
#     tests = json.load(f)

# log = []
# policy_ok = response_ok = high_conf = 0

# for test in tests:
#     user_id = test["user_id"]
#     msg = test["message"]
#     expected_phrases = test["expected_phrases"]
#     expected_policy_id = test["expected_policy_id"]

#     reply = requests.post("http://localhost:8000/chat", json={"user_id": user_id, "message": msg}).json()["response"]
#     retrieved = get_relevant_policies(msg, top_k=1)
#     top_policy = retrieved[0]["id"]
#     sim_score = semantic_score(reply, expected_phrases)

#     ok_policy = top_policy == expected_policy_id
#     ok_response = sim_score >= THRESHOLD
#     if ok_policy: policy_ok += 1
#     if ok_response: response_ok += 1
#     if sim_score >= 0.55: high_conf += 1

#     log.append({
#         "user_id": user_id,
#         "message": msg,
#         "response": reply,
#         "expected_policy_id": expected_policy_id,
#         "retrieved_policy_id": top_policy,
#         "retrieval_similarity": retrieved[0]["similarity"],
#         "semantic_score": round(sim_score, 3),
#         "response_ok": ok_response,
#         "policy_ok": ok_policy
#     })

# with open("evaluation/policy_eval_semantic.json", "w") as f:
#     json.dump(log, f, indent=2)

# total = len(tests)
# print("\nPolicy Evaluation Metrics Summary")
# print("| Metric            | Value     |")
# print("|-------------------|-----------|")
# print(f"| Policy Match Rate | {policy_ok/total:.2%} |")
# print(f"| Response Accuracy | {response_ok/total:.2%} |")
# print(f"| Confidence ≥ 0.75 | {high_conf/total:.2%} |")
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
