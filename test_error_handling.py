import requests
import os
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "secret-token-123"
HEADERS = {"X-API-Key": API_KEY}

def print_test_header(name):
    print(f"\n{'='*50}")
    print(f"TEST: {name}")
    print(f"{'='*50}")

def test_invalid_api_key():
    print_test_header("Invalid API Key")
    response = requests.get(f"{BASE_URL}/", headers={"X-API-Key": "wrong-key"})
    # Note: Root endpoint might be public depending on implementation, checking upload instead
    response = requests.post(f"{BASE_URL}/upload", headers={"X-API-Key": "wrong-key"})
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 403:
        print("[SUCCESS] Success: Correctly rejected invalid key")
    else:
        print("[ERROR] Failed: Should return 403")

def test_invalid_file_type():
    print_test_header("Invalid File Type (Text File)")
    
    # Create a dummy text file
    filename = "test.txt"
    with open(filename, "w") as f:
        f.write("This is not an image")
        
    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "Invalid file type" in response.json()["detail"]:
            print("[SUCCESS] Success: Correctly rejected invalid file type")
        else:
            print("[ERROR] Failed: Should return 400 with 'Invalid file type'")
            
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def test_fake_image_content():
    print_test_header("Fake Image Content (Magic Number Check)")
    
    # Create a file named .jpg but with text content
    filename = "fake.jpg"
    with open(filename, "w") as f:
        f.write("This is definitely not a JPEG image")
        
    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "Invalid file content" in response.json()["detail"]:
            print("[SUCCESS] Success: Correctly rejected fake image content")
        else:
            print("[ERROR] Failed: Should return 400 with 'Invalid file content'")
            
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def test_missing_image_id():
    print_test_header("Missing/Unknown Image ID")
    
    unknown_id = "non_existent_id_123"
    payload = {"image_id": unknown_id}
    
    response = requests.post(f"{BASE_URL}/analyze", headers=HEADERS, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 404 and "not found" in response.json()["detail"]:
        print("[SUCCESS] Success: Correctly handled unknown image ID")
    else:
        print("[ERROR] Failed: Should return 404 for unknown ID")

def test_large_file():
    print_test_header("File Too Large (>5MB)")
    
    # Create a large dummy file (5MB + 1 byte)
    filename = "large_test.jpg"
    size = 5 * 1024 * 1024 + 1
    
    with open(filename, "wb") as f:
        f.seek(size - 1)
        f.write(b"\0")
        
    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)
            
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400 and "File too large" in response.json()["detail"]:
            print("[SUCCESS] Success: Correctly rejected large file")
        else:
            print("[ERROR] Failed: Should return 400 for large file")
            
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    try:
        # Check if server is running
        requests.get(BASE_URL)
        
        test_invalid_api_key()
        test_invalid_file_type()
        test_fake_image_content()
        test_missing_image_id()
        test_large_file()
        
    except requests.exceptions.ConnectionError:
        print("[ERROR] Error: Server is not running.")
        print("   Please run: uvicorn app.main:app --reload")
