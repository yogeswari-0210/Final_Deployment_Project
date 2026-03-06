from sqlalchemy import text
from database.database import engine

def migrate():
    with engine.connect() as conn:
        print("Checking for missing columns in 'orders' table...")
        
        columns_to_add = [
            ("address", "VARCHAR"),
            ("payment_method", "VARCHAR"),
            ("status", "VARCHAR"),
            ("created_at", "TIMESTAMP")
        ]
        
        for col_name, col_type in columns_to_add:
            print(f"Adding '{col_name}' column...")
            try:
                conn.execute(text(f"ALTER TABLE orders ADD COLUMN {col_name} {col_type}"))
                print(f"Successfully added '{col_name}'")
            except Exception as e:
                if "already exists" in str(e).lower():
                    print(f"'{col_name}' column already exists.")
                else:
                    print(f"Error adding '{col_name}': {e}")
            
        conn.commit()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
