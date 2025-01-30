"""Tag Mongo DB Schema."""

from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
)


class Tag(Document):
    """Tag Document for MongoDB"""
    oid = ObjectIdField()
    name = StringField()
