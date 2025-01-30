"""ProjectType MongoDB Schema."""

from datetime import datetime, time, date
from typing import Union, List
from enum import Enum
from bson.objectid import ObjectId


from mongoengine import (
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EnumField,
    ObjectIdField,
    StringField,
    ValidationError
)


# The FieldTypes enum mapped to expected Python types.
FIELD_TYPE_MAPPING = {
    "STRING": str,
    "NUMBER": Union[int, float],
    "LIST_OF_NUM": List[Union[int, float]],
    "LIST_OF_STRING": List[str],
    "DATE": date,
    "TIME": time,
    "DATETIME": datetime
}


class FieldTypes(Enum):
    """Enum depicting supported custom Field Types."""
    STRING = "STRING"
    NUMBER = "NUMBER"
    LIST_OF_NUM = "LIST_OF_NUM"
    LIST_OF_STRING = "LIST_OF_STRING"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"


class Field(EmbeddedDocument):
    """Embedded Document for Project Template fields."""
    oid = ObjectIdField(default=ObjectId())
    label = StringField(required=True)
    data_type = EnumField(FieldTypes, default=FieldTypes.STRING)
    content = DictField(required=False)
    description = StringField()

    def clean(self):
        if not isinstance(self.content["content"], FIELD_TYPE_MAPPING[self.data_type.name]):
            raise ValidationError(f'${self.content} is not of expected type ${str(self.data_type)}.')


class ProjectTemplate(EmbeddedDocument):
    """Project Template Embedded Document for new Projects."""
    oid = ObjectIdField(default=ObjectId())
    name = StringField(required=True)
    fields = EmbeddedDocumentListField(Field)


class ProjectType(Document):
    """ProjectType Document for MongoDB."""
    name = StringField(required=True)
    project_templates = EmbeddedDocumentListField(ProjectTemplate)
