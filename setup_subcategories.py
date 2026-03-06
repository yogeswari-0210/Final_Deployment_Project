import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def setup_categories():
    categories_to_ensure = [
        {"name": "Dog Food", "parent_name": "shop for dogs"},
        {"name": "Dog Toys", "parent_name": "shop for dogs"},
        {"name": "Cat Food", "parent_name": "shop for cats"},
        {"name": "Cat Toys", "parent_name": "shop for cats"}
    ]

    # 1. Get existing categories to find parent IDs
    print("Fetching existing categories...")
    try:
        response = requests.get(f"{BASE_URL}/categories/")
        if response.status_code != 200:
            print("Failed to fetch categories")
            return
        
        existing_cats = response.json()
        cat_map = {c["name"].lower(): c["id"] for c in existing_cats}
        
        # Helper to create if not exists
        for item in categories_to_ensure:
            name = item["name"]
            parent_name = item["parent_name"]
            
            # Check if exists
            if name.lower() in cat_map:
                print(f"✅ Category '{name}' already exists.")
                continue

            # Need parent ID
            parent_id = cat_map.get(parent_name.lower())
            if not parent_id:
                print(f"⚠️ Parent '{parent_name}' not found. Creating top-level '{name}' instead (or fix parent first).")
                parent_id = None # Or handle parent creation
            
            print(f"Creating '{name}' (Parent ID: {parent_id})...")
            payload = {
                "name": name,
                "parent_id": parent_id
            }
            res = requests.post(f"{BASE_URL}/categories/", json=payload)
            if res.status_code == 200:
                print(f"✅ Created '{name}'.")
            else:
                print(f"❌ Failed to create '{name}': {res.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_categories()
