"""Generic Schema Inputs."""
from typing import Optional

import strawberry


@strawberry.input
class DelInput:
    """GraphQL Input for deleting."""
    id: strawberry.ID


@strawberry.type
class UpdatedGQL:
    """UpdatedProject GraphQL Type."""
    updated: bool
    oid: strawberry.ID
    error: Optional[str] = None


# @strawberry.type
# class LazyUserGQL:
#     """LazyReference User GraphQL Type."""
#     id: strawberry.ID
#     user_id: strawberry.ID
