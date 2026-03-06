import sys
import os
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).parent.resolve()))

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine, Base
from models.category_models import Category
from models.product_models import Product

# Ensure tables exist
# Base.metadata.create_all(bind=engine) 

def seed_data():
    db = SessionLocal()
    try:
        print("Seeding data...")
        
        # 1. Ensure Categories Exist
        dogs_cat = db.query(Category).filter(Category.name == "Shop for Dogs").first()
        if not dogs_cat:
            print("Creating 'Shop for Dogs' category...")
            dogs_cat = Category(name="Shop for Dogs", parent_id=None)
            db.add(dogs_cat)
            db.commit()
            db.refresh(dogs_cat)
        
        cats_cat = db.query(Category).filter(Category.name == "Shop for Cats").first()
        if not cats_cat:
            print("Creating 'Shop for Cats' category...")
            cats_cat = Category(name="Shop for Cats", parent_id=None)
            db.add(cats_cat)
            db.commit()
            db.refresh(cats_cat)

        # 2. Add Dummy Products for Dogs
        dog_products = [
            {"name": "Dog Food Premium", "price": 1200, "description": "High quality food for dogs", "image_url": "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"},
            {"name": "Dog Leash", "price": 500, "description": "Strong durable leash", "image_url": "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"}
        ]

        for p_data in dog_products:
            exists = db.query(Product).filter(Product.name == p_data["name"]).first()
            if not exists:
                print(f"Creating product: {p_data['name']}")
                prod = Product(
                    name=p_data["name"],
                    price=p_data["price"],
                    description=p_data["description"],
                    image_url=p_data["image_url"],
                    category_id=dogs_cat.id
                )
                db.add(prod)
        
        # 3. Add Dummy Products for Cats
        cat_products = [
            {"name": "Cat Nip", "price": 200, "description": "Organic cat nip", "image_url": "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"},
            {"name": "Cat Scratcher", "price": 800, "description": "Cardboard scratcher", "image_url": "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg"}
        ]

        for p_data in cat_products:
            exists = db.query(Product).filter(Product.name == p_data["name"]).first()
            if not exists:
                print(f"Creating product: {p_data['name']}")
                prod = Product(
                    name=p_data["name"],
                    price=p_data["price"],
                    description=p_data["description"],
                    image_url=p_data["image_url"],
                    category_id=cats_cat.id
                )
                db.add(prod)

        db.commit()
        print("Seeding complete!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
