from models import User, Subscriber
import os

def test_user():
    print("\nTesting User Model:")
    # Create a new user
    user = User(
        username="testuser",
        email="test@example.com",
        password="testpassword123"
    )
    
    # Save the user
    if user.save():
        print("✓ User created successfully")
    
    # Find user by email
    found_user = User.find_by_email("test@example.com")
    if found_user and found_user.username == "testuser":
        print("✓ User found by email")
    
    # Test password verification
    if found_user.verify_password("testpassword123"):
        print("✓ Password verification works")
    
    # Test JWT token
    token = found_user.generate_token()
    if token and User.verify_token(token):
        print("✓ JWT token generation and verification works")

def test_subscriber():
    print("\nTesting Subscriber Model:")
    # Create a new subscriber
    subscriber = Subscriber(
        email="subscriber@example.com",
        name="Test Subscriber"
    )
    
    # Save the subscriber
    if subscriber.save():
        print("✓ Subscriber created successfully")
    
    # Find subscriber by email
    found_subscriber = Subscriber.find_by_email("subscriber@example.com")
    if found_subscriber and found_subscriber.email == "subscriber@example.com":
        print("✓ Subscriber found by email")
    
    # Test bulk subscribe
    test_emails = ["test1@example.com", "test2@example.com"]
    count = Subscriber.bulk_subscribe(test_emails)
    if count == 2:
        print("✓ Bulk subscribe works")
    
    # Test unsubscribe
    if found_subscriber.unsubscribe():
        print("✓ Unsubscribe works")

if __name__ == "__main__":
    # Install required packages
    os.system("pip install bcrypt PyJWT")
    
    print("Starting model tests...")
    test_user()
    test_subscriber()
    print("\nTests completed!") 