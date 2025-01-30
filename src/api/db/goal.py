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
    PULL
)

from api.db.project import Project


class GoalType(Enum):
    """GoalType EmbeddedDocument for MongoDB."""
    COMPLETED = "COMPLETED"
    PROGRESS = "PROGRESS"


class Goal(Document):
    """Goal Document for MongoDB."""
    projects = ListField(LazyReferenceField(Project, reverse_delete_rule=PULL))
    name = StringField()
    last_update = DateTimeField(default=datetime.today())
    active = BooleanField(default=True)
    completed = BooleanField(default=False)
    goal_type = EnumField(GoalType, required=True)
    target = IntField(default=0)
    progress = IntField(default=0)
