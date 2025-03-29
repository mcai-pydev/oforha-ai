from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

def get_database():
    try:
        # Create a MongoDB client with explicit options
        client = MongoClient(
            "mongodb+srv://cluster0.dtighme.mongodb.net/",
            username="info",
            password="MjFTSPz47ijAcjRV",
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000
        )
        
        # Get the database
        db = client['oforha-ai']
        return db
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        raise e

# Get collections
def get_collections():
    db = get_database()
    return {
        'users': db.users,
        'subscribers': db.subscribers,
        'forms': db.forms,
        'sessions': db.sessions
    } 