"""User MongoDB Schema."""

from mongoengine import (
    Document,
    StringField,
    BinaryField
)


class User(Document):
    """Test Users Document for MongoDB."""
    username = StringField(max_length=16, required=True)
    password = BinaryField(required=True)
    email = StringField(required=True)
