"""MongoDB Client."""

from mongoengine import connect
from api.auth.config import MONGODB_URI, DB_NAME


# Connect to your MongoDB cluster:
client = connect(host=f'{MONGODB_URI}/{DB_NAME}')
