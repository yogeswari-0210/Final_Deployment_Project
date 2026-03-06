import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Checking for admin_id in products table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='products' AND column_name='admin_id';")
        if not cur.fetchone():
            print("Adding admin_id to products...")
            cur.execute("ALTER TABLE products ADD COLUMN admin_id INTEGER REFERENCES users(id);")
        else:
            print("admin_id already exists in products.")

        print("Checking for admin_id in orders table...")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='orders' AND column_name='admin_id';")
        if not cur.fetchone():
            print("Adding admin_id to orders...")
            cur.execute("ALTER TABLE orders ADD COLUMN admin_id INTEGER REFERENCES users(id);")
        else:
            print("admin_id already exists in orders.")
            
        conn.commit()
        cur.close()
        conn.close()
        print("Migration successful!")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
