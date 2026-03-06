from pydantic import BaseModel

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass
class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = {"from_attributes": True}

