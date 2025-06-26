import requests
import time

def call_llm(prompt: str, temperature: float = 0.2) -> str:
    start = time.perf_counter()
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "temperature": temperature  
    })
    duration = time.perf_counter() - start
    print(f"[LLM] Response time: {duration:.2f}s")
    
    try:
        return response.json()["response"].strip()
    except Exception:
        print("⚠️ LLM returned invalid response:", response.text[:300])
        return "Sorry, I couldn't generate a valid response."
