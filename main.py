from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Zomato High-Traffic Order Service",
    description="Microservice backend for handling flash sale orders and user status.",
    version="1.0.0"
)

# Pydantic Model for incoming Order requests (Validation ke liye)
class OrderRequest(BaseModel):
    user_id: int
    item_name: str
    quantity: int
    total_price: float
    delivery_address: str

# Root Endpoint - Health Check
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Zomato Order API",
        "message": "System is ready for high-traffic orders!"
    }

# Mock Endpoint to simulate placing an order (Zomato Flash Sale style)
@app.post("/orders/")
def create_order(order: OrderRequest):
    # Yahan hum future mein Database (RDS) integration add karenge
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    
    return {
        "status": "success",
        "message": "Order placed successfully!",
        "order_details": {
            "user_id": order.user_id,
            "item": order.item_name,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "address": order.delivery_address,
            "order_status": "Preparing"
        }
    }

# Endpoint to check order status
@app.get("/orders/{order_id}")
def get_order_status(order_id: int):
    # Real app mein yahan RDS Database se query chalegi
    return {
        "order_id": order_id,
        "current_status": "Food is being prepared by the restaurant",
        "delivery_partner_assigned": False, # Jab delivery boy accept karega tab True hoga
        "estimated_delivery_time": "30 minutes"
    }