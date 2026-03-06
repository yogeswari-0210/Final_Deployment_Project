


from pydantic import BaseModel

from typing import List
from .cart_items_schemas import CartItemRead, CartItemUpdate


class CartBase(BaseModel):
    user_id: int 


class CartCreate(CartBase):
    pass


class CartRead(CartBase):
    id: int
    cart_items: List[CartItemRead] = []  

    class Config:
        from_attributes = True
