import requests
import json
import time

def test_specific_url():
    base_url = "https://ytmp3new-production.up.railway.app"
    test_url = "https://www.youtube.com/watch?v=Zhz0GeWgvWs"
    
    print(f"Testing API with URL: {test_url}")
    print("=" * 50)
    
    # Test the convert endpoint
    try:
        response = requests.post(
            f"{base_url}/api/convert",
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 202:
            data = response.json()
            task_id = data.get('task_id')
            print(f"\n✅ Conversion started successfully!")
            print(f"Task ID: {task_id}")
            
            # Poll for status
            print("\nPolling for status...")
            for i in range(10):
                time.sleep(3)
                
                status_response = requests.get(f"{base_url}/api/status/{task_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Status: {status_data.get('data', {}).get('status')}")
                    
                    if status_data.get('data', {}).get('status') == 'completed':
                        print("✅ Conversion completed!")
                        download_url = status_data.get('data', {}).get('download_url')
                        if download_url:
                            full_download_url = f"{base_url}{download_url}"
                            print(f"Download URL: {full_download_url}")
                        break
                    elif status_data.get('data', {}).get('status') == 'error':
                        print(f"❌ Conversion failed: {status_data.get('data', {}).get('message')}")
                        break
                else:
                    print(f"Status check failed: {status_response.status_code}")
        else:
            print(f"❌ Conversion failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_specific_url()
