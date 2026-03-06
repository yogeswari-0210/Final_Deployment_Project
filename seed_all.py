import sys
import os

sys.path.append(os.getcwd())

from database.database import SessionLocal
from models.category_models import Category
from models.product_models import Product
from models.user_models import User
from models.cart_models import Cart
from models.cart_items_models import CartItem
from models.order_models import Order
from models.wishlist_models import Wishlist
from models.order_items_models import OrderItem

def seed_all():
    session = SessionLocal()
    try:
        # Define categories to ensure/seed
        categories = [
            {"name": "Dog Toys", "prod": "Squeaky Bone", "img": "../assets/brush.png"},
            {"name": "Cat Food", "prod": "Tuna Delight", "img": "../assets/cat_food.png"},
            {"name": "Cat Toys", "prod": "Feather Wand", "img": "../assets/brush.png"},
            {"name": "Dog Food", "prod": "Premium Kibble", "img": "../assets/drool_food.png"}
        ]

        for cat_info in categories:
            cat_name = cat_info["name"]
            print(f"Checking '{cat_name}'...")
            
            # Find or Create Category
            cat = session.query(Category).filter(Category.name.ilike(cat_name)).first()
            if not cat:
                print(f"  Creating Category '{cat_name}'...")
                cat = Category(name=cat_name)
                session.add(cat)
                session.commit()
                session.refresh(cat)
            
            # Check Products
            count = session.query(Product).filter(Product.category_id == cat.id).count()
            if count == 0:
                print(f"  No products in '{cat_name}'. Creating sample...")
                p = Product(
                    name=cat_info["prod"],
                    price=299,
                    description=f"Best {cat_name} for your pet",
                    image_url=cat_info["img"],
                    category_id=cat.id
                )
                session.add(p)
                session.commit()
                print("  Product created.")
            else:
                print(f"  OK: Found {count} products.")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    seed_all()
