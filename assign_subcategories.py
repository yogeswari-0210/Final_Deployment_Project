import sys
import os
from pathlib import Path
import requests

# Add backend folder to Python path
sys.path.append(str(Path(__file__).parent.resolve()))

BASE_URL = "http://127.0.0.1:8000"

def assign_products():
    print("Fetching categories...")
    try:
        cats = requests.get(f"{BASE_URL}/categories/").json()
        cat_map = {c["name"].lower(): c["id"] for c in cats}
        
        # Mapping: Product Name -> Target Category Name
        assignments = {
            "Dog Food Premium": "dogs Food",
            "Dog Leash": "dogs Toys",
            "Cat Nip": "cats food", 
            "Cat Scratcher": "cats Toys"
        }

        print("Fetching products...")
        all_products = requests.get(f"{BASE_URL}/products/").json()
        
        for p in all_products:
            p_name = p["name"]
            # Find if this product needs reassignment
            target_cat_name = None
            for key in assignments:
                if key in p_name: # Simple substring match or exact match
                    target_cat_name = assignments[key]
                    break
            
            if target_cat_name:
                target_cat_id = cat_map.get(target_cat_name.lower())
                if target_cat_id:
                    print(f"Reassigning '{p_name}' (ID: {p['id']}) to '{target_cat_name}' (ID: {target_cat_id})...")
                    # We need a way to update the product. 
                    # If there's no update endpoint, we might need direct DB access or create a new one.
                    # Checking product.py... there doesn't seem to be an update endpoint in the file I viewed earlier.
                    # using direct DB access for this fix script to be safe.
                    update_via_db(p['id'], target_cat_id)
                else:
                    print(f"Target category '{target_cat_name}' not found!")
            else:
                 print(f"Skipping '{p_name}' (no assignment rule)")

    except Exception as e:
        print(f"Error: {e}")

def update_via_db(product_id, category_id):
    from database.database import SessionLocal
    from models.product_models import Product
    
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.category_id = category_id
            db.commit()
            print("✅ Updated successfully.")
        else:
            print("❌ Product not found in DB.")
    except Exception as e:
        print(f"❌ DB Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    assign_products()
