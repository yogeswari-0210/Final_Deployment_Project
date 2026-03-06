from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.category_models import Category
from models.product_models import Product

def seed_products():
    db: Session = SessionLocal()
    try:
        categories = ["Dog Food", "Cat Food", "Dog Toys", "Cat Toys"]
        
        for cat_name in categories:
            # 1. Get Category ID
            category = db.query(Category).filter(Category.name == cat_name).first()
            if not category:
                print(f"Creating missing category: {cat_name}")
                category = Category(name=cat_name)
                db.add(category)
                db.commit()
                db.refresh(category)
            
            # 2. Check if products exist
            count = db.query(Product).filter(Product.category_id == category.id).count()
            if count == 0:
                print(f"Seeding product for {cat_name}...")
                # Create a specific product for this category
                name = f"Sample {cat_name} Product"
                desc = f"Best quality {cat_name}"
                img = "https://via.placeholder.com/150"
                
                prod = Product(
                    name=name,
                    price=250,
                    description=desc,
                    image_url=img,
                    category_id=category.id
                )
                db.add(prod)
                db.commit()
                print(f"Added '{name}'")
            else:
                print(f"Category '{cat_name}' already has {count} products.")

    except Exception as e:
        print(f"Error seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_products()
