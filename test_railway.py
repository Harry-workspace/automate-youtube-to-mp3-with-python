import requests
import json
import time

def test_railway_api():
    base_url = "https://ytmp3new-production.up.railway.app"
    
    print("Testing Railway API Deployment")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: API info
    print("\n2. Testing API info...")
    try:
        response = requests.get(f"{base_url}/api/info")
        print(f"API info status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API info endpoint working")
        else:
            print(f"❌ API info failed: {response.text}")
    except Exception as e:
        print(f"❌ API info error: {e}")
    
    # Test 3: Convert endpoint
    print("\n3. Testing convert endpoint...")
    test_url = "https://www.youtube.com/watch?v=ZKWndx83RwQ"
    
    try:
        response = requests.post(
            f"{base_url}/api/convert",
            json={"url": test_url},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Convert status: {response.status_code}")
        if response.status_code == 202:
            print("✅ Convert endpoint working")
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            task_id = data.get('task_id')
            if task_id:
                print(f"Task ID: {task_id}")
                
                # Test 4: Status endpoint
                print("\n4. Testing status endpoint...")
                status_response = requests.get(f"{base_url}/api/status/{task_id}")
                print(f"Status check: {status_response.status_code}")
                if status_response.status_code == 200:
                    print("✅ Status endpoint working")
                    status_data = status_response.json()
                    print(f"Status: {json.dumps(status_data, indent=2)}")
                else:
                    print(f"❌ Status check failed: {status_response.text}")
        else:
            print(f"❌ Convert failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Convert error: {e}")
    
    # Test 5: Web interface
    print("\n5. Testing web interface...")
    try:
        response = requests.get(f"{base_url}/web")
        print(f"Web interface status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Web interface working")
        else:
            print(f"❌ Web interface failed: {response.text}")
    except Exception as e:
        print(f"❌ Web interface error: {e}")

if __name__ == "__main__":
    test_railway_api()
