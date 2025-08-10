import requests
import time
import json

# Test the API locally
BASE_URL = "http://localhost:5000"

def test_api():
    print("Testing YouTube to MP3 Converter API")
    print("=" * 40)
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test API documentation
    print("\n2. Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"API docs: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"API docs failed: {e}")
    
    # Test video conversion (you can replace with a real YouTube URL)
    print("\n3. Testing video conversion...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
    
    try:
        response = requests.post(f"{BASE_URL}/api/convert", 
                               json={"url": test_url})
        print(f"Convert request: {response.status_code}")
        
        if response.status_code == 202:
            data = response.json()
            task_id = data.get('task_id')
            print(f"Task ID: {task_id}")
            
            # Poll for status
            print("Polling for status...")
            for i in range(10):  # Poll for up to 10 times
                time.sleep(5)  # Wait 5 seconds between polls
                
                status_response = requests.get(f"{BASE_URL}/api/status/{task_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Status: {status_data}")
                    
                    if status_data.get('status') == 'completed':
                        download_url = status_data.get('download_url')
                        print(f"Download URL: {BASE_URL}{download_url}")
                        break
                    elif status_data.get('status') == 'error':
                        print(f"Error: {status_data.get('message')}")
                        break
                else:
                    print(f"Status check failed: {status_response.status_code}")
        else:
            print(f"Convert request failed: {response.text}")
            
    except Exception as e:
        print(f"Convert test failed: {e}")

if __name__ == "__main__":
    test_api()
