"""GraphQL Tag Schema."""

from typing import List

import strawberry

from api.db.tag import Tag
from api.utils import convert_to_graphql_type

# GQL Types

@strawberry.type
class TagGQL:
    """Tag GraphQL Type."""
    id: strawberry.ID
    name: str


# GQL QUERY

@strawberry.type
class TagQuery:
    """TagQuery GraphQL Type."""
    @strawberry.field
    def user_tags(self, info: strawberry.Info) -> List[TagGQL]:
        """Get all User's Tags."""
        return [convert_to_graphql_type(tag, TagGQL) for tag in Tag.objects(user=info.context.user)]
