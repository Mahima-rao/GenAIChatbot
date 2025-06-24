class BaseTool:
    name = "BaseTool"
    description = "Abstract base class for chatbot tools."

    def run(self, user_id: str, user_input: str, memory, **kwargs):
        raise NotImplementedError("Each tool must implement a run method.")
