from pymongo import MongoClient
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

class MongoDB:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('MONGODB_URI')
        self.client = MongoClient(self.connection_string)
        self.db = self.client['oforha-ai']
    
    def create_user(self, user_data: Dict) -> str:
        """Create a new user"""
        collection = self.db.users
        result = collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        collection = self.db.users
        return collection.find_one({"_id": user_id})
    
    def update_user(self, user_id: str, update_data: Dict) -> bool:
        """Update user data"""
        collection = self.db.users
        result = collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        collection = self.db.users
        result = collection.delete_one({"_id": user_id})
        return result.deleted_count > 0
    
    def list_users(self) -> List[Dict]:
        """List all users"""
        collection = self.db.users
        return list(collection.find())
    
    def create_collection(self, collection_name: str):
        """Create a new collection"""
        self.db.create_collection(collection_name)
    
    def list_collections(self) -> List[str]:
        """List all collections"""
        return self.db.list_collection_names()
    
    def close(self):
        """Close the MongoDB connection"""
        self.client.close()

# Example usage
if __name__ == "__main__":
    # Test the MongoDB class
    db = MongoDB()
    
    try:
        # Create a test user
        test_user = {
            "username": "test_user",
            "email": "test@example.com",
            "role": "user"
        }
        
        print("Creating test user...")
        user_id = db.create_user(test_user)
        print(f"Created user with ID: {user_id}")
        
        # Get user
        print("\nRetrieving user...")
        user = db.get_user(user_id)
        print("Retrieved user:", user)
        
        # Update user
        print("\nUpdating user...")
        db.update_user(user_id, {"role": "admin"})
        
        # List users
        print("\nListing all users:")
        users = db.list_users()
        for user in users:
            print(user)
        
        # Clean up
        print("\nDeleting test user...")
        db.delete_user(user_id)
        
        print("\nAvailable collections:")
        collections = db.list_collections()
        for collection in collections:
            print(f"- {collection}")
            
    except Exception as e:
        print("Error:", e)
    finally:
        db.close() 