"""Users GraphQL Schema."""

from typing import List

import strawberry

from api.db.users import Users
from api.utils import convert_to_graphql_type


@strawberry.type
class UserType:
    """UserType GraphQL Type."""
    id: strawberry.ID
    username: str
    email: str


@strawberry.type
class UserQuery:
    """UserQuery GraphQL Type."""
    @strawberry.field
    def users(self) -> List[UserType]:
        """Returns list of all Users."""
        return [convert_to_graphql_type(user, UserType) for user in Users.objects]


@strawberry.type
class AnotherQuery:
    """AnotherQuery GraphQL Type."""
    @strawberry.field
    def fake_users(self) -> List[UserType]:
        """Returns list of fake Users."""
        return [UserType(email="blerb", username="blep")]
