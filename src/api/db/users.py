from mongoengine import (
    Document,
    StringField
)


class Users(Document):
    username = StringField(max_length=16, required=True)
    password = StringField(max_length=30, required=True)
    email = StringField(required=True)
