import requests
import json
import time

BASE_URL = 'http://localhost:4000'

def wait_for_server(max_retries=5):
    print("Waiting for server to start...")
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.ConnectionError:
            print(f"Attempt {i+1}/{max_retries}: Server not ready yet...")
            time.sleep(2)
    return False

def test_health():
    print("\nTesting health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_auth_endpoints():
    print("\nTesting authentication endpoints...")
    
    # Test signup with valid data
    print("\nTesting signup with valid data...")
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Test123!"
    }
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test signup with existing email
    print("\nTesting signup with existing email...")
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test login with valid credentials
    print("\nTesting login with valid credentials...")
    login_data = {
        "email": "test@example.com",
        "password": "Test123!"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Store token for protected endpoints
    token = response.json().get('token')
    
    # Test login with invalid password
    print("\nTesting login with invalid password...")
    login_data["password"] = "WrongPassword"
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test profile endpoint with valid token
    print("\nTesting profile endpoint with valid token...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test profile endpoint without token
    print("\nTesting profile endpoint without token...")
    response = requests.get(f"{BASE_URL}/api/auth/profile")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_subscriber_endpoints():
    print("\nTesting subscriber endpoints...")
    
    # Test subscribe with valid data
    print("\nTesting subscribe with valid data...")
    subscribe_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/api/subscribers/subscribe", json=subscribe_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test subscribe with invalid email
    print("\nTesting subscribe with invalid email...")
    subscribe_data["email"] = "invalid-email"
    response = requests.post(f"{BASE_URL}/api/subscribers/subscribe", json=subscribe_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test subscribe with missing email
    print("\nTesting subscribe with missing email...")
    subscribe_data = {"name": "Test User"}
    response = requests.post(f"{BASE_URL}/api/subscribers/subscribe", json=subscribe_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test unsubscribe with valid email
    print("\nTesting unsubscribe with valid email...")
    unsubscribe_data = {
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/api/subscribers/unsubscribe", json=unsubscribe_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test unsubscribe with non-existent email
    print("\nTesting unsubscribe with non-existent email...")
    unsubscribe_data["email"] = "nonexistent@example.com"
    response = requests.post(f"{BASE_URL}/api/subscribers/unsubscribe", json=unsubscribe_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_form_endpoints():
    print("\nTesting form endpoints...")
    
    # Test form submission with valid data
    print("\nTesting form submission with valid data...")
    form_data = {
        "form_type": "contact",
        "data": {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Test message"
        }
    }
    response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test form submission with missing form_type
    print("\nTesting form submission with missing form_type...")
    form_data = {
        "data": {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Test message"
        }
    }
    response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test form submission with missing data
    print("\nTesting form submission with missing data...")
    form_data = {
        "form_type": "contact"
    }
    response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test form submission with invalid form type
    print("\nTesting form submission with invalid form type...")
    form_data = {
        "form_type": "invalid_type",
        "data": {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Test message"
        }
    }
    response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test form submission with missing required fields
    print("\nTesting form submission with missing required fields...")
    form_data = {
        "form_type": "contact",
        "data": {
            "name": "Test User"
        }
    }
    response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_rate_limiting():
    print("\nTesting rate limiting...")
    
    # Test health endpoint rate limit (30 per minute)
    print("\nTesting health endpoint rate limit (30 per minute)...")
    responses = []
    for i in range(35):  # Try to exceed the limit
        response = requests.get(f"{BASE_URL}/health")
        responses.append(response.status_code)
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print(f"Rate limit hit! Response: {response.json()}")
            break
        time.sleep(0.1)  # Small delay between requests
    
    # Test auth endpoints rate limit
    print("\nTesting auth endpoints rate limit...")
    signup_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "Test123!"
    }
    responses = []
    for i in range(6):  # Assuming limit is 5 per minute
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        responses.append(response.status_code)
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print(f"Rate limit hit! Response: {response.json()}")
            break
        time.sleep(0.1)
    
    # Test form submission rate limit
    print("\nTesting form submission rate limit...")
    form_data = {
        "form_type": "contact",
        "data": {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Test message"
        }
    }
    responses = []
    for i in range(6):  # Assuming limit is 5 per minute
        response = requests.post(f"{BASE_URL}/api/forms/submit", json=form_data)
        responses.append(response.status_code)
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print(f"Rate limit hit! Response: {response.json()}")
            break
        time.sleep(0.1)

if __name__ == "__main__":
    print("Starting API tests...")
    if not wait_for_server():
        print("Failed to connect to server. Make sure the server is running on port 4000.")
        exit(1)
    
    test_health()
    test_auth_endpoints()
    test_subscriber_endpoints()
    test_form_endpoints()
    test_rate_limiting() 