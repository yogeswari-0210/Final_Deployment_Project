from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.user_models import User
from auth.hashing import Hash

def check_users():
    db = SessionLocal()
    try:
        print("\n--- USERS ---")
        users = db.query(User).all()
        admin_exists = False
        user_exists = False
        
        for user in users:
            print(f"ID: {user.id}, Username: '{user.username}', Role: '{user.role}', Email: '{user.email}'")
            if user.role == "admin":
                admin_exists = True
            if user.role == "user":
                user_exists = True
        
        if not admin_exists:
            print("\nCreating Admin User...")
            admin = User(
                username="admin",
                email="admin@example.com",
                password=Hash.bcrypt("admin123"),
                role="admin",
                phone_number="1234567890"
            )
            db.add(admin)
            db.commit()
            print("Admin created: admin@example.com / admin123")
            
        if not user_exists:
            print("\nCreating Test User...")
            user = User(
                username="testuser",
                email="test@example.com",
                password=Hash.bcrypt("password123"),
                role="user",
                phone_number="0987654321"
            )
            db.add(user)
            db.commit()
            print("User created: test@example.com / password123")

    finally:
        db.close()

if __name__ == "__main__":
    check_users()
