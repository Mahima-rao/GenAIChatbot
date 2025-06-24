# # # # import json
# # # # import requests

# # # # with open("evaluation/test_cases.json") as f:
# # # #     tests = json.load(f)

# # # # correct = 0

# # # # for i, test in enumerate(tests):
# # # #     res = requests.post("http://localhost:8000/chat", json={
# # # #         "user_id": test["user_id"],
# # # #         "message": test["message"]
# # # #     })
# # # #     reply = res.json()["response"]
# # # #     print(f"[Test {i+1}] User: {test['user_id']}")
# # # #     print(f"> {test['message']}")
# # # #     print(f"Bot: {reply}")
# # # #     if test["expected_keyword"].lower() in reply.lower():
# # # #         correct += 1
# # # #     print("---")

# # # # print(f"✅ End-to-End Accuracy: {correct}/{len(tests)}")
# # # import json
# # # import requests

# # # with open("evaluation/test_cases.json") as f:
# # #     tests = json.load(f)

# # # correct = 0
# # # logs = []

# # # for i, test in enumerate(tests):
# # #     user_id = test["user_id"]
# # #     msg = test["message"]
# # #     expected = test["expected_keyword"].lower()

# # #     res = requests.post("http://localhost:8000/chat", json={
# # #         "user_id": user_id,
# # #         "message": msg
# # #     })

# # #     reply = res.json().get("response", "")
# # #     passed = expected in reply.lower()
# # #     if passed:
# # #         correct += 1

# # #     logs.append({
# # #         "user_id": user_id,
# # #         "input": msg,
# # #         "response": reply,
# # #         "expected_keyword": expected,
# # #         "passed": passed
# # #     })

# # #     print(f"[Test {i+1}] {user_id} ➜ {msg}")
# # #     print(f"✓ Passed" if passed else f"✗ Failed")
# # #     print(f"Bot: {reply}\n---")

# # # print(f"\n✅ Accuracy: {correct}/{len(tests)}")
# # import json
# # import requests

# # with open("evaluation/test_cases.json") as f:
# #     tests = json.load(f)

# # passed = 0

# # for i, test in enumerate(tests):
# #     res = requests.post("http://localhost:8000/chat", json={
# #         "user_id": test["user_id"],
# #         "message": test["message"]
# #     })
# #     response = res.json()["response"]
# #     expected_phrases = test["expected_phrases"]

# #     match = any(phrase.lower() in response.lower() for phrase in expected_phrases)

# #     print(f"[Test {i+1}] {test['message']}")
# #     print(f"Bot: {response}")
# #     print("✓ Passed" if match else "✗ Failed")
# #     print("---")

# #     if match:
# #         passed += 1

# # print(f"\n✅ Conversational Accuracy: {passed}/{len(tests)}")
# import json
# import requests
# from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def is_semantic_match(predicted, expected_phrases, threshold=0.55):
#     pred_emb = model.encode(predicted, convert_to_tensor=True)

#     max_score = 0.0
#     for phrase in expected_phrases:
#         target_emb = model.encode(phrase, convert_to_tensor=True)
#         score = util.cos_sim(pred_emb, target_emb).item()
#         max_score = max(max_score, score)
#     return max_score >= threshold, max_score

# with open("evaluation/test_cases.json") as f:
#     tests = json.load(f)

# log = []
# passed = 0

# for i, test in enumerate(tests):
#     user_id = test["user_id"]
#     message = test["message"]
#     expected_phrases = test["expected_phrases"]

#     res = requests.post("http://localhost:8000/chat", json={
#         "user_id": user_id,
#         "message": message
#     })

#     reply = res.json().get("response", "")
#     matched, score = is_semantic_match(reply, expected_phrases)

#     print(f"[Test {i+1}] {message}")
#     print(f"Bot: {reply}")
#     print(f"✓ Passed (Score: {score:.2f})" if matched else f"✗ Failed (Score: {score:.2f})")
#     print("---")

#     if matched:
#         passed += 1

#     log.append({
#         "user_id": user_id,
#         "message": message,
#         "expected_phrases": expected_phrases,
#         "response": reply,
#         "semantic_score": round(score, 3),
#         "passed": matched
#     })

# with open("evaluation/semantic_eval_results.json", "w") as f:
#     json.dump(log, f, indent=2)

# print(f"\n✅ Semantic Accuracy: {passed}/{len(tests)}")
import json
import requests
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")
THRESHOLD = 0.55  # Semantic similarity cutoff

def summarize_for_eval(text: str):
    """Pick the most relevant sentence from LLM reply."""
    lines = text.split(".")
    for line in lines:
        if any(kw in line.lower() for kw in ["order", "cancel", "ship", "return", "refund", "password"]):
            return line.strip()
    return lines[0].strip()

def sentence_level_score(reply: str, expected_phrases):
    """Return highest score from any sentence to any expected phrase."""
    best_score = 0.0
    best_sent = ""
    sentences = [s.strip() for s in reply.split(".") if s.strip()]
    for sent in sentences:
        for phrase in expected_phrases:
            score = util.cos_sim(
                model.encode(sent, convert_to_tensor=True),
                model.encode(phrase, convert_to_tensor=True)
            ).item()
            if score > best_score:
                best_score = score
                best_sent = sent
    return best_score, best_sent

with open("evaluation/test_cases.json") as f:
    tests = json.load(f)

passed = 0
log = []

for i, test in enumerate(tests):
    user_id = test["user_id"]
    message = test["message"]
    expected_phrases = test["expected_phrases"]

    res = requests.post("http://localhost:8000/chat", json={
        "user_id": user_id,
        "message": message
    })

    reply = res.json().get("response", "")
    score, matched_sentence = sentence_level_score(reply, expected_phrases)
    passed_case = score >= THRESHOLD

    if passed_case:
        passed += 1

    print(f"[Test {i+1}] {message}")
    print(f"Bot: {reply}")
    print(f"✓ Passed (Score: {score:.2f})" if passed_case else f"✗ Failed (Score: {score:.2f})")
    print(f"Best Match: \"{matched_sentence}\"\n---")

    log.append({
        "user_id": user_id,
        "message": message,
        "expected_phrases": expected_phrases,
        "response": reply,
        "matched_sentence": matched_sentence,
        "semantic_score": round(score, 3),
        "passed": passed_case
    })

with open("evaluation/semantic_eval_results.json", "w") as f:
    json.dump(log, f, indent=2)

print(f"\n✅ Semantic Accuracy: {passed}/{len(tests)}")
