# from database.database import SessionLocal
# from models.category_models import Category
# from models.product_models import Product   # ✅ ADD THIS

from database.database import SessionLocal

# import ALL models so SQLAlchemy registers relationships
from models.user_models import User
from models.product_models import Product
from models.category_models import Category
from models.cart_models import Cart
from models.cart_items_models import CartItem
from models.wishlist_models import Wishlist
from models.order_models import Order
from models.order_items_models import OrderItem

db = SessionLocal()

# delete old categories
db.query(Category).delete()
db.commit()

# create parent categories
dogs = Category(name="Shop for Dogs", parent_id=None)
cats = Category(name="Shop for Cats", parent_id=None)

db.add_all([dogs, cats])
db.commit()
db.refresh(dogs)
db.refresh(cats)

# create subcategories
dog_food = Category(name="Dog Food", parent_id=dogs.id)
dog_toys = Category(name="Dog Toys", parent_id=dogs.id)

cat_food = Category(name="Cat Food", parent_id=cats.id)
cat_toys = Category(name="Cat Toys", parent_id=cats.id)

db.add_all([dog_food, dog_toys, cat_food, cat_toys])
db.commit()

db.close()

print("✅ Categories fixed successfully")