"""Goal MongoDB Schema."""

from enum import Enum
from datetime import datetime

from mongoengine import (
    Document,
    LazyReferenceField,
    ListField,
    StringField,
    DateTimeField,
    BooleanField,
    EnumField,
    IntField,
    PULL,
    CASCADE
)

from api.db.project import Project
from api.db.user import User


class GoalType(Enum):
    """GoalType EmbeddedDocument for MongoDB."""
    COMPLETED = "COMPLETED"
    PROGRESS = "PROGRESS"


class Goal(Document):
    """Goal Document for MongoDB."""
    user = LazyReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField()
    projects = ListField(LazyReferenceField(Project, reverse_delete_rule=PULL))
    last_update = DateTimeField(default=datetime.today())
    active = BooleanField(default=True)
    completed = BooleanField(default=False)
    goal_type = EnumField(GoalType, required=True)
    target = IntField(default=0)
    progress = IntField(default=0)
