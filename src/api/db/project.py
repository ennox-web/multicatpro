"""Project Mongo DB Schema."""

from datetime import datetime

from mongoengine import (
    ObjectIdField,
    ReferenceField,
    StringField,
    DateTimeField,
    IntField,
    ListField,
    Document,
    FloatField,
    EmbeddedDocumentListField,
    LazyReferenceField,
    CASCADE,
    PULL
)

from api.db.project_type import ProjectType, Field
from api.db.user import User
from api.db.tag import Tag



class Project(Document):
    """Project Document for MongoDB."""
    user = LazyReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    name = StringField(required=True, max_length=60)
    project_type = ReferenceField(ProjectType, reverse_delete_rule=PULL)
    project_template_id = ObjectIdField()
    fields = EmbeddedDocumentListField(Field)

    started_on = DateTimeField()
    completed_on = DateTimeField()
    updated_on = DateTimeField(default=datetime.today())

    tags = ListField(ReferenceField(Tag), reverse_delete_rule=PULL)
    priority = IntField(default=0)

    progress = FloatField(default=0, required=True)
    steps = ListField(StringField())
    active_step = IntField(default=0)

    def to_json(self):  # pylint: disable=arguments-differ
        """Converts document to json."""
        data = self.to_mongo()
        data["project_type"] = {
            "Project Type": {
                "name": self.project_type.name
            }
        }
