"""JWT Revoked Tokens Schema."""

from mongoengine import (
    Document,
    StringField,
    DateTimeField,
)


class TokenBlacklist(Document):
    """Token Blacklist document for MongoDB."""
    token = StringField(required=True)
    expiration = DateTimeField(required=True)
