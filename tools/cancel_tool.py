from tools.base_tool import BaseTool
from data.orders_db import get_order
from datetime import datetime

class CancelOrderTool(BaseTool):
    name = "CancelOrder"

    def run(self, user_id, user_input, memory, **kwargs):
        order_ids = kwargs.get("order_id") or memory.get_user_data(user_id, "last_order")

        # Always make order_ids a list
        if isinstance(order_ids, str):
            order_ids = [order_ids]

        if not order_ids:
            return {"status": "error", "message": "No order ID provided or remembered."}

        results = []
        for order_id in order_ids:
            order = get_order(order_id)
            if not order:
                results.append(f"❌ Order {order_id} not found.")
                continue

            if order["user_id"] != user_id:
                results.append(f"❌ Order {order_id} does not belong to you.")
                continue

            order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
            if (datetime.today() - order_date).days > 10:
                results.append(f"⏳ Order {order_id} is older than 10 days and cannot be cancelled.")
                continue

            results.append(f"✅ Order {order_id} has been cancelled.")

        final_message = "\n".join(results)
        return {"status": "success", "message": final_message}
