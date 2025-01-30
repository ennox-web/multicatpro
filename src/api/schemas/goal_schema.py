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
from api.utils import convert_to_graphql_type


@strawberry.type
class GoalProjectGQL:
    id: strawberry.ID


@strawberry.type
class GoalGQL:
    """Goal GraphQL Type."""
    id: strawberry.ID
    name: Optional[str] = None
    projects: Optional[List[GoalProjectGQL]] = None
    last_update: Optional[datetime] = None
    active: Optional[bool] = False
    completed: Optional[bool] = False
    goal_type: Optional[GoalType] = None
    target: Optional[int] = None
    progress: Optional[int] = None


@strawberry.input
class GoalInput:
    """GraphQL Input for adding a Goal."""
    id: Optional[str] = None
    name: Optional[str] = None
    projects: Optional[List[strawberry.ID]] = None
    last_update: Optional[datetime] = None
    active: Optional[bool] = False
    completed: Optional[bool] = False
    goal_type: Optional[GoalType] = None
    target: Optional[int] = None
    progress: Optional[int] = None


@strawberry.type
class GoalQuery:
    """GoalQuery GraphQL Type."""
    @strawberry.field
    def goals(self) -> List[GoalGQL]:
        """Get all Goals."""
        return [convert_to_graphql_type(goal, GoalGQL) for goal in Goal.objects]


def setup_goal_fields(goal_input: GoalInput):
    """Setup fields for Goals"""
    fields = {}
    no_error = False

    for key, value in goal_input.__dict__.items():
        if value is not None and key not in ("id", "projects"):
            fields[key] = value

    if len(goal_input.projects) > 0:
        projects = []
        for project_id in goal_input.projects:
            try:

                projects.append(Project.objects.get(id=ObjectId(project_id)))
            except DoesNotExist:
                if not no_error:
                    fields["error"] = []
                    no_error = True
                fields["error"].append(f"Unable to find Project with ID {project_id}")

        if len(projects) > 0:
            fields["projects"] = projects

    return fields


@strawberry.type
class GoalMutation:
    """GoalMutation GraphQL Type."""
    @strawberry.mutation
    def add_goal(self, goal_input: GoalInput) -> GoalGQL:
        """Add a new Goal to MongoDB."""
        fields = setup_goal_fields(goal_input)
        if "errors" in fields.keys():
            raise Exception(f"Errors have been detected: {fields["errors"]}")  # pylint: disable=broad-exception-raised

        goal = Goal(**fields).save()
        # goal.oid = goal.id  # pylint: disable=no-member
        # goal.save()

        print(f"PROJECTS: {goal.projects}")

        goal_gql = convert_to_graphql_type(goal, GoalGQL)
        goal_gql.id = goal.id
        print(goal.id)
        return goal_gql

    @strawberry.mutation
    def delete_goal(self, goal_input: DelInput) -> UpdatedGQL:
        """Delete a Goal from MongoDB."""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    goal = Goal.objects.get(id=ObjectId(goal_input.id))
                    goal.delete()
                except Exception as e:
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
    def update_goal(self, goal_input: GoalInput) -> UpdatedGQL:
        """Update a Goal in MongoDB."""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    if goal_input.id is None:
                        raise DoesNotExist("No ID detected for Goal")

                    goal = Goal.objects.get(id=ObjectId(goal_input.id))
                    fields = setup_goal_fields(goal_input)
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
