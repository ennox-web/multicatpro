""""""

import strawberry

from api.schemas.users_schema import UserQuery, AnotherQuery
from api.schemas.project_type_schema import ProjectTypeQuery, ProjectTypeMutation
from api.schemas.project_schema import ProjectQuery, ProjectMutation
from api.schemas.goal_schema import GoalQuery, GoalMutation


@strawberry.type
class Query:
    """Strawberry Query Type."""

    # project_templates: List[ProjectTemplateType] = strawberry.field(resolver=get_project_templates)
    @strawberry.field
    def fake(self) -> AnotherQuery:
        """Fake Users Query for testing purposes."""
        return AnotherQuery()

    @strawberry.field
    def users(self) -> UserQuery:
        """Test Users Query."""
        return UserQuery()

    @strawberry.field
    def project_types(self) -> ProjectTypeQuery:
        """ProjectTypes Query."""
        return ProjectTypeQuery()

    @strawberry.field
    def projects(self) -> ProjectQuery:
        """Projects Query."""
        return ProjectQuery()

    @strawberry.field
    def goals(self) -> GoalQuery:
        """Goal Query."""
        return GoalQuery()


@strawberry.type
class Mutation:
    """Strawberry Mutation Type."""

    @strawberry.field
    def project_type(self) -> ProjectTypeMutation:
        """ProjectType Mutation."""
        return ProjectTypeMutation()

    @strawberry.field
    def project(self) -> ProjectMutation:
        """Project Mutation."""
        return ProjectMutation()

    @strawberry.field
    def goal(self) -> GoalMutation:
        """Goal Mutation."""
        return GoalMutation()


schema = strawberry.Schema(query=Query, mutation=Mutation)
