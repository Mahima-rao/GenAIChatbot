# # # # # # import json
# # # # # # import requests

# # # # # # with open("evaluation/test_cases.json") as f:
# # # # # #     tests = json.load(f)

# # # # # # correct = 0

# # # # # # for i, test in enumerate(tests):
# # # # # #     res = requests.post("http://localhost:8000/chat", json={
# # # # # #         "user_id": test["user_id"],
# # # # # #         "message": test["message"]
# # # # # #     })
# # # # # #     reply = res.json()["response"]
# # # # # #     print(f"[Test {i+1}] User: {test['user_id']}")
# # # # # #     print(f"> {test['message']}")
# # # # # #     print(f"Bot: {reply}")
# # # # # #     if test["expected_keyword"].lower() in reply.lower():
# # # # # #         correct += 1
# # # # # #     print("---")

# # # # # # print(f"✅ End-to-End Accuracy: {correct}/{len(tests)}")
# # # # # import json
# # # # # import requests

# # # # # with open("evaluation/test_cases.json") as f:
# # # # #     tests = json.load(f)

# # # # # correct = 0
# # # # # logs = []

# # # # # for i, test in enumerate(tests):
# # # # #     user_id = test["user_id"]
# # # # #     msg = test["message"]
# # # # #     expected = test["expected_keyword"].lower()

# # # # #     res = requests.post("http://localhost:8000/chat", json={
# # # # #         "user_id": user_id,
# # # # #         "message": msg
# # # # #     })

# # # # #     reply = res.json().get("response", "")
# # # # #     passed = expected in reply.lower()
# # # # #     if passed:
# # # # #         correct += 1

# # # # #     logs.append({
# # # # #         "user_id": user_id,
# # # # #         "input": msg,
# # # # #         "response": reply,
# # # # #         "expected_keyword": expected,
# # # # #         "passed": passed
# # # # #     })

# # # # #     print(f"[Test {i+1}] {user_id} ➜ {msg}")
# # # # #     print(f"✓ Passed" if passed else f"✗ Failed")
# # # # #     print(f"Bot: {reply}\n---")

# # # # # print(f"\n✅ Accuracy: {correct}/{len(tests)}")
# # # # import json
# # # # import requests

# # # # with open("evaluation/test_cases.json") as f:
# # # #     tests = json.load(f)

# # # # passed = 0

# # # # for i, test in enumerate(tests):
# # # #     res = requests.post("http://localhost:8000/chat", json={
# # # #         "user_id": test["user_id"],
# # # #         "message": test["message"]
# # # #     })
# # # #     response = res.json()["response"]
# # # #     expected_phrases = test["expected_phrases"]

# # # #     match = any(phrase.lower() in response.lower() for phrase in expected_phrases)

# # # #     print(f"[Test {i+1}] {test['message']}")
# # # #     print(f"Bot: {response}")
# # # #     print("✓ Passed" if match else "✗ Failed")
# # # #     print("---")

# # # #     if match:
# # # #         passed += 1

# # # # print(f"\n✅ Conversational Accuracy: {passed}/{len(tests)}")
# # # import json
# # # import requests
# # # from sentence_transformers import SentenceTransformer, util

# # # model = SentenceTransformer("all-MiniLM-L6-v2")

# # # def is_semantic_match(predicted, expected_phrases, threshold=0.55):
# # #     pred_emb = model.encode(predicted, convert_to_tensor=True)

# # #     max_score = 0.0
# # #     for phrase in expected_phrases:
# # #         target_emb = model.encode(phrase, convert_to_tensor=True)
# # #         score = util.cos_sim(pred_emb, target_emb).item()
# # #         max_score = max(max_score, score)
# # #     return max_score >= threshold, max_score

# # # with open("evaluation/test_cases.json") as f:
# # #     tests = json.load(f)

# # # log = []
# # # passed = 0

# # # for i, test in enumerate(tests):
# # #     user_id = test["user_id"]
# # #     message = test["message"]
# # #     expected_phrases = test["expected_phrases"]

# # #     res = requests.post("http://localhost:8000/chat", json={
# # #         "user_id": user_id,
# # #         "message": message
# # #     })

# # #     reply = res.json().get("response", "")
# # #     matched, score = is_semantic_match(reply, expected_phrases)

# # #     print(f"[Test {i+1}] {message}")
# # #     print(f"Bot: {reply}")
# # #     print(f"✓ Passed (Score: {score:.2f})" if matched else f"✗ Failed (Score: {score:.2f})")
# # #     print("---")

# # #     if matched:
# # #         passed += 1

# # #     log.append({
# # #         "user_id": user_id,
# # #         "message": message,
# # #         "expected_phrases": expected_phrases,
# # #         "response": reply,
# # #         "semantic_score": round(score, 3),
# # #         "passed": matched
# # #     })

# # # with open("evaluation/semantic_eval_results.json", "w") as f:
# # #     json.dump(log, f, indent=2)

# # # print(f"\n✅ Semantic Accuracy: {passed}/{len(tests)}")
# # import json
# # import requests
# # from sentence_transformers import SentenceTransformer, util

# # model = SentenceTransformer("all-MiniLM-L6-v2")
# # THRESHOLD = 0.55  # Semantic similarity cutoff

# # def summarize_for_eval(text: str):
# #     """Pick the most relevant sentence from LLM reply."""
# #     lines = text.split(".")
# #     for line in lines:
# #         if any(kw in line.lower() for kw in ["order", "cancel", "ship", "return", "refund", "password"]):
# #             return line.strip()
# #     return lines[0].strip()

