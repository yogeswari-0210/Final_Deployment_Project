from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List

from dependency.db_dependency import get_db
from models.product_models import Product
from models.category_models import Category
from schemas.product_schemas import ProductRead

router = APIRouter(
    tags=["Search"]
)

@router.get("/", response_model=List[ProductRead])
def search_products(
    q: str = Query("", description="Search query for product name, category, or subcategory"),
    db: Session = Depends(get_db)
):
    print(f"SEARCH ROUTE HIT with q={q}")
    """
    Unified search endpoint for product name, category, and subcategory (case-insensitive).
    Returns all products if query is empty.
    """
    # If query is empty, return all products
    if not q or q.strip() == "":
        return db.query(Product).all()
    
    # Alias for parent category
    ParentCategory = aliased(Category)
    
    # Search across product name, category name, and parent category name
    products = (
        db.query(Product)
        .outerjoin(Category, Product.category)
        .outerjoin(ParentCategory, Category.parent)
        .filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Category.name.ilike(f"%{q}%"),
                ParentCategory.name.ilike(f"%{q}%")
            )
        )
        .distinct()
        .all()
    )
    
    return products
