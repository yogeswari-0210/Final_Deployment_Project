
from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
import cloudinary.uploader
from sqlalchemy.orm import Session
from typing import List
from dependency.auth_dependency import get_current_user
from dependency.db_dependency import get_db
from models.cart_models import Cart
from models.order_models import Order
from models.order_items_models import OrderItem
from models.product_models import Product
from schemas.order_schemas import OrderCreate, OrderRead, OrderUpdate, OrderItemCreate, OrderItemRead, OrderStatusUpdate
from models.user_models import User
from sqlalchemy import func

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)











# -------------------------------
# Create order (JWT-secured)
# -------------------------------
@router.post("/create", response_model=OrderRead)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # <-- JWT user
):
    user_id = current_user.id

    if not order.items:
        raise HTTPException(status_code=400, detail="No items in order")

    total_price = 0

    # Calculate total price
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )
        total_price += product.price * item.quantity

    # Create order
    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        address=order.address,
        payment_method=order.payment_method
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add order items
    order_items = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)
        order_items.append(order_item)

    db.commit()
    new_order.items = order_items

    # Clear user's cart after successful order
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()

    return new_order


# -------------------------------
# Get all orders of logged-in user
# -------------------------------
@router.get("/me", response_model=List[OrderRead])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


# -------------------------------
# Delete an order (user-specific)
# -------------------------------
@router.delete("/delete/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id  # Only allow user's own order
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}


# -------------------------------
# ADMIN: Get all orders (paginated, sorted by date DESC)
# -------------------------------
@router.get("/admin/all", response_model=List[dict])
def get_all_orders_admin(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    offset = (page - 1) * size
    
    # Get unique order IDs that contain products owned by this admin
    order_ids_query = db.query(Order.id)\
        .join(OrderItem)\
        .join(Product)\
        .filter(Product.admin_id == current_user.id)\
        .group_by(Order.id, Order.created_at)\
        .order_by(Order.created_at.desc())
    
    # Paginate unique order IDs
    paged_order_ids = [r[0] for r in order_ids_query.offset(offset).limit(size).all()]
    
    if not paged_order_ids:
        return []

    # Fetch full Order objects with their items
    orders = db.query(Order).filter(Order.id.in_(paged_order_ids)).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        # Filter items to only show what belongs to this admin
        admin_items = [item for item in order.items if item.product.admin_id == current_user.id]
        
        # Aggregate product names and calculate the admin's share of the total price
        product_names = ", ".join([item.product.name for item in admin_items])
        total_admin_price = sum(item.quantity * item.price for item in admin_items)
        total_quantity = sum(item.quantity for item in admin_items)

        result.append({
            "order_id": order.id,
            "product_name": product_names,
            "total_price": total_admin_price,
            "quantity": total_quantity,
            "status": order.status,
            "created_at": order.created_at,
            "user_name": order.user.username if order.user else "Anonymous"
        })
        
    return result

# -------------------------------
# ADMIN: Update order status
# -------------------------------
@router.put("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify permission: Admin must own at least one product in this order
    owns_product = db.query(OrderItem).join(Product).filter(
        OrderItem.order_id == order_id,
        Product.admin_id == current_user.id
    ).first()
    
    if not owns_product:
        raise HTTPException(status_code=403, detail="Access denied: You do not own any products in this order")
    
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    order.user_name = order.user.username
    order.admin_name = order.admin.username if order.admin else "Unknown"
    return order

# -------------------------------
# ADMIN: Get analytics by category
# -------------------------------
@router.get("/admin/analytics")
def get_order_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    # Total Orders: Unique orders containing products owned by the admin
    total_orders = db.query(func.count(func.distinct(Order.id)))\
        .join(OrderItem)\
        .join(Product)\
        .filter(Product.admin_id == current_user.id).scalar() or 0
        
    # Total Delivered: Unique orders with status 'Delivered' containing products owned by the admin
    delivered_orders = db.query(func.count(func.distinct(Order.id)))\
        .join(OrderItem)\
        .join(Product)\
        .filter(Product.admin_id == current_user.id, Order.status == "Delivered").scalar() or 0
        
    # Pending-to-Ship: Status 'Ordered'
    pending_to_ship = db.query(func.count(func.distinct(Order.id)))\
        .join(OrderItem)\
        .join(Product)\
        .filter(Product.admin_id == current_user.id, Order.status == "Ordered").scalar() or 0
        
    # Total Revenue: Sum of (quantity * item_price) for DELIVERED orders for products owned by the admin
    total_revenue = db.query(func.sum(OrderItem.quantity * OrderItem.price))\
        .join(Product)\
        .join(Order)\
        .filter(Product.admin_id == current_user.id, Order.status == "Delivered").scalar() or 0
        
    return {
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "pending_to_ship": pending_to_ship,
        "total_revenue": total_revenue
    }


# -------------------------------
# ADMIN: Create order with new product (and Cloudinary image)
# -------------------------------
@router.post("/admin/create-with-product", response_model=OrderRead)
async def create_order_with_product_admin(
    user_id: int = Form(...),
    address: str = Form(...),
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
        
    try:
        # 1. Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(file.file)
        image_url = upload_result.get("secure_url")
        
        # 2. Create Product
        new_product = Product(
            name=name,
            price=price,
            description=description,
            image_url=image_url,
            category_id=category_id,
            admin_id=current_user.id
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        # 3. Create Order
        new_order = Order(
            user_id=user_id,
            total_price=price, # Direct purchase of one item
            address=address,
            payment_method="Cash on Delivery",
            admin_id=current_user.id
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        # 4. Create OrderItem
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=new_product.id,
            fixed_price=price,
            quantity=1
        )
        db.add(order_item)
        db.commit()
        
        # Refresh and attach names for schema
        db.refresh(new_order)
        new_order.user_name = new_order.user.username
        new_order.admin_name = current_user.username
        
        return new_order
        
    except Exception as e:
        db.rollback()
        print(f"Error in admin order posting: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to post order: {str(e)}")




# @router.post("/create", response_model=OrderRead)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):

#     if not order.items:
#         raise HTTPException(status_code=400, detail="No items in order")

#     total_price = 0

#     for item in order.items:
#         product = db.query(Product).filter(Product.id == item.product_id).first()
#         if not product:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Product {item.product_id} not found"
#             )
#         total_price += product.price * item.quantity

   
#     new_order = Order(
#         user_id=order.user_id,
#         total_price=total_price
#     )
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)

#     order_items = []
#     for item in order.items:
#         product = db.query(Product).filter(Product.id == item.product_id).first()

#         order_item = OrderItem(
#             order_id=new_order.id,
#             product_id=item.product_id,
#             quantity=item.quantity,
#             price=product.price
#         )
#         db.add(order_item)
#         order_items.append(order_item)

#     db.commit()

#     new_order.items = order_items
#     return new_order




    



# @router.get("/user/{user_id}", response_model=List[OrderRead])
# def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
#     orders = db.query(Order).filter(Order.user_id == user_id).all()
#     return orders




# # Delete an order

# @router.delete("/delete/{order_id}")
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     db.delete(order)
#     db.commit()
#     return {"detail": "Order deleted successfully"}
