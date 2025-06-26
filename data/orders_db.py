orders = {
    "ORD001": {"user_id": "Shashi", "order_date": "2025-06-10", "status": "delivered"},
    "ORD002": {"user_id": "Jo", "order_date": "2025-06-20", "status": "shipped"},
    "ORD003": {"user_id": "Magda", "order_date": "2025-06-23", "status": "processing"},
    "ORD004": {"user_id": "Magda", "order_date": "2025-06-23", "status": "processing"},
    "ORD005": {"user_id": "Mahima", "order_date": "2025-06-05", "status": "delivered"},
    "ORD006": {"user_id": "user5", "order_date": "2025-06-01", "status": "delivered"},

}

def get_order(order_id: str):
    return orders.get(order_id)
