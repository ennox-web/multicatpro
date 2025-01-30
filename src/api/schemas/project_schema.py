"""GraphQL Project Schema."""

from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
import strawberry
from mongoengine import DoesNotExist
from mongoengine.connection import get_connection

from api.db.project import Project, Tag
from api.db.project_type import ProjectType, Field
from api.schemas.project_type_schema import ProjectTypeGQL, FieldTypeGQL, AddFieldTypeInput, UpdateFieldTypeInput
from api.schemas.generic_schema import DelInput, UpdatedGQL
from api.utils import convert_to_graphql_type


@strawberry.type
class TagGQL:
    """Tag GraphQL Type."""
    oid: strawberry.ID
    name: str


@strawberry.type
class ProjectGQL:
    """Project GraphQL Type."""
    oid: strawberry.ID
    name: str
    project_type: Optional[ProjectTypeGQL] = None
    project_template_id: Optional[int] = None
    fields: Optional[FieldTypeGQL] = None

    started_on: Optional[datetime] = None
    completed_on: Optional[datetime] = None
    updated_on: datetime

    tags: Optional[List[TagGQL]] = None
    priority: Optional[int] = None
    progress: Optional[float] = None
    steps: Optional[List[str]] = None
    active_step: Optional[int] = None


@strawberry.input
class AddProjectInput:
    """ProjectInput GraphQL Type."""
    name: str
    project_type_id: Optional[str] = None
    project_template_id: Optional[int] = None
    fields: Optional[List[AddFieldTypeInput]] = None
    started_on: Optional[datetime] = None
    completed_on: Optional[datetime] = None
    tag_names: Optional[List[str]] = None
    priority: Optional[int] = None
    progress: Optional[float] = None
    steps: Optional[List[str]] = None
    active_step: Optional[int] = None


@strawberry.input
class UpdateProjectInput:
    """GraphQL Input for updating a Project."""
    id: str
    name: Optional[str] = None
    project_type_id: Optional[str] = None
    project_template_id: Optional[int] = None
    fields: Optional[List[UpdateFieldTypeInput]] = None
    started_on: Optional[datetime] = None
    completed_on: Optional[datetime] = None
    tag_names: Optional[List[str]] = None
    priority: Optional[int] = None
    progress: Optional[float] = None
    steps: Optional[List[str]] = None
    active_step: Optional[int] = None


def setup_project_fields(project_input: AddProjectInput | UpdateProjectInput, project: Project=None) -> dict:
    """Setup Project fields based on input."""
    fields = {}
    updated_on = datetime.now()

    tags = []
    if project_input.tag_names:
        for tag_name in project_input.tag_names:
            try:
                tag = Tag.objects.get(name=tag_name)
            except DoesNotExist:
                tag = Tag(name=tag_name).save()
                tag.oid = tag.id  # pylint: disable=no-member
                tag.save()
            tags.append(tag)

        fields["tags"] = tags

    for key, value in project_input.__dict__.items():
        if value is not None and key not in ("id", "project_type_id", "tag_names", "fields"):
            fields[key] = value

    if project_input.fields:
        field_objects = []
        for field in project_input.fields:
            if field.id and project:
                try:
                    print(f"Field to update {field}")
                    current_field = project.fields.filter(oid=field.id).first()
                    if current_field:
                        for key, value in field.__dict__.items():
                            print(f"key: {key}; value: {value}")
                            if value is not None and key not in ("id", "mark_for_deletion"):
                                current_field[key] = value
                        # project.fields.filter(oid=field.id).update(**field_data)
                        project.save()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(f"FAIL: {e}")
            else:
                field_objects.append(
                    Field(
                        label=field.label,
                        data_type=field.data_type,
                        content={"content": field.content},
                        description=field.description
                    )
                )
        if len(field_objects) > 0:
            fields["fields"] = field_objects

    if project_input.project_type_id:
        project_type = ProjectType.objects.get(id=ObjectId(project_input.project_type_id))
        fields["project_type"] = project_type

    fields["updated_on"] = updated_on

    print(fields)

    return fields


@strawberry.type
class ProjectQuery:
    """ProjectQuery GraphQL Type."""
    @strawberry.field
    def projects(self) -> List[ProjectGQL]:
        """Get all Projects."""
        return [convert_to_graphql_type(project, ProjectGQL) for project in Project.objects]


@strawberry.type
class ProjectMutation:
    """ProjectMutation GraphQL Type."""
    @strawberry.mutation
    def add_project(self, project_input: AddProjectInput) -> ProjectGQL:
        """Add a new Project to MongoDB."""
        fields = setup_project_fields(project_input)

        project = Project(**fields).save()
        project.oid = project.id  # pylint: disable=no-member
        project.save()

        return convert_to_graphql_type(project, ProjectGQL)

    @strawberry.mutation
    def delete_project(self, project_input: DelInput) -> UpdatedGQL:
        """Delete a Project from MongoDB"""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project = Project.objects.get(id=ObjectId(project_input.id))
                    project.delete()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=project_input.id,
                        error=f"Project document could not be deleted. Error: {e}",
                    )

        return UpdatedGQL(
            updated=True,
            oid=project_input.id,
        )

    # Find relevent goals and upate progress
    @strawberry.mutation
    def update_project(self, project_input: UpdateProjectInput) -> UpdatedGQL:
        """Update a Project in MongoDB."""
        mongo = get_connection()
        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project = Project.objects.get(id=ObjectId(project_input.id))
                    fields = setup_project_fields(project_input, project=project)
                    project.update(**fields)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=project_input.id,
                        error=f"Project document could not be updated. Error: {e}",
                    )
        return UpdatedGQL(
            updated=True,
            oid=project_input.id,
        )


# """

# @strawberry.type
# class Author:
#     id: int
#     name: str

# @strawberry.type
# class Book:
#     id: int
#     title: str
#     author: Author

# @strawberry.input
# class CreateBookInput:
#     title: str
#     author_id: int

# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     async def create_book(self, info, input: CreateBookInput) -> Book:
#         # Assume we have a database connection here
#         author = await get_author_by_id(input.author_id)  # Implement this function
#         if not author:
#             raise Exception("Author not found")

#         new_book = await create_book_in_db(input.title, author.id)  # Implement this function
#         return Book(id=new_book.id, title=new_book.title, author=author)

# """
