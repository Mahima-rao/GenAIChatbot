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
