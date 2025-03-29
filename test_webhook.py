import os
import requests
from dotenv import load_dotenv
import sys

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Load environment variables
print("Loading environment variables...")
load_dotenv(verbose=True)

# Print all environment variables (excluding sensitive ones)
print("\nEnvironment variables:")
for key in os.environ:
    if 'SECRET' not in key and 'PASSWORD' not in key:
        print(f"{key}: {os.environ[key]}")

def test_webhook():
    webhook_url = os.getenv('N8N_WEBHOOK_URL')
    if not webhook_url:
        print("\nError: N8N_WEBHOOK_URL not found in .env file")
        print("Make sure:")
        print("1. The .env file exists in the current directory")
        print("2. The file contains N8N_WEBHOOK_URL=http://localhost:5678/webhook/test")
        print("3. There are no spaces around the '=' sign")
        print("4. The file is saved with UTF-8 encoding")
        return False
    
    print(f"\nTesting webhook URL: {webhook_url}")
    
    test_data = {
        "query": "Test connection",
        "timestamp": "2024-03-21T12:00:00Z"
    }
    
    try:
        print("\nSending POST request...")
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n=== N8N Webhook Test ===\n")
    success = test_webhook()
    if success:
        print("\nSuccessfully connected to n8n!")
    else:
        print("\nFailed to connect to n8n. Check the error messages above.") 