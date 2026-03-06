from auth.jwt import create_access_token
from auth.hashing import Hash


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependency.db_dependency import get_db
from dependency.auth_dependency import get_current_user
from models.user_models import User
from schemas.users_schemas import UserCreate , UserLogin,UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# #  get all users
# @router.get("/", response_model=List[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(User).all()

# #  get user by ID
# @router.get("/{user_id}", response_model=UserResponse)
# def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


#  signup
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    try:
        new_user = User(
            username=user.username,
            email=user.email,
            password=Hash.bcrypt(user.password),
            role=user.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print(f"Signup Error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Auto-login: return token
    token = create_access_token(data={"sub": new_user.email, "user_id": new_user.id})
    return {
        "message": "Signup successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "username": new_user.username,
        "role": new_user.role
    }




@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not Hash.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 🔑 Create JWT token
    token = create_access_token(data={"sub": db_user.email, "user_id": db_user.id})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user.id,
        "username": db_user.username,
        "role": db_user.role
    }


# @router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(
#         User.email == user.email,
#         User.password == user.password
#     ).first()

#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     return {
#         "message": "Login successful",
#         "user_id": db_user.id,
#         "username": db_user.username
#     }





# # Signup route (optional)
# @router.post("/signup", response_model=UserResponse)
# def signup(user: UserLogin, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = User(
#         username=user.username,
#         email=user.email,
#         password=user.password
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# # Login route
# @router.post("/login")
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     print("Login attempt:", user.email, user.password)  # debug

#     db_user = db.query(User).filter(
#         User.email == user.email,
#         User.password == user.password
#     ).first()

#     if not db_user:
#         print("Login failed")
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     print("Login successful:", db_user.username)
#     return {
#         "message": "Login successful",
#         "user_id": db_user.id,
#         "username": db_user.username
#     }
