from tools.base_tool import BaseTool
from data.orders_db import get_order

class ReturnOrderTool(BaseTool):
    name = "ReturnOrder"

    def run(self, user_id, user_input, memory, **kwargs):
        order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
        if not order_id:
            return {"status": "error", "message": "No order ID provided or remembered."}

        order = get_order(order_id)
        if not order:
            return {"status": "error", "message": f"Order {order_id} not found."}

        if order["user_id"] != user_id:
            return {"status": "error", "message": f"Order {order_id} does not belong to you."}

        if order["status"] != "delivered":
            return {"status": "denied", "message": f"Order {order_id} cannot be returned until it is delivered."}

        return {"status": "success", "message": f"Return for order {order_id} has been initiated."}
