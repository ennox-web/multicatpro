import strawberry
from strawberry.types import Info
from typing import List

from api.db.users import Users
from api.utils import convert_to_graphql_type



@strawberry.type
class UserType:
    username: str
    email: str


@strawberry.type
class UserQuery:
    @strawberry.field
    def users(self) -> List[UserType]:
        return [convert_to_graphql_type(user, UserType) for user in Users.objects]

@strawberry.type
class AnotherQuery:
    @strawberry.field
    def fake_users(self) -> List[UserType]:
        return [UserType(email="blerb", username="blep")]


@strawberry.type
class Query:
    @strawberry.field
    def fake(self) -> AnotherQuery:
        return AnotherQuery()

    @strawberry.field
    def users(self) -> UserQuery:
        return UserQuery()

schema = strawberry.Schema(query=Query)
