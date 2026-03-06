import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def get_json(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def check_api():
    print("--- Categories ---")
    categories = get_json(f"{BASE_URL}/categories/")
    if categories:
        for cat in categories:
            print(f"ID: {cat['id']} | Name: '{cat['name']}' | ParentID: {cat.get('parent_id')}")
            
    print("\n--- Products in 'Shop for Dogs' ---")
    dogs_products = get_json(f"{BASE_URL}/products/category/Shop%20for%20Dogs")
    if dogs_products:
        print(f"Count: {len(dogs_products)}")
        for p in dogs_products:
            print(f" - {p['name']} (Category ID: {p.get('category_id')})")
    else:
        print("No products or error.")

    print("\n--- Products in 'Dog Food' ---")
    dog_food_products = get_json(f"{BASE_URL}/products/category/Dog%20Food")
    if dog_food_products:
        print(f"Count: {len(dog_food_products)}")
        for p in dog_food_products:
            print(f" - {p['name']}")
    else:
        print("No products or error (expected if not populated yet).")

    print("\n--- Products in 'Dog Toys' ---")
    dog_toys_products = get_json(f"{BASE_URL}/products/category/Dog%20Toys")
    if dog_toys_products:
        print(f"Count: {len(dog_toys_products)}")
    else:
        print("No products or error.")

if __name__ == "__main__":
    check_api()
