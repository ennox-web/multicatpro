"""GraphQL ProjectType Schema."""

from typing import List, Optional

from bson.objectid import ObjectId
from mongoengine import DoesNotExist
from mongoengine.connection import get_connection
import strawberry

from api.db.project_type import ProjectType, ProjectTemplate, Field, FieldTypes
from api.db.project import Project
from api.utils import convert_to_graphql_type
from api.schemas.generic_schema import DelInput, UpdatedGQL
from api.utils import setup_fields, IGNORE_FIELDS

# GQL TYPES

@strawberry.type
class FieldTypeGQL:
    """FieldType GraphQL Type."""
    oid: strawberry.ID
    label: str
    data_type: FieldTypes
    content: strawberry.scalars.JSON


@strawberry.type
class ProjectTemplateGQL:
    """ProjectTemplateType GraphQL Type."""
    oid: strawberry.ID
    name: str
    fields: Optional[List[FieldTypeGQL]] = strawberry.UNSET


@strawberry.type
class ProjectTypeGQL:
    """ProjectType GraphQL Type."""
    id: strawberry.ID
    name: str
    project_templates: Optional[List[ProjectTemplateGQL]] = strawberry.UNSET


# GQL INPUT FOR ADDING

@strawberry.input
class AddFieldTypeInput:
    """AddFieldTypeInput GraphQL Type."""
    label: str
    data_type: FieldTypes
    content: Optional[strawberry.scalars.JSON] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET


@strawberry.input
class AddProjectTemplateInput:
    """ProjectTemplateInput GraphQL Type."""
    name: str
    fields: Optional[List[AddFieldTypeInput]] = strawberry.UNSET


@strawberry.input
class AddProjectTypeInput:
    """ProjectTypeInput GraphQL Type."""
    name: str
    project_templates: Optional[List[AddProjectTemplateInput]] = strawberry.UNSET


#GQL INPUT FOR UPDATING

@strawberry.input
class UpdateFieldTypeInput:
    """UpdateFieldTypeInput GraphQL Type."""
    oid: Optional[strawberry.ID] = strawberry.UNSET
    label: Optional[str] = strawberry.UNSET
    data_type: Optional[FieldTypes] = strawberry.UNSET
    content: Optional[strawberry.scalars.JSON] = strawberry.UNSET
    description: Optional[str] = strawberry.UNSET
    mark_for_deletion: Optional[bool] = False


@strawberry.input
class UpdateProjectTemplateInput:
    """UpdateProjectTemplateInput GraphQL Type."""
    oid: Optional[strawberry.ID] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET
    fields: Optional[List[UpdateFieldTypeInput]] = strawberry.UNSET
    mark_for_deletion: Optional[bool] = False


@strawberry.input
class UpdateProjectTypeInput:
    """GraphQL Input for updating a Project Type."""
    id: strawberry.ID
    name: Optional[str] = strawberry.UNSET
    project_templates: Optional[List[UpdateProjectTemplateInput]] = strawberry.UNSET


# SETUP FUNCTIONS

def update_template_field(field_input: UpdateFieldTypeInput, project_template: ProjectTemplate):
    """Update an existing Field in ProjectTemplate."""
    current_field = project_template.fields.filter(oid=field_input.oid).get()
    if current_field:
        # Check if the field is marked for deletion
        if hasattr(field_input, "mark_for_deletion") and field_input.mark_for_deletion:
            index = project_template.fields.index(current_field)
            del project_template.fields[index]

        # Otherwise, the field will be updated
        else:
            setup_fields(field_input, IGNORE_FIELDS, current_field)


def setup_template_fields(fields: List[UpdateFieldTypeInput], project_template: ProjectTemplate):
    """Setup ProjectTemplate Fields for addition, updates, or deletion."""
    for field in fields:
        # If there is an ID, we should update an existing field
        if hasattr(field, "oid"):
            update_template_field(field, project_template)

        # Otherwise, we should add a new field to the current template
        else:
            new_field = setup_fields(field, IGNORE_FIELDS)
            project_template.fields.append(Field(**new_field))


def update_project_template(project_template_input: UpdateProjectTemplateInput, project_type: ProjectType):
    """Update an existing ProjectTemplate in ProjectType."""
    current_template = project_type.project_templates.filter(oid=project_template_input.oid).get()

    if current_template:
        # Check if the project_template is marked for deletion
        if project_template_input.mark_for_deletion:
            template_index = project_type.project_templates.index(current_template)
            del project_type.project_templates[template_index]

        # Otherwise, the project_template will be updated
        else:
            setup_fields(project_template_input, IGNORE_FIELDS, current_template)

            # Setup Project Template Fields
            if hasattr(project_template_input, "fields"):
                setup_template_fields(project_template_input.fields, current_template)

    project_type.save()



