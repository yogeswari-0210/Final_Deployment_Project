


from pydantic import BaseModel, Field

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int
 




from .product_schemas import ProductRead

class CartItemRead(BaseModel):
    id: int         
    user_id: int
    product_id: int
    quantity: int
    product: ProductRead

    class Config:
        from_attributes = True

