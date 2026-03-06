import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))

from database.database import Base, engine
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

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
