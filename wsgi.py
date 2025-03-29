from waitress import serve
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'oforha_db', '.env')
load_dotenv(dotenv_path)

app = create_app()

if __name__ == '__main__':
    print("Starting server with Waitress...")
    print(f"Using .env file from: {dotenv_path}")
    serve(app, host='0.0.0.0', port=4000) 