from db_client import MongoDBClient
from pprint import pprint

def test_mongodb_operations():
    # Initialize the MongoDB client
    db = MongoDBClient()
    
    try:
        # 1. Create a collection for users
        collection_name = "users"
        print("\n1. Creating users collection...")
        try:
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created successfully")
        except Exception as e:
            print(f"Collection might already exist: {e}")

        # 2. Insert a test user
        test_user = {
            "username": "test_user",
            "email": "test@example.com",
            "profile": {
                "first_name": "Test",
                "last_name": "User",
                "age": 25
            },
            "active": True
        }
        
        print("\n2. Creating test user...")
        user_id = db.create_document(collection_name, test_user)
        print(f"Created user with ID: {user_id}")

        # 3. Retrieve the user
        print("\n3. Retrieving user...")
        user = db.get_document(collection_name, {"username": "test_user"})
        print("Retrieved user:")
        pprint(user)

        # 4. Update user information
        print("\n4. Updating user...")
        update_result = db.update_document(
            collection_name,
            {"username": "test_user"},
            {"profile.age": 26, "last_updated": "2024-03-20"}
        )
        print(f"Update successful: {update_result}")

        # 5. List all users
        print("\n5. Listing all users:")
        users = db.list_documents(collection_name)
        for user in users:
            pprint(user)

        # 6. List all collections
        print("\n6. Available collections:")
        collections = db.list_collections()
        for collection in collections:
            print(f"- {collection}")

        # 7. Clean up - Delete test user
        print("\n7. Cleaning up - Deleting test user...")
        delete_result = db.delete_document(collection_name, {"username": "test_user"})
        print(f"Deletion successful: {delete_result}")

    except Exception as e:
        print(f"\nError during operations: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_mongodb_operations() 