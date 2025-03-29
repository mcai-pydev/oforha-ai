import os
from pathlib import Path
from dotenv import load_dotenv

print("=== Environment Debug Info ===")

# Print current directory
current_dir = os.getcwd()
print(f"\nCurrent working directory: {current_dir}")

# Check if .env file exists
env_path = Path(current_dir) / '.env'
print(f"\n.env file path: {env_path}")
print(f".env file exists: {env_path.exists()}")

if env_path.exists():
    print("\n.env file contents:")
    with open(env_path, 'r') as f:
        print(f.read())

# Try loading the environment variables
print("\nAttempting to load .env file...")
load_dotenv(verbose=True)

# Print relevant environment variables
print("\nEnvironment variables after loading:")
webhook_url = os.getenv('N8N_WEBHOOK_URL')
port = os.getenv('PORT')

print(f"N8N_WEBHOOK_URL: {webhook_url}")
print(f"PORT: {port}") 