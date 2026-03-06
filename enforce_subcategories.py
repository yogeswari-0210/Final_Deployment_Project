import sys
import os
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.category_models import Category

def enforce_subcategories():
    db = SessionLocal()
    try:
        print("Enforcing sub-categories...")
        
        # 1. Ensure Parent Categories Exist
        dogs_parent = db.query(Category).filter(Category.name == "Shop for Dogs").first()
        if not dogs_parent:
            dogs_parent = Category(name="Shop for Dogs", parent_id=None)
            db.add(dogs_parent)
            db.commit()
            db.refresh(dogs_parent)
        
        cats_parent = db.query(Category).filter(Category.name == "Shop for Cats").first()
        if not cats_parent:
            cats_parent = Category(name="Shop for Cats", parent_id=None)
            db.add(cats_parent)
            db.commit()
            db.refresh(cats_parent)

        # 2. Define required sub-categories
        required_subs = [
            {"name": "dog food", "parent_id": dogs_parent.id},
            {"name": "dog toys", "parent_id": dogs_parent.id},
            {"name": "cat food", "parent_id": cats_parent.id},
            {"name": "cat toys", "parent_id": cats_parent.id},
        ]

        for sub_data in required_subs:
            sub = db.query(Category).filter(Category.name == sub_data["name"]).first()
            if not sub:
                print(f"Creating sub-category: {sub_data['name']}")
                sub = Category(name=sub_data["name"], parent_id=sub_data["parent_id"])
                db.add(sub)
            else:
                # Ensure correct parent
                sub.parent_id = sub_data["parent_id"]
        
        db.commit()
        print("Sub-categories enforced!")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error enforcing sub-categories: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    enforce_subcategories()
