from chatbot.policy.load_policies import PolicyVectorDB

db = PolicyVectorDB()
db.load_policies()

def get_relevant_policies(user_query: str, top_k=2):
    return db.query(user_query, top_k=top_k)
