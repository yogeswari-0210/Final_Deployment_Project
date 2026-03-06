from sqlalchemy import text
from database.database import engine

def add_status_column():
    with engine.connect() as conn:
        print("Attempting to add 'status' column...")
        try:
            conn.execute(text("ALTER TABLE orders ADD COLUMN status VARCHAR DEFAULT 'Ordered'"))
            conn.commit()
            print("Successfully added 'status' column")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    add_status_column()
