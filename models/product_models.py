from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from database.database import Base
from models.cart_models import Cart
from models.cart_items_models import CartItem
from models.category_models import Category
from models.wishlist_models import Wishlist

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)  
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    image_url = Column(String, nullable=True)

    carts = relationship("Cart", back_populates="product", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan") 
    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete")

    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin = relationship("User")
