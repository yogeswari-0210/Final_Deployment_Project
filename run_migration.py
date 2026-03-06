from sqlalchemy import text
from database.database import engine

def migrate():
    with engine.connect() as conn:
        print("Adding 'address' column...")
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN address VARCHAR"))
            print("Successfully added 'address'")
        except Exception as e:
            print(f"'address' column might already exist or error: {e}")
            
        print("Adding 'payment_method' column...")
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR"))
            print("Successfully added 'payment_method'")
        except Exception as e:
            print(f"'payment_method' column might already exist or error: {e}")
            
        conn.commit()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
