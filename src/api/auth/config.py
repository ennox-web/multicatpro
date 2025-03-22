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

MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_FROM = os.environ['MAIL_FROM']
MAIL_PORT = int(os.environ['MAIL_PORT'])
MAIL_SERVER = os.environ['MAIL_SERVER']
TEST_EMAIL = os.environ['TEST_EMAIL']
