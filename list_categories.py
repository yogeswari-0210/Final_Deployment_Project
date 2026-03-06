import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def get_categories():
    try:
        with urllib.request.urlopen(f"{BASE_URL}/categories/") as response:
            categories = json.loads(response.read().decode())
            print(f"Found {len(categories)} categories:")
            for cat in categories:
                print(f"ID: {cat['id']} | Name: '{cat['name']}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_categories()
