
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from typing import List

# from dependency import get_db
# from models.cart_items_models import CartItem
# from schemas.cart_items_schemas import CartItemCreate

# router = APIRouter(
#     prefix="/cart-items",
#     tags=["CartItems"]
# )

# @router.post("/", response_model=CartItemCreate)
# def add_cart_item(item: CartItemCreate, db: Session = Depends(get_db)):
#     new_item = CartItem(cart_id=item.cart_id, product_id=item.product_id, quantity=item.quantity)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item

# @router.get("/", response_model=List[CartItemCreate])
# def get_cart_items(db: Session = Depends(get_db)):
#     return db.query(CartItem).all()
