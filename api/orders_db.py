orders = {
    "ORD001": {"user_id": "user1", "order_date": "2025-06-10", "status": "delivered"},
    "ORD002": {"user_id": "user2", "order_date": "2025-06-01", "status": "shipped"},
    "ORD003": {"user_id": "user3", "order_date": "2025-06-23", "status": "processing"},
    "ORD004": {"user_id": "user3", "order_date": "2025-06-23", "status": "processing"},

}

def get_order(order_id: str):
    return orders.get(order_id)
