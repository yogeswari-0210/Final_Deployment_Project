import sys
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).parent.resolve()))



from fastapi import FastAPI
from database.database import Base, engine
import cloudinary
from models import user_models, product_models
import dependency.cloudinary_config


from router.user import router as users
from router.product import router as products
from router.cart import router as cart
from router.category import router as categories
from router.wishlist import router as wishlist
from router.order import router as order
from router.search import router as search
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# ✅ Add CORS middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




from models import (
    user_models,
    product_models,
    cart_models,
    cart_items_models,
    category_models,
    wishlist_models,
    order_models,
    order_items_models
)

Base.metadata.create_all(bind=engine)

app.include_router(users)
app.include_router(products)
app.include_router(cart)
app.include_router(categories)
app.include_router(wishlist) 
app.include_router(order)
app.include_router(search, prefix="/search")


