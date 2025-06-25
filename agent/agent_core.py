import re
from agent.llm_interface import call_llm
from tools.cancel_tool import CancelOrderTool
from tools.track_tool import TrackOrderTool
from tools.return_tool import ReturnOrderTool
from tools.refund_tool import RefundStatusTool
from tools.reset_tool import PasswordResetTool
from memory.user_store import UserStore
from chatbot.policy.vector_search import get_relevant_policies

TOOLS = {
    "cancel": CancelOrderTool(),
    "track": TrackOrderTool(),
    "return": ReturnOrderTool(),
    "refund": RefundStatusTool(),
    "reset": PasswordResetTool()
}

memory = UserStore()


def extract_order_ids(text: str):
    """Extract order IDs matching pattern ORD### from the text."""
    return re.findall(r"(ORD\d{3})", text.upper())


def classify_intent(user_input: str) -> str:
    """Call LLM to classify intent from user input."""
    prompt = f"Classify user intent: cancel, track, return, refund, reset, or unknown.\nUser: {user_input}\nIntent:"
    intent = call_llm(prompt).lower().strip()
    # Basic sanity fallback
    if intent not in TOOLS.keys():
        intent = "unknown"
    return intent


def build_response_with_llm(user_id: str, user_input: str, tool_result: dict, policy_text: str) -> str:
    """Build final user-facing response based on policy, tool result, and conversation history."""
    history = memory.get_conversation_history(user_id, limit=3)
    history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

    prompt = f"""
You are a helpful support assistant. Based on the company's policy, the tool's internal result, and recent conversation, answer the user clearly and conversationally. 
If the tool response is a SUCCESS, confirm it politely and do not override it. 
If the tool response is DENIED or ERROR, explain why using the policy if applicable. Do not invent reasons not in the tool output.
Always reflect the actual result from the system accurately.

Policy:
{policy_text}

Tool Result:
Status: {tool_result.get('status')}
Message: {tool_result.get('message')}

Conversation:
{history_text}

Now the user says:
{user_input}

Answer:"""

    return call_llm(prompt)


def agent_loop(user_id: str, user_input: str) -> str:
    """Main agent loop handling user input and generating chatbot response."""
    intent = classify_intent(user_input)
    order_ids = extract_order_ids(user_input)

    # Save last mentioned order id for user context
    for oid in order_ids:
        memory.save_user_data(user_id, "last_order", oid)

    response = ""

    if intent in TOOLS:
        tool = TOOLS[intent]

        if intent == "cancel" and len(order_ids) > 1:
            # If multiple orders to cancel, handle them one by one
            response_parts = []
            for oid in order_ids:
                tool_result = tool.run(user_id, user_input, memory, order_id=oid)
                policies = get_relevant_policies(user_input, top_k=1)
                policy_text = policies[0]["text"] if policies else ""
                 # Debug prints here
                print(f"Tool Result Status: {tool_result.get('status')}")
                print(f"Tool Result Message: {tool_result.get('message')}")
                print(f"Policy Text: {policy_text}")
                reply = build_response_with_llm(user_id, user_input, tool_result, policy_text)
                response_parts.append(reply)
            response = "\n".join(response_parts)
        else:
            # Single order or other intents
            oid = order_ids[0] if order_ids else memory.get_user_data(user_id, "last_order")
            tool_result = tool.run(user_id, user_input, memory, order_id=oid)
            policies = get_relevant_policies(user_input, top_k=1)
            policy_text = policies[0]["text"] if policies else ""
            response = build_response_with_llm(user_id, user_input, tool_result, policy_text)
    else:
        # Intent unknown or no tool for intent — fallback to general policy-based answer
        policies = get_relevant_policies(user_input, top_k=1)
        policy_text = policies[0]["text"] if policies else "No specific policy found."

        prompt = f"""
You are a helpful support assistant. A user is asking: "{user_input}"

Company policies:
{policy_text}

Answer the user conversationally based on this policy.
"""
        response = call_llm(prompt)

    memory.log_conversation(user_id, user_input, response)
    return response
