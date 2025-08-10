import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000"
    
    # Test health check first
    print("Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test convert endpoint with the specific YouTube URL
    print("\nTesting convert endpoint...")
    test_url = "https://www.youtube.com/watch?v=ZKWndx83RwQ"
    
    try:
        response = requests.post(
            f"{base_url}/api/convert",
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Convert status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 202:
            data = response.json()
            task_id = data.get('task_id')
            print(f"Task ID: {task_id}")
            
            # Poll for status
            print("\nPolling for status...")
            for i in range(10):
                time.sleep(3)
                
                status_response = requests.get(f"{base_url}/api/status/{task_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Status: {status_data}")
                    
                    if status_data.get('data', {}).get('status') == 'completed':
                        print("✅ Conversion completed successfully!")
                        break
                    elif status_data.get('data', {}).get('status') == 'error':
                        print(f"❌ Conversion failed: {status_data.get('data', {}).get('message')}")
                        break
                else:
                    print(f"Status check failed: {status_response.status_code}")
        else:
            print(f"❌ Convert request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_api()
