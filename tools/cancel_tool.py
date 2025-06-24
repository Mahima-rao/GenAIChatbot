
# #     def run(self, user_id, user_input, memory, **kwargs):
# #         order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
# #         order = get_order(order_id)
# #         if not order:
# #             return f"Order {order_id} not found."
# #         if order["user_id"] != user_id:
# #             return f"Order {order_id} does not belong to you. Please check the order number."

# #         order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
# #         if (datetime.today() - order_date).days > 10:
# #             return f"Order {order_id} is older than 10 days and cannot be cancelled."
# #         return f"Order {order_id} has been successfully cancelled."
# from tools.base_tool import BaseTool
# from api.orders_db import get_order
# from datetime import datetime

# class CancelOrderTool(BaseTool):
#     name = "CancelOrder"

#     def run(self, user_id, user_input, memory, **kwargs):
#         order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
#         order = get_order(order_id)
#         if not order:
#             return {"success": False, "message": f"Order {order_id} not found.", "policy_id": None}

#         if order["user_id"] != user_id:
#             return {"success": False, "message": f"Order {order_id} does not belong to you.", "policy_id": None}

#         order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
#         if (datetime.today() - order_date).days > 10:
#             return {"success": False, "message": f"Order {order_id} is older than 10 days and cannot be cancelled.",
#                     "policy_id": "P1"}  # Policy ID example

#         return {"success": True, "message": f"Order {order_id} has been successfully cancelled.", "policy_id": "P1"}
from tools.base_tool import BaseTool
from api.orders_db import get_order
from datetime import datetime

class CancelOrderTool(BaseTool):
    name = "CancelOrder"

    def run(self, user_id, user_input, memory, **kwargs):
        order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
        if not order_id:
            return {"status": "error", "message": "No order ID provided or remembered."}

        order = get_order(order_id)
        if not order:
            return {"status": "error", "message": f"Order {order_id} not found."}
        if order["user_id"] != user_id:
            return {"status": "error", "message": f"Order {order_id} does not belong to you."}

        order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
        if (datetime.today() - order_date).days > 10:
            return {"status": "denied", "message": f"Order {order_id} is older than 10 days and cannot be cancelled."}

        return {"status": "success", "message": f"Order {order_id} has been cancelled."}
