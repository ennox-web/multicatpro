"""GraphQL Goal Schema."""
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from mongoengine import DoesNotExist
from mongoengine.connection import get_connection

import strawberry

from api.schemas.generic_schema import DelInput, UpdatedGQL
from api.db.goal import GoalType, Goal
from api.db.project import Project
from api.db.user import User
from api.utils import convert_to_graphql_type, setup_fields, IGNORE_FIELDS


@strawberry.type
class GoalGQL:
    """Goal GraphQL Type."""
    id: strawberry.ID
    name: Optional[str] = None
    projects: Optional[List[strawberry.ID]] = None
    last_update: Optional[datetime] = None
    active: Optional[bool] = False
    completed: Optional[bool] = False
    goal_type: Optional[GoalType] = None
    target: Optional[int] = None
    progress: Optional[int] = None


@strawberry.input
class GoalInput:
    """GraphQL Input for adding a Goal."""
    id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    projects: Optional[List[strawberry.ID]] = None
    last_update: Optional[datetime] = None
    active: Optional[bool] = False
    completed: Optional[bool] = False
    goal_type: Optional[GoalType] = None
    target: Optional[int] = None
    progress: Optional[int] = None


def setup_goal_fields(goal_input: GoalInput, user: User):
    """Setup fields for Goals"""
    fields = setup_fields(goal_input, IGNORE_FIELDS)
    fields["user"] = user

    if len(goal_input.projects) > 0:
        projects = []
        for project_id in goal_input.projects:
            projects.append(Project.objects(id=ObjectId(project_id), user=user).first())

        if len(projects) > 0:
            fields["projects"] = projects

    return fields


@strawberry.type
class GoalQuery:
    """GoalQuery GraphQL Type."""
    @strawberry.field
    def goals(self, info: strawberry.Info) -> List[GoalGQL]:
        """Get all Goals."""
        return [convert_to_graphql_type(goal, GoalGQL) for goal in Goal.objects(user=info.context.user)]


@strawberry.type
class GoalMutation:
    """GoalMutation GraphQL Type."""
    @strawberry.mutation
    def add_goal(self, info: strawberry.Info, goal_input: GoalInput) -> GoalGQL:
        """Add a new Goal to MongoDB."""
        fields = setup_goal_fields(goal_input, info.context.user)
        goal = Goal(**fields).save()

        return convert_to_graphql_type(goal, GoalGQL)

    @strawberry.mutation
    def delete_goal(self, info: strawberry.Info, goal_input: DelInput) -> UpdatedGQL:
        """Delete a Goal from MongoDB."""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    goal = Goal.objects(id=ObjectId(goal_input.id), user=info.context.user).first()
                    goal.delete()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=goal_input.id,
                        error=f"Goal document could not be deleted. Error{e}"
                    )

        return UpdatedGQL(
            updated=True,
            oid=goal_input.id
        )

    @strawberry.mutation
    def update_goal(self, info: strawberry.Info, goal_input: GoalInput) -> UpdatedGQL:
        """Update a Goal in MongoDB."""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    if goal_input.id is None:
                        raise DoesNotExist("No ID detected for Goal")

                    goal = Goal.objects(id=ObjectId(goal_input.id), user=info.context.user)
                    fields = setup_goal_fields(goal_input, user=info.context.user)
                    goal.update(**fields)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=goal_input.id,
                        error=f"Unable to update Goal. Error: {e}"
                    )

        return UpdatedGQL(
            updated=True,
            oid=goal_input.id,
        )
