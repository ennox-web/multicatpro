"""JWT Revoked Tokens Schema."""

from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    BooleanField
)


class Token(Document):
    """Token Blacklist document for MongoDB."""
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)
    access_expiration_date = DateTimeField(required=True)
    refresh_expiration_date = DateTimeField(required=True)
    blacklisted = BooleanField(default=False)
