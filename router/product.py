from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
import cloudinary.uploader
from sqlalchemy.orm import Session
from typing import List

from dependency.db_dependency import get_db
from models.product_models import Product
from schemas.product_schemas import ProductCreate,ProductRead
from models.category_models import Category
from schemas.order_schemas import OrderRead
from models.order_models import Order
from models.user_models import User
from dependency.auth_dependency import get_current_user


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductRead)
def create_product(
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(None),
    category_id: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        upload_result = cloudinary.uploader.upload(file.file)
        image_url = upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Error: {e}")
        raise HTTPException(status_code=500, detail=f"Image Upload Failed: {str(e)}")

    new_product = Product(
        name=name,
        price=price,
        description=description,   
        image_url=image_url,       
        category_id=category_id,
        admin_id=current_user.id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

#get all product
@router.get("/", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()



#get product by id

@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


#get product by name
@router.get("/name/{product_name}", response_model=List[ProductRead])
def get_product_by_name(product_name: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.name.ilike(f"%{product_name}%")
    ).all()
    return products




@router.get("/category/{category_name}", response_model=List[ProductRead])
def get_products_by_category(
    category_name: str, 
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import aliased
    ParentCategory = aliased(Category)
    query = (
        db.query(Product)
        .join(Category)
        .outerjoin(ParentCategory, Category.parent)
        .filter(
            (Category.name.ilike(f"%{category_name}%")) |
            (ParentCategory.name.ilike(f"%{category_name}%"))
        )
    )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()
    if not products:
        raise HTTPException(status_code=404, detail=f"No products found for category '{category_name}'")
    return products


@router.get("/filter/strict", response_model=List[ProductRead])
def get_products_by_parent_and_child(
    category: str = Query(..., description="Parent category name (e.g. 'Shop for Dogs')"),
    subcategory: str = Query(..., description="Subcategory name (e.g. 'Food')"),
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
    db: Session = Depends(get_db)
):
    # We need to find products where:
    # Product.category.name ILIKE %subcategory%
    # AND Product.category.parent.name ILIKE %parent_category%
    
    # Alias for parent category to join twice
    from sqlalchemy.orm import aliased
    ParentCategory = aliased(Category)
    
    query = (
        db.query(Product)
        .join(Product.category)
        .join(ParentCategory, Category.parent)
        .filter(
            Category.name.ilike(f"%{subcategory}%"),
            ParentCategory.name.ilike(f"%{category}%")
        )
    )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()
    
    # If no results found with strict parent-child structure, 
    # fallback to just checking if the category name contains both? 
    # No, strict structure is better to avoid the contamination issue.
    
    if not products:
        # Fallback: Maybe the product is directly in the "Subcategory" but the parent linkage isn't perfect in DB?
        # Or maybe the "Subcategory" name in DB is "Dog Food" and user passed "Food".
        # Let's trust the join first.
        raise HTTPException(status_code=404, detail=f"No products found for {category} > {subcategory}")
        
    return products



@router.get("/filter/price", response_model=List[ProductRead])
def filter_products_by_price(
    min_price: float = Query(0),
    max_price: float = Query(100000),
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.price >= min_price,
        Product.price <= max_price
    ).all()
    return products




