import urllib.request
import json
import random

BASE_URL = "http://127.0.0.1:8000"
ASSETS_DIR = "c:/fullstack-gravity1/frontend/assets"

def get_or_create_category(name):
    # 1. Check if exists
    try:
        with urllib.request.urlopen(f"{BASE_URL}/categories/") as response:
            if response.getcode() == 200:
                categories = json.loads(response.read().decode())
                for cat in categories:
                    if cat['name'].lower() == name.lower():
                        print(f"Category '{name}' already exists (ID: {cat['id']})")
                        return cat['id']
    except Exception as e:
        print(f"Error checking categories: {e}")

    # 2. Create if not exists
    print(f"Creating category '{name}'...")
    data = json.dumps({"name": name, "parent_id": None}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/categories/", data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                cat = json.loads(response.read().decode())
                print(f"Created category '{name}' (ID: {cat['id']})")
                return cat['id']
    except Exception as e:
        print(f"Failed to create category '{name}': {e}")
        return None

def create_product(name, price, description, category_id, image_filename):
    print(f"Creating product '{name}'...")
    
    try:
        with open(f"{ASSETS_DIR}/{image_filename}", "rb") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: Image text_file '{image_filename}' not found.")
        return

    # Construct multipart form data manually
    boundary = '---BOUNDARYString' + str(random.randint(100000, 999999))
    lines = []
    
    lines.append('--' + boundary)
    lines.append('Content-Disposition: form-data; name="name"')
    lines.append('')
    lines.append(name)
    
    lines.append('--' + boundary)
    lines.append('Content-Disposition: form-data; name="price"')
    lines.append('')
    lines.append(str(price))
    
    lines.append('--' + boundary)
    lines.append('Content-Disposition: form-data; name="description"')
    lines.append('')
    lines.append(description)
    
    lines.append('--' + boundary)
    lines.append('Content-Disposition: form-data; name="category_id"')
    lines.append('')
    lines.append(str(category_id))
    
    lines.append('--' + boundary)
    lines.append(f'Content-Disposition: form-data; name="file"; filename="{image_filename}"')
    lines.append('Content-Type: image/jpeg') # Simplified content type
    lines.append('')
    
    # We need to construct the body as bytes
    # Separate text parts and file part
    
    body_parts = []
    for line in lines:
        body_parts.append(line.encode('utf-8'))
        body_parts.append(b'\r\n')
    
    # Add file content
    body_parts.append(file_content)
    body_parts.append(b'\r\n')
    
    # End boundary
    body_parts.append(('--' + boundary + '--').encode('utf-8'))
    body_parts.append(b'\r\n')
    
    body = b''.join(body_parts)
    
    req = urllib.request.Request(f"{BASE_URL}/products/", data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('Content-Length', len(body))
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                print(f"Successfully created product '{name}'")
    except Exception as e:
        try:
             err_body = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
             print(f"Failed to create product '{name}': {e} - {err_body}")
        except:
             print(f"Failed to verify product creation '{name}': {e}")

def seed():
    print("Starting API seed...")
    
    # 1. Categories
    dog_cat_id = get_or_create_category("shop for dogs")
    cat_cat_id = get_or_create_category("shop for cats")
    
    if dog_cat_id:
        create_product("Premium Dog Food", 1500, "Healthy food for your dog", dog_cat_id, "dog_food.png")
        create_product("Dog Bone Toy", 300, "Durable bone toy", dog_cat_id, "pro3.png")
        create_product("Dog Leash", 500, "Strong leash", dog_cat_id, "belt.png")
        
    if cat_cat_id:
        create_product("Cat Scratcher", 800, "Cardboard scratcher", cat_cat_id, "CAT.png")
        create_product("Cat Nip", 250, "Organic cat nip", cat_cat_id, "cat_food.png")
        create_product("Fish Toy", 150, "Interactive fish", cat_cat_id, "brush.png")

    print("Seeding finished.")

if __name__ == "__main__":
    seed()
