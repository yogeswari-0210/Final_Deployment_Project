from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: int
    category_id: Optional[int]
    image_url: Optional[str] = None 
    description: Optional[str] = None 

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True





