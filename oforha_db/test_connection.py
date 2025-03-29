from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get the connection string
    uri = os.getenv('MONGODB_URI')
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        
        # List available databases
        print("\nAvailable databases:")
        databases = client.list_database_names()
        for db in databases:
            print(f"- {db}")
            
    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__ == "__main__":
    test_connection() 