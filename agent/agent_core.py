# # from agent.llm_interface import call_llm
# # from tools.cancel_tool import CancelOrderTool
# # from tools.track_tool import TrackOrderTool
# # from tools.return_tool import ReturnOrderTool
# # from tools.refund_tool import RefundStatusTool
# # from tools.reset_tool import PasswordResetTool
# # from memory.user_store import UserStore
# # from chatbot.policy.vector_search import get_relevant_policies
# # import re

# # TOOLS = {
# #     "cancel": CancelOrderTool(),
# #     "track": TrackOrderTool(),
# #     "return": ReturnOrderTool(),
# #     "refund": RefundStatusTool(),
# #     "reset": PasswordResetTool()
# # }

# # memory = UserStore()

# # def extract_order_ids(text: str):
# #     return re.findall(r"(ORD\d{3})", text.upper())

# # def classify_intent(user_input: str) -> str:
# #     prompt = f"""
# # You are an intent classifier. Classify the user's intent into one of the following:
# # cancel, track, return, refund, reset, unknown

# # User: {user_input}
# # Intent:"""
# #     return call_llm(prompt).lower().strip()

# # def build_contextual_prompt(user_id: str, user_input: str) -> str:
# #     retrieved = get_relevant_policies(user_input, top_k=1)
# #     context_text = "\n".join([f"- {r['text']} (confidence: {r['similarity']})" for r in retrieved])
# #     history = memory.get_conversation_history(user_id,limit=3)
# #     history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])
# #     return f"""
# # Policies:
# # {context_text}

# # Conversation (last 3 turns):
# # {history_text}

# # User: {user_input}
# # Answer:
# # """


# # def agent_loop(user_id: str, user_input: str) -> str:
# #     intent = classify_intent(user_input)
# #     order_ids = extract_order_ids(user_input)

# #     for oid in order_ids:
# #         memory.save_user_data(user_id, "last_order", oid)

# #     if intent in TOOLS:
# #         tool = TOOLS[intent]
# #         responses = []

# #         if intent == "cancel" and len(order_ids) > 1:
# #             for oid in order_ids:
# #                 tool_result = tool.run(user_id, user_input, memory, order_id=oid)
# #                 responses.append(tool_result)
# #         else:
# #             oid = order_ids[0] if order_ids else memory.get_user_data(user_id, "last_order")
# #             tool_result = tool.run(user_id, user_input, memory, order_id=oid)
# #             responses = [tool_result]

# #         # Retrieve policies for the input
# #         retrieved = get_relevant_policies(user_input, top_k=1)

# #         # Build LLM prompt including tool results and policy texts
# #         policy_texts = "\n".join([f"- {r['text']} (confidence: {r['similarity']:.2f})" for r in retrieved])
# #         tool_msgs = "\n".join([f"Result: {r['message']} (Success: {r['success']})" for r in responses])
# #         history = memory.get_conversation_history(user_id, limit=3)
# #         history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

# #         llm_prompt = f"""
# # You are a helpful assistant responding to user queries about orders.

# # Company Policies:
# # {policy_texts}

# # Conversation History:
# # {history_text}

# # Tool Validation Results:
# # {tool_msgs}

# # User Input:
# # {user_input}

# # Based on the above, provide a clear, friendly response that addresses the user's query and respects company policies.
# # """

# #         response = call_llm(llm_prompt)
# #     else:
# #         response = call_llm(build_contextual_prompt(user_id, user_input))

# #     memory.log_conversation(user_id, user_input, response)
# #     return response

# from agent.llm_interface import call_llm
# from tools.cancel_tool import CancelOrderTool
# from tools.track_tool import TrackOrderTool
# from tools.return_tool import ReturnOrderTool
# from tools.refund_tool import RefundStatusTool
# from tools.reset_tool import PasswordResetTool
# from memory.user_store import UserStore
# from chatbot.policy.vector_search import get_relevant_policies
# import re

# TOOLS = {
#     "cancel": CancelOrderTool(),
#     "track": TrackOrderTool(),
#     "return": ReturnOrderTool(),
#     "refund": RefundStatusTool(),
#     "reset": PasswordResetTool()
# }

# memory = UserStore()

# def extract_order_ids(text: str):
#     return re.findall(r"(ORD\d{3})", text.upper())

