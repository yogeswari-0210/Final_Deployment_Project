import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def create_category():
    print("--- Create Category ---")
    name = input("Enter category name (e.g., Dog Food): ")
    
    # Optional parent_id
    parent_id_input = input("Enter parent category ID (optional, press Enter to skip): ")
    parent_id = int(parent_id_input) if parent_id_input else None

    payload = {
        "name": name,
        "parent_id": parent_id
    }

    try:
        response = requests.post(f"{BASE_URL}/categories/", json=payload)
        
        if response.status_code == 200:
            print("\n✅ Category created successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Failed to connect to server: {e}")

if __name__ == "__main__":
    create_category()
