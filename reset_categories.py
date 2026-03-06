import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def reset_categories():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Cleaning up categories...")

        # 1. Delete all products first or update them to a temporary category?
        # Actually, let's just delete all categories that aren't the ones we want.
        # But products might be linked.
        
        # Strategy: 
        # A. Rename the ones we want to keep to a unique name temporarily
        # B. Delete ALL categories
        # C. Re-insert the 4 required ones and parents
        
        # Actually simpler:
        cur.execute("DELETE FROM products;")
        cur.execute("DELETE FROM categories CASCADE;")
        
        # 2. Insert Parents
        cur.execute("INSERT INTO categories (name) VALUES ('Shop for Dogs') RETURNING id;")
        dogs_parent_id = cur.fetchone()[0]
        
        cur.execute("INSERT INTO categories (name) VALUES ('Shop for Cats') RETURNING id;")
        cats_parent_id = cur.fetchone()[0]

        # 3. Insert required sub-categories (EXACT names)
        required_subs = [
            ("dog food", dogs_parent_id),
            ("dog toys", dogs_parent_id),
            ("cat food", cats_parent_id),
            ("cat toys", cats_parent_id),
        ]

        for name, p_id in required_subs:
            print(f"Creating required sub-category: {name}")
            cur.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s);", (name, p_id))

        conn.commit()
        cur.close()
        conn.close()
        print("Categories reset to exactly 4 sub-categories and 2 parents.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_categories()
