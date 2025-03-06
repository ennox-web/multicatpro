"""User MongoDB Schema."""

from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    BinaryField,
    BooleanField,
    DateTimeField
)


class User(Document):
    """Test Users Document for MongoDB."""
    username = StringField(max_length=16, required=True)
    password = BinaryField(required=True)
    email = StringField(required=True)
    blacklisted = BooleanField(default=False)
    verified = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
