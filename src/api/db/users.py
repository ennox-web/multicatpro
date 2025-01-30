"""Users MongoDB Schema."""

from mongoengine import (
    Document,
    StringField
)


class Users(Document):
    """Test Users Document for MongoDB."""
    username = StringField(max_length=16, required=True)
    password = StringField(max_length=30, required=True)
    email = StringField(required=True)