# # def sentence_level_score(reply: str, expected_phrases):
# #     """Return highest score from any sentence to any expected phrase."""
# #     best_score = 0.0
# #     best_sent = ""
# #     sentences = [s.strip() for s in reply.split(".") if s.strip()]
# #     for sent in sentences:
# #         for phrase in expected_phrases:
# #             score = util.cos_sim(
# #                 model.encode(sent, convert_to_tensor=True),
# #                 model.encode(phrase, convert_to_tensor=True)
# #             ).item()
# #             if score > best_score:
# #                 best_score = score
# #                 best_sent = sent
# #     return best_score, best_sent

# # with open("evaluation/test_cases.json") as f:
# #     tests = json.load(f)

# # passed = 0
# # log = []

# # for i, test in enumerate(tests):
# #     user_id = test["user_id"]
# #     message = test["message"]
# #     expected_phrases = test["expected_phrases"]

# #     res = requests.post("http://localhost:8000/chat", json={
# #         "user_id": user_id,
# #         "message": message
# #     })

# #     reply = res.json().get("response", "")
# #     score, matched_sentence = sentence_level_score(reply, expected_phrases)
# #     passed_case = score >= THRESHOLD

# #     if passed_case:
# #         passed += 1

# #     print(f"[Test {i+1}] {message}")
# #     print(f"Bot: {reply}")
# #     print(f"✓ Passed (Score: {score:.2f})" if passed_case else f"✗ Failed (Score: {score:.2f})")
# #     print(f"Best Match: \"{matched_sentence}\"\n---")

# #     log.append({
# #         "user_id": user_id,
# #         "message": message,
# #         "expected_phrases": expected_phrases,
# #         "response": reply,
# #         "matched_sentence": matched_sentence,
# #         "semantic_score": round(score, 3),
# #         "passed": passed_case
# #     })

# # with open("evaluation/semantic_eval_results.json", "w") as f:
# #     json.dump(log, f, indent=2)

# # print(f"\n✅ Semantic Accuracy: {passed}/{len(tests)}")
# import json
# import requests
# from sentence_transformers import SentenceTransformer, util
# import sys
# import os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, project_root)
# from agent.agent_core import classify_intent  # Ensure this exists as a standalone function

# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# model = SentenceTransformer("all-MiniLM-L6-v2")
# THRESHOLD = 0.55

# def summarize(text: str):
#     lines = text.split(".")
#     for line in lines:
#         if any(kw in line.lower() for kw in ["order", "cancel", "ship", "return", "password"]):
#             return line.strip()
#     return lines[0].strip()

# def semantic_score(reply, expected_phrases):
#     best_score = 0
#     best_sentence = ""
#     for sentence in reply.split("."):
#         sentence = sentence.strip()
#         for phrase in expected_phrases:
#             score = util.cos_sim(
#                 model.encode(sentence, convert_to_tensor=True),
#                 model.encode(phrase, convert_to_tensor=True)
#             ).item()
#             if score > best_score:
#                 best_score = score
#                 best_sentence = sentence
#     return best_score, best_sentence

# with open("evaluation/test_cases.json") as f:
#     tests = json.load(f)

# results = []
# intent_matches = tool_matches = response_passes = high_confidence = e2e_passes = 0

# for i, test in enumerate(tests):
#     user_id = test["user_id"]
#     msg = test["message"]
#     expected_intent = test.get("expected_intent")
#     expected_tool = test.get("expected_tool")
#     expected_policy_id = test.get("expected_policy_id")
#     expected_phrases = test.get("expected_phrases", [])

#     predicted_intent = classify_intent(msg)
#     predicted_tool = predicted_intent.capitalize() + "Order" if predicted_intent != "reset" else "PasswordReset"

#     res = requests.post("http://localhost:8000/chat", json={"user_id": user_id, "message": msg})
#     reply = res.json()["response"]
#     score, matched_sent = semantic_score(reply, expected_phrases)

#     # Individual metrics
#     intent_ok = predicted_intent == expected_intent
#     tool_ok = predicted_tool == expected_tool
#     response_ok = score >= THRESHOLD
#     confidence_ok = score >= 0.50
#     all_ok = intent_ok and tool_ok and response_ok

#     if intent_ok: intent_matches += 1
#     if tool_ok: tool_matches += 1
#     if response_ok: response_passes += 1
#     if confidence_ok: high_confidence += 1
#     if all_ok: e2e_passes += 1

#     results.append({
#         "user_id": user_id,
#         "message": msg,
#         "expected_intent": expected_intent,
#         "predicted_intent": predicted_intent,
#         "expected_tool": expected_tool,
#         "predicted_tool": predicted_tool,
#         "expected_phrases": expected_phrases,
#         "response": reply,
#         "semantic_score": round(score, 3),
#         "matched_sentence": matched_sent,
#         "intent_ok": intent_ok,
#         "tool_ok": tool_ok,
#         "response_ok": response_ok,
#         "confidence_ok": confidence_ok,
#         "passed": all_ok
#     })

# with open("evaluation/semantic_eval_results.json", "w") as f:
#     json.dump(results, f, indent=2)

# total = len(tests)
# print("\nEvaluation Metrics Summary")
# print("| Metric              | Value     |")
# print("|---------------------|-----------|")
# print(f"| Intent Accuracy     | {intent_matches/total:.2%} |")
# print(f"| Tool Accuracy       | {tool_matches/total:.2%} |")
# print(f"| Response Accuracy   | {response_passes/total:.2%} |")
# print(f"| Confidence ≥ 0.75   | {high_confidence/total:.2%} |")
# print(f"| End-to-End Accuracy | {e2e_passes/total:.2%} |")
import json
import requests
import os
import sys
from sentence_transformers import CrossEncoder

# Add project root to path
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

    # Step 1: Intent prediction
    predicted_intent = classify_intent(msg)
    predicted_tool = predicted_intent.capitalize() + "Order" if predicted_intent != "reset" else "PasswordReset"

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
