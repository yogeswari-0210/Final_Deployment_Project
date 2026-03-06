

from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from typing import List
from schemas.cart_schemas import  CartItemRead
from schemas.cart_items_schemas import CartItemCreate,CartItemRead
from dependency.db_dependency import get_db
from models.wishlist_models import Wishlist
from schemas.wishlist_schemas import WishlistCreate,WishlistRead
from models.cart_models import Cart
from models.user_models import User
from dependency.auth_dependency import get_current_user


router = APIRouter(
    prefix="/wishlists",
    tags=["Wishlists"]
)





@router.post("/add", response_model=WishlistRead)
def add_to_wishlist(
    item: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # <-- JWT dependency
):
    user_id = current_user.id  # get user_id from token

    existing = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.product_id == item.product_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    new_item = Wishlist(user_id=user_id, product_id=item.product_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item



@router.get("/me", response_model=List[WishlistRead])
def get_my_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return items


@router.delete("/remove/{wishlist_id}")
def remove_from_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Wishlist item removed"}




@router.post("/move-to-cart", response_model=CartItemRead)
def move_wishlist_to_cart(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    # Check wishlist item
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    # Check user's cart
    existing_cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == wishlist_item.product_id
    ).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        db.commit()
        db.refresh(existing_cart_item)

        db.delete(wishlist_item)
        db.commit()
        return existing_cart_item

    new_cart_item = Cart(
        user_id=user_id,
        product_id=wishlist_item.product_id,
        quantity=1
    )
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    db.delete(wishlist_item)
    db.commit()

    return new_cart_item




# # Add product to wishlist

# @router.post("/add", response_model=WishlistRead)
# def add_to_wishlist(item: WishlistCreate, db: Session = Depends(get_db)):
#     existing = db.query(Wishlist).filter(
#         Wishlist.user_id == item.user_id,
#         Wishlist.product_id == item.product_id
#     ).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Product already in wishlist")

#     new_item = Wishlist(user_id=item.user_id, product_id=item.product_id)
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item


# Get wishlist items by user_id

# @router.get("/user/{user_id}", response_model=List[WishlistRead])
# def get_wishlist_by_user(user_id: int, db: Session = Depends(get_db)):
#     items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
#     return items


# Remove product from wishlist

# @router.delete("/remove/{wishlist_id}")
# def remove_from_wishlist(wishlist_id: int, db: Session = Depends(get_db)):
#     item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
#     if not item:
#         raise HTTPException(status_code=404, detail="Wishlist item not found")
#     db.delete(item)
#     db.commit()
#     return {"detail": "Wishlist item removed"}



# # Move a product from wishlist to cart
# @router.post("/move-to-cart", response_model=CartItemRead)
# def move_wishlist_to_cart(wishlist_id: int, db: Session = Depends(get_db)):
#     # check wishlist item
#     wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
#     if not wishlist_item:
#         raise HTTPException(status_code=404, detail="Wishlist item not found")
    
#     # Check  user's cart
#     existing_cart_item = db.query(Cart).filter(
#         Cart.user_id == wishlist_item.user_id,
#         Cart.product_id == wishlist_item.product_id
#     ).first()
    
#     if existing_cart_item:
      
#         existing_cart_item.quantity += 1
#         db.commit()
#         db.refresh(existing_cart_item)
       
#         db.delete(wishlist_item)
#         db.commit()
#         return existing_cart_item

   
#     new_cart_item = Cart(
#         user_id=wishlist_item.user_id,
#         product_id=wishlist_item.product_id,
#         quantity=1  
#     )
#     db.add(new_cart_item)
#     db.commit()
#     db.refresh(new_cart_item)


#     db.delete(wishlist_item)
#     db.commit()

#     return new_cart_item
