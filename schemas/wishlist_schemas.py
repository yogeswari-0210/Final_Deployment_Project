from pydantic import BaseModel
from typing import List

class WishlistBase(BaseModel):
    product_id: int

class WishlistCreate(WishlistBase):
    pass

from .product_schemas import ProductRead

class WishlistRead(WishlistBase):
    id: int
    user_id: int
    product: ProductRead

    class Config:
        from_attributes = True  

