class UserStore:
    def __init__(self):
        self.memory = {}

    def save_user_data(self, user_id, key, value):
        if user_id not in self.memory:
            self.memory[user_id] = {}
        self.memory[user_id][key] = value

    def get_user_data(self, user_id, key):
        return self.memory.get(user_id, {}).get(key)

    def get_full_context(self, user_id):
        return self.memory.get(user_id, {})

    def log_conversation(self, user_id, user_msg, bot_response):
        if user_id not in self.memory:
            self.memory[user_id] = {}
        if "history" not in self.memory[user_id]:
            self.memory[user_id]["history"] = []
        self.memory[user_id]["history"].append({
            "user": user_msg,
            "bot": bot_response
        })

    def get_conversation_history(self, user_id, limit=5):
        return self.memory.get(user_id, {}).get("history", [])[-limit:]
