"""Tag MongoDB Schema."""
from mongoengine import (
    StringField,
    LazyReferenceField,
    Document,
    CASCADE
)
from api.db.user import User

class Tag(Document):
    """Tag EmbeddedDocument for MongoDB."""
    name = StringField(required=True)
    user = LazyReferenceField(User, required=True, reverse_delete_rule=CASCADE)
