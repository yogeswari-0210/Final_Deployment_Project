
from database.database import Base, engine

from models.user_models import User
from models.product_models import Product
from models.category_models import Category
from models.cart_models import Cart
from models.cart_items_models import CartItem
from models.wishlist_models import Wishlist
from models.order_models import Order
from models.order_items_models import OrderItem

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating fresh tables...")
Base.metadata.create_all(bind=engine)

print("Done! All tables cleared and recreated.")
