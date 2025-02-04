"""Environment Variables."""

import os
from dotenv import load_dotenv

# Load config from a .env file:
if os.path.exists(".env.local"):
    load_dotenv(".env.local")
MONGODB_URI = os.environ['MONGODB_URI']
DB_NAME = os.environ['DB_NAME']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ALGO = os.environ['JWT_ALGO']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ['REFRESH_TOKEN_EXPIRE_DAYS'])
