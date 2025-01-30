import os
from dotenv import load_dotenv

# Load config from a .env file:
if os.path.exists(".env.local"):
    load_dotenv(".env.local")
MONGODB_URI = os.environ['MONGODB_URI']
DB_NAME = os.environ['DB_NAME']
