# from fastapi import FastAPI
# from pydantic import BaseModel
# from chatbot.generative_bot import handle_user_input
# from api import order_cancellation, order_tracking

# app = FastAPI()

# app.include_router(order_cancellation.router)
# app.include_router(order_tracking.router)

# class ChatInput(BaseModel):
#     message: str

# @app.post("/chat")
# def chat(input: ChatInput):
#     response = handle_user_input(input.message)
#     return {"response": response}

from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent_core import agent_loop

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.user_id:
        return {"response": "Missing user ID. Please log in or provide a valid ID."}
    response = agent_loop(req.user_id, req.message)
    return {"response": response}
