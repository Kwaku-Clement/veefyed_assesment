import requests
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "secret-token-123"
HEADERS = {"X-API-Key": API_KEY}
TEST_IMAGE_NAME = "test_image.png"

def create_test_image():
    """Creates a dummy image file for testing"""
    print(f" Creating dummy image '{TEST_IMAGE_NAME}'...")
    # Create a small valid PNG header to pass validation
    # This is a 1x1 transparent PNG
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    with open(TEST_IMAGE_NAME, "wb") as f:
        f.write(png_data)

def test_flow():
    # 1. Check if server is running
    try:
        requests.get(BASE_URL)
    except requests.exceptions.ConnectionError:
        print("[ERROR] Server is not running.")
        print("  Please run: uvicorn app.main:app --reload")
        return

    # 2. Upload Image
    print("[INFO] Starting Upload...")
    try:
        with open(TEST_IMAGE_NAME, 'rb') as f:
            files = {'file': (TEST_IMAGE_NAME, f, 'image/png')}
            response = requests.post(f"{BASE_URL}/upload", files=files, headers=HEADERS)
            
        if response.status_code == 200:
            data = response.json()
            image_id = data.get("image_id")
            print(f"[SUCCESS] Upload Successful! Image ID: {image_id}")
        elif response.status_code == 403:
            print("[ERROR] Authentication Failed (403). Check your API Key.")
            return
        else:
            print(f"[ERROR] Upload Failed: {response.status_code} - {response.text}")
            return

    except Exception as e:
        print(f"[ERROR] An error occurred during upload: {e}")
        return

    # 3. Analyze Image
    print(f"\n[INFO] Analyzing Image {image_id}...")
    try:
        payload = {"image_id": image_id}
        response = requests.post(f"{BASE_URL}/analyze", json=payload, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()
            print("[SUCCESS] Analysis Complete!")
            print("-" * 30)
            print(f"Skin Type:  {result.get('skin_type')}")
            print(f"Issues:     {', '.join(result.get('issues', []))}")
            print(f"Confidence: {result.get('confidence')}")
            print("-" * 30)
        else:
            print(f"[ERROR] Analysis Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"[ERROR] An error occurred during analysis: {e}")

    # Cleanup
    if os.path.exists(TEST_IMAGE_NAME):
        os.remove(TEST_IMAGE_NAME)
        print(f"\n[INFO] Cleaned up {TEST_IMAGE_NAME}")

if __name__ == "__main__":
    create_test_image()
    test_flow()
