import sys
import os

# Ensure backend dir is in path
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

def fix():
    session = SessionLocal()
    try:
        # 1. Check Category
        cat_name = "Dog Food"
        print(f"Checking '{cat_name}'...")
        cat = session.query(Category).filter(Category.name.ilike(cat_name)).first()
        
        if not cat:
            print("Category missing. Creating...")
            cat = Category(name=cat_name)
            session.add(cat)
            session.commit()
            session.refresh(cat)
        
        print(f"Category ID: {cat.id}, Name: {cat.name}")
        
        # 2. Check Products (Direct)
        count = session.query(Product).filter(Product.category_id == cat.id).count()
        print(f"Direct Product Count: {count}")
        
        if count == 0:
            print("Creating sample product...")
            p = Product(
                name="Premium Dog Food",
                price=199,
                description="Healthy food",
                image_url="https://via.placeholder.com/150",
                category_id=cat.id
            )
            session.add(p)
            session.commit()
            print("Product added.")
        
        # 3. Test API Query
        print("Testing API Query (Join)...")
        api_matches = session.query(Product).join(Category).filter(Category.name.ilike(f"%{cat_name}%")).all()
        print(f"API Query Match Count: {len(api_matches)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    fix()
