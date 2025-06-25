from tools.base_tool import BaseTool

class PasswordResetTool(BaseTool):
    name = "PasswordReset"

    def run(self, user_id, user_input, memory, **kwargs):
        return {
            "status": "success",
            "message": "A password reset link has been sent to your registered email address."
        }
