import requests
import json

def check_status(task_id):
    response = requests.get(f"http://localhost:5000/api/status/{task_id}")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    # Print the full error message
    if 'data' in data and 'message' in data['data']:
        print(f"\nFull error message: {data['data']['message']}")

if __name__ == "__main__":
    check_status("1e049b71-9461-4ed5-bf79-036f2fd00f16")
