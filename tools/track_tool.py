# # # from tools.base_tool import BaseTool
# # # from api.orders_db import get_order

# # # class TrackOrderTool(BaseTool):
# # #     name = "TrackOrder"

# # #     def run(self, user_id, user_input, memory, **kwargs):
# # #         order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
# # #         order = get_order(order_id)
# # #         if not order:
# # #             return f"Order {order_id} not found."
# # #         if order["user_id"] != user_id:
# # #             return f"Order {order_id} does not belong to you. Please check the order number."

# # #         return f"Order {order_id} is currently {order['status']}."
# # from tools.base_tool import BaseTool
# # from api.orders_db import get_order

# # class TrackOrderTool(BaseTool):
# #     name = "TrackOrder"

# #     def run(self, user_id, user_input, memory, **kwargs):
# #         order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
# #         order = get_order(order_id)
# #         if not order:
# #             return {"success": False, "message": f"Order {order_id} not found.", "policy_id": None}
# #         if order["user_id"] != user_id:
# #             return {"success": False, "message": f"Order {order_id} does not belong to you.", "policy_id": None}

# #         return {"success": True, "message": f"Order {order_id} is currently {order['status']}.", "policy_id": None}
# from tools.base_tool import BaseTool
# from api.orders_db import get_order

# class TrackOrderTool(BaseTool):
#     name = "TrackOrder"

#     def run(self, user_id, user_input, memory, **kwargs):
#         order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
#         if not order_id:
#             return "No order ID provided or remembered."

#         order = get_order(order_id)
#         if not order:
#             return f"Order {order_id} not found."

#         if order["user_id"] != user_id:
#             return f"Order {order_id} does not belong to you."

#         return f"Order {order_id} is currently {order['status']}."
from tools.base_tool import BaseTool
from api.orders_db import get_order

class TrackOrderTool(BaseTool):
    name = "TrackOrder"

    def run(self, user_id, user_input, memory, **kwargs):
        order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
        if not order_id:
            return {"status": "error", "message": "No order ID provided or remembered."}

        order = get_order(order_id)
        if not order:
            return {"status": "error", "message": f"Order {order_id} not found."}

        if order["user_id"] != user_id:
            return {"status": "error", "message": f"Order {order_id} does not belong to you."}

        return {"status": "success", "message": f"Order {order_id} is currently {order['status']}."}
