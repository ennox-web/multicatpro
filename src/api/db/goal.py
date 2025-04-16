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
    CASCADE,
    ReferenceField
)

from api.db.project import Project
from api.db.project_type import ProjectType
from api.db.user import User
from api.db.tag import Tag


class GoalType(Enum):
    """GoalType Enum for MongoDB."""
    COMPLETED = "COMPLETED"
    PROGRESS = "PROGRESS"


class Basis(Enum):
    """Basis Enum for MongoDB."""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    ANNUALLY = "ANNUALLY"


class Frequency(Enum):
    """Frequency Enum for MongoDB."""
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class Goal(Document):
    """Goal Document for MongoDB."""
    user = LazyReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField()
    projects = ListField(LazyReferenceField(Project, reverse_delete_rule=PULL))
    last_update = DateTimeField(default=datetime.today())
    active = BooleanField(default=True)
    completed = BooleanField(default=False)
    progress = IntField(default=0)

    basis = EnumField(Basis, required=True)  # Daily, Weekly, Monthly, Annually
    goal_type = EnumField(GoalType, required=True)  # COMPLETE or PROGRESS
    frequency = EnumField(Frequency, required=True)  # Per Day, Week, or Month
    target = IntField(default=0)  # Number of Projects to complete or make progress on
    project_type = ReferenceField(ProjectType, required=False)
    tags = ReferenceField(Tag, required=False)
    target_frequency = IntField(default=-1)  # How many Days, Weeks, Months
    target_date = DateTimeField(default=datetime.today())  # To complete by
    start_date = DateTimeField(default=datetime.today())
    pinned = BooleanField(default=False)
