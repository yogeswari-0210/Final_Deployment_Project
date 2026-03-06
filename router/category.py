

from fastapi import APIRouter, Depends,Query,HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency.db_dependency import get_db
from models.category_models import Category
from schemas.categories_schemas import CategoryCreate, CategoryRead,CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
  
    # Treat 0 as None (root category) to handle frontend/default inputs
    if category.parent_id == 0:
        category.parent_id = None

    if category.parent_id:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category does not exist")

    try:
        new_category = Category(name=category.name, parent_id=category.parent_id)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as e:
        print(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/subcategories", response_model=List[CategoryRead])
def get_subcategories(db: Session = Depends(get_db)):
    """Return only sub-categories (categories with a parent)."""
    return db.query(Category).filter(Category.parent_id.isnot(None)).all()


# Get category by id

@router.get("/id/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# # Get category by name

# @router.get("/name/", response_model=List[CategoryRead])
# def get_category_by_name(name: str = Query(..., description="Name of category to search"), 
#                          db: Session = Depends(get_db)):
#     categories = db.query(Category).filter(Category.name.ilike(f"%{name}%")).all()
#     if not categories:
#         raise HTTPException(status_code=404, detail="No categories found with this name")
#     return categories




