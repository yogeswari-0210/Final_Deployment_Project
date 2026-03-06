from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .product_schemas import ProductRead

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class OrderItemRead(BaseModel):
    product_id: int
    quantity: int
    product: ProductRead

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]
    address: str
    payment_method: str

class OrderRead(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    address: Optional[str] = "" 
    payment_method: Optional[str] = ""
    status: Optional[str] = "Ordered"
    total_price: float
    created_at: datetime
    admin_id: Optional[int] = None
    admin_name: Optional[str] = None
    items: List[OrderItemRead] = []

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

class OrderUpdate(BaseModel):
    quantity: int
