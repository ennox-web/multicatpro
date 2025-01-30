"""Generic Schema Inputs."""
from typing import Optional

import strawberry


@strawberry.input
class DelInput:
    """GraphQL Input for deleting."""
    id: str


@strawberry.type
class UpdatedGQL:
    """UpdatedProject GraphQL Type."""
    updated: bool
    oid: strawberry.ID
    error: Optional[str] = None