def setup_project_type_fields(
        project_type_input: AddProjectTypeInput | UpdateProjectTypeInput, project_type: ProjectType = None
    ):
    """Setup fields for ProjectTypes"""
    fields = setup_fields(project_type_input, IGNORE_FIELDS)

    # Setup Project Template
    if (
        hasattr(project_type_input, "project_templates")
        and project_type_input.project_templates is not strawberry.UNSET
    ):
        for project_template in project_type_input.project_templates:
            # If there is an OID, we should update an existing ProjectTemplate in the given ProjectType
            if hasattr(project_template, "oid") and project_type:
                update_project_template(project_template, project_type)

            # Otherwise, add a new ProjectTemplate
            else:
                templates = []
                new_proj_template = setup_fields(project_template, IGNORE_FIELDS)
                if hasattr(project_template, "fields") and project_template.fields is not strawberry.UNSET:
                    field_objects = []
                    for field in project_template.fields:
                        field_objects.append(Field(**setup_fields(field, IGNORE_FIELDS)))
                    new_proj_template["fields"] = field_objects
                templates.append(ProjectTemplate(**new_proj_template))
                fields["project_templates"] = templates
    return fields


# GQL QUERY

@strawberry.type
class ProjectTypeQuery:
    """ProjectTypeQuery GraphQL Type."""
    @strawberry.field
    def all_project_types(self) -> List[ProjectTypeGQL]:
        """Get all Projects."""
        return [convert_to_graphql_type(project_type, ProjectTypeGQL) for project_type in ProjectType.objects]

    @strawberry.field
    def user_project_types(self, info: strawberry.Info) -> List[ProjectTypeGQL]:
        """Get user's Project Types."""
        return [
            convert_to_graphql_type(project_type, ProjectTypeGQL)
            for project_type in ProjectType.objects(user=info.context.user)
        ]


# GQL MUTATIONS

@strawberry.type
class ProjectTypeMutation:
    """ProjectTypeMutation GraphQL Type."""

    @strawberry.mutation
    def add_project_type(self, info: strawberry.Info, project_type: AddProjectTypeInput) -> ProjectTypeGQL:
        """Add a new ProjectType to MongoDB."""
        fields = setup_project_type_fields(project_type)
        fields["user"] = info.context.user
        project = ProjectType(**fields).save()

        return convert_to_graphql_type(project, ProjectTypeGQL)

    # @strawberry.mutation
    # def add_project_types(self, project_types: List[AddProjectTypeInput]) -> List[ProjectTypeGQL]:
    #     """Add Multiple Project Types to MongoDB."""
    #     project_type_gqls = []
    #     for project_type in project_types:
    #         project_type_gqls.append(self.add_project_type(project_type))

    #     return project_type_gqls

    @strawberry.mutation
    def delete_project_type(self, info: strawberry.Info, project_type_input: DelInput) -> UpdatedGQL:
        """Delete a ProjectType from MongoDB."""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project_type = ProjectType.objects(
                        id=ObjectId(project_type_input.id),
                        user=info.context.user
                    ).first()
                except DoesNotExist:
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=project_type_input.id,
                        error="ProjectType document does not exist."
                    )

                try:
                    projects = Project.objects(project_type=project_type)
                    if projects:
                        projects.update(
                            unset__project_template=True
                        )
                    project_type.delete()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=project_type_input.id,
                        error=f"ProjectType document could not be deleted. Error: {e}"
                    )

        return UpdatedGQL(updated=True, oid=project_type_input.id, error=None)

    # @strawberry.mutation
    # def delete_project_types(self, project_types: List[DelInput]) -> List[UpdatedGQL]:
    #     """Delete multiple project types from MongoDB."""
    #     updated_types = []
    #     for project_type in project_types:
    #         updated_types.append(self.delete_project_type(project_type))

    #     return [convert_to_graphql_type(updated_type, UpdatedGQL) for updated_type in updated_types]

    @strawberry.mutation
    def update_project_type(self, info: strawberry.Info, project_type_input: UpdateProjectTypeInput) -> UpdatedGQL:
        """Update a ProjectType in MongoDB"""
        mongo = get_connection()

        with mongo.start_session() as session:
            with session.start_transaction():
                try:
                    project_type = ProjectType.objects(
                        id=ObjectId(project_type_input.id),
                        user=info.context.user
                    ).first()
                except DoesNotExist:
                    session.abort_transaction()
                    return UpdatedGQL(
                        updated=False,
                        oid=project_type_input.id,
                        error="ProjectType document does not exist.",
                    )

                fields = setup_project_type_fields(project_type_input, project_type)
                project_type.update(**fields)

                project_type.save()
        return UpdatedGQL(updated=True, oid=project_type_input.id, error=None)
