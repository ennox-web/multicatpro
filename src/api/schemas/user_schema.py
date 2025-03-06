"""Users GraphQL Schema."""

from typing import List, Optional

import strawberry
from mongoengine.queryset.visitor import Q

from api.db.user import User
from api.utils import convert_to_graphql_type, get_hashed_password
from api.auth.email_validator import send_email


@strawberry.type
class UserGQL:
    """UserType GraphQL Type."""
    id: strawberry.ID
    username: str
    email: str


@strawberry.input
class UserInput:
    """UserInput GraphQL Type."""
    username: str
    email: str
    password: str


@strawberry.type
class UserQuery:
    """UserQuery GraphQL Type."""
    @strawberry.field
    def users(self) -> List[UserGQL]:
        """Returns list of all Users."""
        return [convert_to_graphql_type(user, UserGQL) for user in User.objects]


@strawberry.type
class UserMutation:
    """UserMutations GraphQL Type."""
    @strawberry.mutation
    async def register_new_user(self, user_input: UserInput) -> Optional[UserGQL]:
        """Add a new user"""
        user = User.objects(Q(username=user_input.username) | Q(email=user_input.email)).first()
        if user:
            print(f"Username: {user.username}\nEmail: {user.email}")
            raise Exception("Username or Email already exists")  # pylint: disable=broad-exception-raised

        hashed_password = get_hashed_password(user_input.password)
        user = User(username=user_input.username, password=hashed_password, email=user_input.email)
        user.save()
        await send_email()
        return convert_to_graphql_type(user, UserGQL)
