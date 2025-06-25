orders = {
    "ORD001": {"user_id": "user1", "order_date": "2025-06-10", "status": "delivered"},
    "ORD002": {"user_id": "user2", "order_date": "2025-06-20", "status": "shipped"},
    "ORD003": {"user_id": "user3", "order_date": "2025-06-23", "status": "processing"},
    "ORD004": {"user_id": "user3", "order_date": "2025-06-23", "status": "processing"},
    "ORD005": {"user_id": "user4", "order_date": "2025-06-05", "status": "delivered"},
    "ORD006": {"user_id": "user5", "order_date": "2025-06-01", "status": "delivered"},

}

def get_order(order_id: str):
    return orders.get(order_id)
