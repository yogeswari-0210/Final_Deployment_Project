
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency.db_dependency import get_db
from models.cart_models import Cart
from models.user_models import User
from schemas.cart_schemas import CartCreate,CartItemRead ,CartItemUpdate
from schemas. cart_items_schemas import CartItemBase,CartItemCreate,CartItemUpdate
from models.wishlist_models import Wishlist
from schemas.wishlist_schemas import WishlistRead
from dependency.auth_dependency import get_current_user


router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)

#get all carts
@router.get("/", response_model=List[CartCreate])
def get_carts(db: Session = Depends(get_db)):
    return db.query(Cart).all()

@router.post("/add", response_model=CartItemRead)
def add_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id  # <-- secure
    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == cart_item.product_id
    ).first()
    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = Cart(
        user_id=user_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



# Get all cart items for the logged-in user
@router.get("/me", response_model=List[CartItemRead])
def get_cart_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    return db.query(Cart).filter(Cart.user_id == user_id).all()


# Remove a single cart item (must belong to current user)
@router.delete("/remove/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Cart).filter(Cart.id == cart_item_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Cart item removed successfully"}


# Update quantity of a cart item (must belong to current user)
@router.put("/update/{cart_item_id}", response_model=CartItemRead)
def update_cart_item_quantity(
    cart_item_id: int,
    cart_item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(Cart).filter(Cart.id == cart_item_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    item.quantity = cart_item_update.quantity
    db.commit()
    db.refresh(item)
    return item


# Move cart item to wishlist (must belong to current user)
@router.post("/move-to-wishlist", response_model=WishlistRead)
def move_cart_to_wishlist(cart_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_item = db.query(Cart).filter(Cart.id == cart_item_id, Cart.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check if product already in wishlist
    existing_wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == cart_item.product_id
    ).first()
    
    if existing_wishlist_item:
        db.delete(cart_item)
        db.commit()
        return existing_wishlist_item

    wishlist_item = Wishlist(
        user_id=current_user.id,
        product_id=cart_item.product_id
    )
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)

    db.delete(cart_item)
    db.commit()

    return wishlist_item






























#add to cart

# @router.post("/add", response_model=CartItemRead)
# def add_to_cart(cart_item: CartItemCreate, user_id: int, db: Session = Depends(get_db)):
#     existing_item = db.query(Cart).filter(
#         Cart.user_id == user_id, 
#         Cart.product_id == cart_item.product_id
#     ).first()
#     if existing_item:
#         existing_item.quantity += cart_item.quantity
#         db.commit()
#         db.refresh(existing_item)
#         return existing_item

#     new_item = Cart(
#         user_id=user_id,
#         product_id=cart_item.product_id,
#         quantity=cart_item.quantity
#     )
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item






# # Get all cart items by  user_id

# @router.get("/user/{user_id}", response_model=List[CartItemRead])
# def get_cart_items_by_userid(user_id: int, db: Session = Depends(get_db)):
#     return db.query(Cart).filter(Cart.user_id == user_id).all()


# # Remove a single cart item

# @router.delete("/remove/{cart_item_id}")
# def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
#     item = db.query(Cart).filter(Cart.id == cart_item_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
#     db.delete(item)
#     db.commit()
#     return {"detail": "Cart item removed successfully"}


# # Update quantity of a cart item
# @router.put("/update/{cart_item_id}", response_model=CartItemRead)
# def update_cart_item_quantity(
#     cart_item_id: int, 
#     cart_item_update: CartItemUpdate, 
#     db: Session = Depends(get_db)
# ):
   
#     item = db.query(Cart).filter(Cart.id == cart_item_id).first()
    
#     if not item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
    
 
#     item.quantity = cart_item_update.quantity
#     db.commit()
#     db.refresh(item)
    
#     return item




# # Move cart to wishlist
# @router.post("/move-to-wishlist", response_model=WishlistRead)
# def move_cart_to_wishlist(cart_item_id: int, db: Session = Depends(get_db)):
   
#     cart_item = db.query(Cart).filter(Cart.id == cart_item_id).first()
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
    
#     # Check product in wishlist

#     existing_wishlist_item = db.query(Wishlist).filter(
#         Wishlist.user_id == cart_item.user_id,
#         Wishlist.product_id == cart_item.product_id
#     ).first()
    
#     if existing_wishlist_item:
      
#         db.delete(cart_item)
#         db.commit()
#         return existing_wishlist_item


#     wishlist_item = Wishlist(
#         user_id=cart_item.user_id,
#         product_id=cart_item.product_id
#     )
#     db.add(wishlist_item)
#     db.commit()
#     db.refresh(wishlist_item)

  
#     db.delete(cart_item)
#     db.commit()

#     return wishlist_item