# def classify_intent(user_input: str) -> str:
#     prompt = f"""Classify the user's intent: cancel, track, return, refund, reset, or unknown.
# User: {user_input}
# Intent:"""
#     return call_llm(prompt).lower().strip()

# def build_contextual_prompt(user_id: str, user_input: str) -> str:
#     retrieved = get_relevant_policies(user_input, top_k=1)
#     policy_context = "\n".join([f"- {r['text']}" for r in retrieved])
#     history = memory.get_conversation_history(user_id, limit=3)
#     history_context = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])
    
#     return f"""Policies:\n{policy_context}

# Conversation:\n{history_context}

# User: {user_input}
# Answer:"""

# def agent_loop(user_id: str, user_input: str) -> str:
#     intent = classify_intent(user_input)
#     order_ids = extract_order_ids(user_input)

#     for oid in order_ids:
#         memory.save_user_data(user_id, "last_order", oid)

#     response = ""
#     if intent in TOOLS:
#         tool = TOOLS[intent]
#         if intent == "cancel" and len(order_ids) > 1:
#             responses = [
#                 tool.run(user_id, user_input, memory, order_id=oid)
#                 for oid in order_ids
#             ]
#             response = "\n".join(responses)
#         else:
#             oid = order_ids[0] if order_ids else memory.get_user_data(user_id, "last_order")
#             response = tool.run(user_id, user_input, memory, order_id=oid)
#     else:
#         response = call_llm(build_contextual_prompt(user_id, user_input))

#     memory.log_conversation(user_id, user_input, response)
#     return response
from agent.llm_interface import call_llm
from tools.cancel_tool import CancelOrderTool
from tools.track_tool import TrackOrderTool
from tools.return_tool import ReturnOrderTool
from tools.refund_tool import RefundStatusTool
from tools.reset_tool import PasswordResetTool
from memory.user_store import UserStore
from chatbot.policy.vector_search import get_relevant_policies
import re

TOOLS = {
    "cancel": CancelOrderTool(),
    "track": TrackOrderTool(),
    "return": ReturnOrderTool(),
    "refund": RefundStatusTool(),
    "reset": PasswordResetTool()
}

memory = UserStore()

def extract_order_ids(text: str):
    return re.findall(r"(ORD\d{3})", text.upper())

def classify_intent(user_input: str) -> str:
    prompt = f"Classify user intent: cancel, track, return, refund, reset, or unknown.\nUser: {user_input}\nIntent:"
    return call_llm(prompt).lower().strip()

def build_response_with_llm(user_id: str, user_input: str, tool_result: dict, policy_text: str) -> str:
    history = memory.get_conversation_history(user_id, limit=3)
    history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

    prompt = f"""
You are a helpful support assistant. Based on the company's policy, the tool's internal result, and recent conversation, answer the user clearly and conversationally.

Policy:
{policy_text}

Tool Result:
Status: {tool_result.get('status')}
Message: {tool_result.get('message')}

Conversation:
{history_text}

Now the user says: {user_input}
Answer:"""

    return call_llm(prompt)

def agent_loop(user_id: str, user_input: str) -> str:
    intent = classify_intent(user_input)
    order_ids = extract_order_ids(user_input)

    for oid in order_ids:
        memory.save_user_data(user_id, "last_order", oid)

    response = ""

    if intent in TOOLS:
        tool = TOOLS[intent]
        if intent == "cancel" and len(order_ids) > 1:
            response_parts = []
            for oid in order_ids:
                tool_result = tool.run(user_id, user_input, memory, order_id=oid)
                policies = get_relevant_policies(user_input, top_k=1)
                policy_text = policies[0]["text"] if policies else ""
                reply = build_response_with_llm(user_id, user_input, tool_result, policy_text)
                response_parts.append(reply)
            response = "\n".join(response_parts)
        else:
            oid = order_ids[0] if order_ids else memory.get_user_data(user_id, "last_order")
            tool_result = tool.run(user_id, user_input, memory, order_id=oid)
            policies = get_relevant_policies(user_input, top_k=1)
            policy_text = policies[0]["text"] if policies else ""
            response = build_response_with_llm(user_id, user_input, tool_result, policy_text)
    else:
        prompt = f"""
You are a helpful support assistant. A user is asking: "{user_input}"

Company policies:
{get_relevant_policies(user_input, top_k=1)[0]['text']}

Answer the user conversationally based on this policy.
"""
        response = call_llm(prompt)

    memory.log_conversation(user_id, user_input, response)
    return response
