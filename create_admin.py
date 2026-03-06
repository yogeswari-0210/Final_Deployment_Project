import sys
from pathlib import Path

# Add the project root to the sys.path
# File is at backend/create_admin.py, root is at /
project_root = str(Path(__file__).parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import backend to ensure absolute imports work if handled that way
# But the structure seems to be relative within backend
backend_path = str(Path(__file__).parent.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from database.database import SessionLocal, engine, Base
from auth.hashing import Hash

# Import ALL models to ensure SQLAlchemy mappers are initialized
from models import (
    user_models,
    product_models,
    cart_models,
    cart_items_models,
    category_models,
    wishlist_models,
    order_models,
    order_items_models,
    offer_models
)

from models.user_models import User

def create_admin():
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin_email = "admin@petcare.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        
        if existing_admin:
            print(f"Admin with email {admin_email} already exists.")
            return

        admin_user = User(
            username="Admin",
            email=admin_email,
            password=Hash.bcrypt("admin123"),
            role="admin"
        )
        
        db.add(admin_user)
        db.commit()
        print(f"Admin user created successfully! Email: {admin_email}, Password: admin123")
    except Exception as e:
        print(f"Error creating admin: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
