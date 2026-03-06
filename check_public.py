import urllib.request

try:
    resp = urllib.request.urlopen("http://127.0.0.1:8000/products/")
    print(f"Status: {resp.getcode()}")
except Exception as e:
    print(f"Error: {e}")
