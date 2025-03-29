import os
from dotenv import load_dotenv

# Load environment variables from oforha_db/.env
dotenv_path = os.path.join(os.path.dirname(__file__), 'oforha_db', '.env')
print(f"Looking for .env file at: {os.path.abspath(dotenv_path)}")

if os.path.exists(dotenv_path):
    print("Found .env file!")
    load_dotenv(dotenv_path)
    connection_string = os.getenv('MONGODB_URI')
    if connection_string:
        # Mask the password in the connection string
        if '@' in connection_string:
            parts = connection_string.split('@')
            credentials = parts[0].split(':')
            masked_uri = f"{credentials[0]}:****@{parts[1]}"
            print(f"\nFound connection string: {masked_uri}")
    else:
        print("No MONGODB_URI found in .env file")
else:
    print(".env file not found!") 