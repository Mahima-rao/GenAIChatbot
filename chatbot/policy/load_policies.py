import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class PolicyVectorDB:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.policies = []
        self.embeddings = []
        self.index = None

    def load_policies(self, path="chatbot/policy/policy_store.json"):
        with open(path, "r") as f:
            self.policies = json.load(f)

        texts = [p["text"] for p in self.policies]
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)

        self.index = faiss.IndexFlatL2(self.embeddings[0].shape[0])
        self.index.add(np.array(self.embeddings))

    def query(self, question, top_k=1):
        query_vector = self.model.encode([question], convert_to_numpy=True)
        distances, indices = self.index.search(query_vector, top_k)
        results = []

        for idx, dist in zip(indices[0], distances[0]):
            policy = self.policies[idx]
            similarity = 1 / (1 + dist)
            results.append({
                "id": policy["id"],
                "text": policy["text"],
                "similarity": round(float(similarity), 3)
            })

        return results
