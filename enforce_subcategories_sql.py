import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def enforce_subcategories():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Enforcing sub-categories via raw SQL...")

        # 1. Ensure Parent Categories
        cur.execute("SELECT id FROM categories WHERE name = 'Shop for Dogs' AND parent_id IS NULL;")
        dogs_parent = cur.fetchone()
        if not dogs_parent:
            cur.execute("INSERT INTO categories (name) VALUES ('Shop for Dogs') RETURNING id;")
            dogs_parent = cur.fetchone()
        
        cur.execute("SELECT id FROM categories WHERE name = 'Shop for Cats' AND parent_id IS NULL;")
        cats_parent = cur.fetchone()
        if not cats_parent:
            cur.execute("INSERT INTO categories (name) VALUES ('Shop for Cats') RETURNING id;")
            cats_parent = cur.fetchone()

        dogs_id = dogs_parent[0]
        cats_id = cats_parent[0]

        # 2. Required sub-categories
        required_subs = [
            ("dog food", dogs_id),
            ("dog toys", dogs_id),
            ("cat food", cats_id),
            ("cat toys", cats_id),
        ]

        for name, p_id in required_subs:
            cur.execute("SELECT id FROM categories WHERE name = %s;", (name,))
            sub = cur.fetchone()
            if not sub:
                print(f"Creating sub-category: {name}")
                cur.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s);", (name, p_id))
            else:
                print(f"Ensuring sub-category {name} has parent {p_id}")
                cur.execute("UPDATE categories SET parent_id = %s WHERE name = %s;", (p_id, name))

        conn.commit()
        cur.close()
        conn.close()
        print("Sub-categories enforced successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    enforce_subcategories()
