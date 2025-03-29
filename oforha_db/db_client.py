from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

class MongoDBClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get MongoDB connection string
        self.connection_string = os.getenv('MONGODB_URI')
        if not self.connection_string:
            raise ValueError("MongoDB connection string not found in environment variables")
            
        # Initialize the client with ServerApi
        print("Connecting to MongoDB...")
        self.client = MongoClient(self.connection_string, server_api=ServerApi('1'))
        self.db = self.client['oforha-ai']
        
        # Test connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            # List available databases
            print("\nAvailable databases:")
            databases = self.client.list_database_names()
            for db in databases:
                print(f"- {db}")
                
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def create_document(self, collection_name: str, document: Dict) -> str:
        """Create a new document in the specified collection"""
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)
    
    def get_document(self, collection_name: str, query: Dict) -> Optional[Dict]:
        """Get a document from the specified collection"""
        collection = self.db[collection_name]
        return collection.find_one(query)
    
    def update_document(self, collection_name: str, query: Dict, update_data: Dict) -> bool:
        """Update a document in the specified collection"""
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0
    
    def delete_document(self, collection_name: str, query: Dict) -> bool:
        """Delete a document from the specified collection"""
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count > 0
    
    def list_documents(self, collection_name: str, query: Dict = None) -> List[Dict]:
        """List all documents in the specified collection"""
        collection = self.db[collection_name]
        return list(collection.find(query or {}))
    
    def create_collection(self, collection_name: str):
        """Create a new collection"""
        self.db.create_collection(collection_name)
    
    def list_collections(self) -> List[str]:
        """List all collections"""
        return self.db.list_collection_names()
    
    def close(self):
        """Close the MongoDB connection"""
        self.client.close()
        print("MongoDB connection closed")

# Example usage
if __name__ == "__main__":
    try:
        # Initialize the client
        db = MongoDBClient()
        
        # Test basic operations
        collection_name = "test_collection"
        
        # Create a test document
        test_doc = {
            "name": "test_document",
            "status": "active",
            "data": {
                "field1": "value1",
                "field2": "value2"
            }
        }
        
        print("\nCreating test document...")
        doc_id = db.create_document(collection_name, test_doc)
        print(f"Created document with ID: {doc_id}")
        
        # Retrieve the document
        print("\nRetrieving document...")
        doc = db.get_document(collection_name, {"name": "test_document"})
        print("Retrieved document:", doc)
        
        # Update the document
        print("\nUpdating document...")
        db.update_document(
            collection_name,
            {"name": "test_document"},
            {"status": "updated"}
        )
        
        # List all documents
        print("\nListing all documents:")
        docs = db.list_documents(collection_name)
        for doc in docs:
            print(doc)
        
        # Clean up
        print("\nDeleting test document...")
        db.delete_document(collection_name, {"name": "test_document"})
        
        # List collections
        print("\nAvailable collections:")
        collections = db.list_collections()
        for collection in collections:
            print(f"- {collection}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'db' in locals():
            db.close() 