from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# 1. AWS RDS DATABASE CONFIGURATION
# ==========================================
# ⚠️ WARNING: 'TeraPassword' hata kar apna asli password likhna!
DATABASE_URL = "postgresql+psycopg2://postgres:Divy1234qwer@zomato-db.ch8cyq2g6j89.ap-southeast-2.rds.amazonaws.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. DATABASE MODEL (SQL TABLE SCHEMA)
# ==========================================
class DBOrder(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    item_name = Column(String)
    quantity = Column(Integer)
    total_price = Column(Float)
    delivery_address = Column(String)

# Yeh line start hote hi AWS RDS mein 'orders' naam ki table automatic bana degi
Base.metadata.create_all(bind=engine)

# ==========================================
# 3. FASTAPI APP INITIALIZATION
# ==========================================
app = FastAPI(
    title="Zomato High-Traffic Order Service",
    description="Microservice backend for handling flash sale orders with AWS RDS integration.",
    version="1.0.0"
)

# Pydantic Model (Incoming Request Data Validation)
class OrderRequest(BaseModel):
    user_id: int
    item_name: str
    quantity: int
    total_price: float
    delivery_address: str

# ==========================================
# 4. API ENDPOINTS
# ==========================================
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Zomato Order API",
        "message": "System is now connected to secure AWS RDS Database!"
    }

@app.post("/orders/")
def create_order(order: OrderRequest):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    
    # Database ka connection open karo
    db = SessionLocal()
    
    try:
        # Naya order database model mein daalo
        new_order = DBOrder(
            user_id=order.user_id,
            item_name=order.item_name,
            quantity=order.quantity,
            total_price=order.total_price,
            delivery_address=order.delivery_address
        )
        
        # AWS RDS mein actually save (commit) karo
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        return {
            "status": "success",
            "message": "Real order permanently saved to AWS RDS!",
            "order_id": new_order.id
        }
    finally:
        # Har request ke baad connection close karna good practice hai
        db.close() 

@app.get("/orders/{order_id}")
def get_order_status(order_id: int):
    db = SessionLocal()
    try:
        # Database se id ke hisaab se order dhundo
        order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found in database")
            
        return {
            "order_id": order.id,
            "item_name": order.item_name,
            "total_paid": order.total_price,
            "current_status": "Food is being prepared by the restaurant",
            "delivery_partner_assigned": False
        }
    finally:
        db.close()