from pymongo import MongoClient
from pprint import pprint
import os
from dotenv import load_dotenv
import certifi
import sys

def test_connection():
    # Load environment variables from .env in current directory
    load_dotenv()
    
    # Get MongoDB URI from environment variables
    connection_string = os.getenv('MONGODB_URI')
    
    if not connection_string:
        print("Error: MONGODB_URI not found in environment variables")
        return
        
    print(f"Python version: {sys.version}")
    print("Certifi version:", certifi.__version__)
    print("Certificate file location:", certifi.where())
    print("\nAttempting to connect to MongoDB...")
    
    try:
        # Create a MongoDB client with explicit options
        client = MongoClient(
            "mongodb+srv://cluster0.dtighme.mongodb.net/",
            username="info",
            password="MjFTSPz47ijAcjRV",
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        
        # Test the connection
        client.admin.command('ping')
        print("\nSuccessfully connected to MongoDB!")
        
        # Get database list
        print("\nAvailable databases:")
        dbs = client.list_database_names()
        for db in dbs:
            print(f"- {db}")
            
        # Connect to your specific database
        db = client['oforha-ai']
        
        # List collections
        print("\nCollections in oforha-ai:")
        for collection in db.list_collection_names():
            print(f"- {collection}")
        
        # Create a test collection and insert a document
        test_collection = db.test_collection
        test_doc = {"name": "test", "status": "success"}
        
        result = test_collection.insert_one(test_doc)
        print("\nInserted test document with id:", result.inserted_id)
        
        # Retrieve the document
        print("\nRetrieved document:")
        pprint(test_collection.find_one({"name": "test"}))
        
        # Clean up - remove test document
        test_collection.delete_one({"name": "test"})
        print("\nTest document removed")
        
    except Exception as e:
        print("\nError connecting to MongoDB Atlas:", str(e))
        if hasattr(e, 'details'):
            print("Error details:", e.details)
        print("\nTroubleshooting tips:")
        print("1. Check if your MongoDB Atlas cluster is running")
        print("2. Verify your IP address is whitelisted in MongoDB Atlas")
        print("3. Ensure your username and password are correct")
        print("4. Check if your network allows outbound connections to MongoDB Atlas")
        print("5. Try connecting with mongosh to verify credentials")
    
if __name__ == "__main__":
    test_connection() 