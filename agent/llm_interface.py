import requests
import time

def call_llm(prompt: str) -> str:
    start = time.perf_counter()
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    duration = time.perf_counter() - start
    print(f"[LLM] Response time: {duration:.2f}s")
    return response.json()["response"].strip()
