import sys
import os
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from database.database import SessionLocal
from models.category_models import Category
from models.product_models import Product

def check_data():
    session = SessionLocal()
    try:
        print("\n--- Categories ---", flush=True)
        categories = session.query(Category).all()
        for cat in categories:
            parent_name = cat.parent.name if cat.parent else "None"
            print(f"ID: {cat.id}, Name: '{cat.name}', Parent: {parent_name}", flush=True)

        print("\n--- Products ---", flush=True)
        products = session.query(Product).all()
        for p in products:
            cat_name = p.category.name if p.category else "None"
            print(f"ID: {p.id}, Name: '{p.name}', Category: '{cat_name}'", flush=True)
            
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    check_data()
