from tools.base_tool import BaseTool
from data.orders_db import get_order

class RefundStatusTool(BaseTool):
    name = "RefundStatus"

    def run(self, user_id, user_input, memory, **kwargs):
        order_id = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")
        if not order_id:
            return {"status": "error", "message": "No order ID provided or remembered."}

        order = get_order(order_id)
        if not order:
            return {"status": "error", "message": f"Order {order_id} not found."}

        if order["user_id"] != user_id:
            return {"status": "error", "message": f"Order {order_id} does not belong to you."}

        return {"status": "success", "message": f"Refund for order {order_id} is currently being processed."}
