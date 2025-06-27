
import json
from memory.user_store import UserStore
from tools.tool_registry import tool_registry
from chatbot.policy.vector_search import get_relevant_policies
from agent.llm_interface import call_llm

memory = UserStore()

def classify_intent(user_input: str) -> str:
    """
    Classify the user intent using LLM. Avoid 'unknown' unless absolutely needed.
    Normalizes slight variations and adds few-shot examples.
    """
    prompt = f"""
Classify the user's intent into one of the following categories:
- cancel
- track
- return
- refund
- reset

Examples:
"Can I cancel my order?" → cancel  
"I want to return a product" → return  
"Where is my order?" → track  
"When will I get my money back?" → refund  
"I forgot my password" → reset  

Now classify the following message:
"{user_input}"
Intent:"""

    intent = call_llm(prompt, temperature=0.0).strip().lower()
    intent = intent.replace(".", "").replace("intent:", "").strip()

    for canonical in ["cancel", "track", "return", "refund", "reset"]:
        if canonical in intent:
            return canonical

    return "unknown"


def build_tool_selection_prompt(user_input, user_id):
    last_order = memory.get_user_data(user_id, "last_order")
    context = f"Last known order ID: {last_order}" if last_order else "No known order ID."
    return f"""
You are a backend AI agent. Based on the user's message, decide which tool to use and what arguments to pass.

Context:
{context}

Return ONLY a JSON object like this:
{{
  "tool": "ToolName",
  "args": {{
    "order_id": "ORD123"
  }}
}}

Available tools:
- CancelOrder: Requires 'order_id'
- TrackOrder: Requires 'order_id'
- ReturnOrder: Requires 'order_id'
- RefundStatus: Requires 'order_id'
- PasswordReset: No args needed

User message: "{user_input}"
"""


def build_response_prompt(user_id, user_input, tool_result: dict, matched_policy: str, confidence: float):
    history = memory.get_conversation_history(user_id, limit=3)
    history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])

    return f"""
You are a helpful support assistant. Based on the company's policy, the tool's internal result, and recent conversation, answer the user clearly and conversationally.

DO NOT guess or fabricate answers — only reflect the actual tool result.

If the tool status is 'success', confirm politely.
If the tool status is 'denied' or 'error', explain it using the policy if relevant.

Tool Result:
Status: {tool_result.get("status")}
Message: {tool_result.get("message")}

Relevant Policy (confidence {confidence:.2f}):
{matched_policy}

Conversation History:
{history_text}

User just said:
"{user_input}"

Now respond clearly and helpfully:
"""


def agent_loop(user_id, user_input):
    memory.save_user_data(user_id, "last_message", user_input)

    # Step 1: Let LLM choose tool and arguments
    plan_prompt = build_tool_selection_prompt(user_input, user_id)
    plan_raw = call_llm(plan_prompt, temperature=0.0)

    try:
        plan = json.loads(plan_raw)
        tool_name = plan.get("tool")
        args = plan.get("args", {})
    except Exception:
        return "Sorry, I couldn't understand your request structure."

    if tool_name not in tool_registry:
        return f"Tool '{tool_name}' is not supported."

    # Step 2: Handle order ID fallback from memory
    if "order_id" not in args or not args["order_id"]:
        last_order = memory.get_user_data(user_id, "last_order")
        if last_order:
            args["order_id"] = last_order

    if "order_id" in args and args["order_id"]:
        memory.save_user_data(user_id, "last_order", args["order_id"])

    # Step 3: Run tool
    tool = tool_registry[tool_name]()
    result = tool.run(user_id=user_id, user_input=user_input, memory=memory, **args)
    memory.save_user_data(user_id, "last_tool_result", result)

    # Step 4: Retrieve policy
    top_policy = get_relevant_policies(user_input, top_k=1)[0]
    matched_policy = top_policy["text"]
    confidence = top_policy["similarity"]

    # Step 5: Generate response
    response_prompt = build_response_prompt(user_id, user_input, result, matched_policy, confidence)
    response = call_llm(response_prompt, temperature=0.2)

    memory.log_conversation(user_id, user_input, response)
    return response
