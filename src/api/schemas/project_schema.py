"""GraphQL Project Schema."""

from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId
import strawberry
from mongoengine import DoesNotExist
from mongoengine.connection import get_connection

from api.db.project import Project
from api.db.project_type import ProjectType, Field
from api.db.user import User
from api.db.tag import Tag
from api.schemas.tag_schema import TagGQL
from api.schemas.project_type_schema import ProjectTypeGQL, FieldTypeGQL, AddFieldTypeInput, UpdateFieldTypeInput
from api.schemas.generic_schema import DelInput, UpdatedGQL
from api.utils import convert_to_graphql_type, setup_fields, IGNORE_FIELDS


@strawberry.type
class ProjectGQL:
    """Project GraphQL Type."""
    # user: LazyUserGQL
    id: strawberry.ID
    name: str
    project_type: Optional[ProjectTypeGQL] = None
    project_template_id: Optional[strawberry.ID] = None
    fields: Optional[List[FieldTypeGQL]] = None

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
    project_type_id: Optional[strawberry.ID] = None
    project_template_id: Optional[strawberry.ID] = None
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
    id: strawberry.ID
    name: Optional[str] = None
    project_type_id: Optional[strawberry.ID] = None
    project_template_id: Optional[strawberry.ID] = None
    fields: Optional[List[UpdateFieldTypeInput]] = None
    started_on: Optional[datetime] = None
    completed_on: Optional[datetime] = None
    tag_names: Optional[List[str]] = None
    priority: Optional[int] = None
    progress: Optional[float] = None
    steps: Optional[List[str]] = None
    active_step: Optional[int] = None


# SETUP FUNCTIONS

def update_internal_field(field_input: UpdateFieldTypeInput, project: Project):
    """Update an existing Field for a Project."""
    current_field = project.fields.filter(oid=field_input.id).first()
    if current_field:
        if hasattr(field_input, "mark_for_deletion") and field_input.mark_for_deletion:
            index = project.fields.index(current_field)
            del project.fields[index]
        else:
            setup_fields(field_input, IGNORE_FIELDS, current_field)


def setup_internal_fields(fields: List[UpdateFieldTypeInput], project: Project=None):
    """Setup Fields for Project."""
    field_objects = []
    for field in fields:
        if hasattr(field, "oid") and project:
            update_internal_field(field, project)
        else:
            new_field_data = setup_fields(field, IGNORE_FIELDS)
            field_objects.append(Field(**new_field_data))
    return field_objects



def setup_tags(tag_names: List[str], user: User) -> List[Tag]:
    """Setup Project Tags."""
    tags = []
    if tag_names:
        for tag_name in tag_names:
            try:
                tag = None
                if user:
                    tag = Tag.objects(user=user, name=tag_name).first()
                if not tag:
                    raise DoesNotExist
            except DoesNotExist:
                tag = Tag(name=tag_name, user=user)
                tag.save()

            tags.append(tag)
        user.save()

    return tags


def setup_project_fields(
    project_input: AddProjectInput | UpdateProjectInput,
    user: User,
    project: Project=None,
) -> dict:
    """Setup Project fields based on input."""
    fields = setup_fields(project_input, IGNORE_FIELDS)
    fields["updated_on"] = datetime.now()

    # Setup Tags
    tags = setup_tags(project_input.tag_names, user=user)
    if len(tags) > 0:
        fields["tags"] = tags

    if project_input.fields:
        internal_fields = setup_internal_fields(project_input.fields, project=project)
        if len(internal_fields) > 0:
            fields["fields"] = internal_fields

    if project_input.project_type_id:
        project_type = ProjectType.objects.get(id=ObjectId(project_input.project_type_id))
        fields["project_type"] = project_type

    if project:
        project.save()

    return fields


@strawberry.type
class ProjectQuery:
    """ProjectQuery GraphQL Type."""
    @strawberry.field
    def projects(self) -> List[ProjectGQL]:
        """Get all Projects."""
        return [convert_to_graphql_type(project, ProjectGQL) for project in Project.objects]

    @strawberry.field
    def user_projects(self, info: strawberry.Info) -> List[ProjectGQL]:
        """Get User's Projects."""
        projects = Project.objects(user=info.context.user)
        return [convert_to_graphql_type(project, ProjectGQL) for project in projects]


@strawberry.type
class ProjectMutation:
    """ProjectMutation GraphQL Type."""
    @strawberry.mutation
    def add_project(self, info: strawberry.Info, project_input: AddProjectInput) -> ProjectGQL:
        """Add a new Project to MongoDB."""
        fields = setup_project_fields(project_input, user=info.context.user)
        fields["user"] = info.context.user

        project = Project(**fields).save()

        return convert_to_graphql_type(project, ProjectGQL)

    @strawberry.mutation
    def delete_project(self, info: strawberry.Info, project_input: DelInput) -> UpdatedGQL:
        """Delete a Project from MongoDB"""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project = Project.objects.get(id=ObjectId(project_input.id), user=info.context.user)
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
    def update_project(self, info: strawberry.Info, project_input: UpdateProjectInput) -> UpdatedGQL:
        """Update a Project in MongoDB."""
        mongo = get_connection()
        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project = Project.objects.get(id=ObjectId(project_input.id), user=info.context.user)
                    fields = setup_project_fields(project_input, info.context.user, project=project)
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
