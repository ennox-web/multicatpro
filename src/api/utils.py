"""GraphQL Utils."""
from typing import List, TypeVar

from strawberry import UNSET
import bcrypt


T = TypeVar('T')
Y = TypeVar('Y')

IGNORE_FIELDS = [
    "id",
    "oid",
    "mark_for_deletion",
    "fields",
    "project_templates",
    "project_type_id",
    "tag_names",
    "projects"
]


def verify_password(plain_password, hashed_password):
    """Verify user password."""
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)


def get_hashed_password(password: str):
    """Get the hashed password."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def get_graphql_type_fields_name(type_: T) -> List[str]:
    """Returns a list of keys for the Object.

    Args:
        type_: The GraphQL type to get fields from.

    Returns:
        List[str]: A list of the fields in the GraphQL type.
    """
    return type_.__dict__["__dataclass_fields__"].keys()


def convert_to_graphql_type(db_model_object: Y, graphql_type: T) -> T:
    """Converts a MongoDB type object to a GraphQL object.

    Args:
        db_model_object: The MongoDB object to convert.
        graphql_type: The GraphQL type to convert to.

    Returns:
        Object: The GraphQL object the MongoDB object has been converted to.
    """
    fields = get_graphql_type_fields_name(graphql_type)
    return graphql_type(**{f: getattr(db_model_object, f) for f in fields})


def setup_fields(input_fields: object, ignore_keys: List[str], fields: dict = None) -> dict:
    """Setup fields from GQL Input types for MongoDB.

    Args:
        fields: A dictionary of fields from GQL Input.
        ignore_keys: A list of keys to ignore from the GQL Input.
    """
    if fields is None:
        fields = {}
    for key, value in input_fields.__dict__.items():
        print(f"key: {key}; value: {value}")
        if value is UNSET:
            print("UNSET!")
        if value is not UNSET and key not in ignore_keys:
            fields[key] = value
    return fields
