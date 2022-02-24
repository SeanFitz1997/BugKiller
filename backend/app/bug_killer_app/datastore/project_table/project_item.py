from enum import Enum

from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from bug_killer_app.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer_app.datastore.project_table.user_project_gsi import UserProjectGsi
from bug_killer_app.domain.enviorment import DdbVariables


class ProjectAssociationPrefix(str, Enum):
    PROJECT = 'P'
    BUG = 'B'
    MANAGER = 'MA'
    MEMBER = 'ME'


class ProjectItem(Model):
    class Meta:
        table_name = DdbVariables.PROJECT_TABLE_NAME
        read_capacity_units = 1
        write_capacity_units = 1
        region = DdbVariables.TABLE_REGION


    # Table Keys
    project_id = UnicodeAttribute(attr_name=DdbVariables.AttributeNames.PROJECT_ID, hash_key=True)
    project_association = UnicodeAttribute(attr_name=DdbVariables.AttributeNames.PROJECT_ASSOCIATION, range_key=True)

    # Bug Attributes
    bug_resolution = BugResolutionMapAttribute(attr_name=DdbVariables.AttributeNames.BUG_RESOLUTION, null=True)

    # Common Attributes
    title = UnicodeAttribute(attr_name=DdbVariables.AttributeNames.TITLE, null=True)
    description = UnicodeAttribute(attr_name=DdbVariables.AttributeNames.DESCRIPTION, null=True)
    tags = UnicodeSetAttribute(attr_name=DdbVariables.AttributeNames.TAGS, null=True)
    created_on = UTCDateTimeAttribute(attr_name=DdbVariables.AttributeNames.CREATED_ON, null=True)
    last_updated_on = UTCDateTimeAttribute(attr_name=DdbVariables.AttributeNames.LAST_UPDATED_ON, null=True)

    # Indexes
    user_project_index = UserProjectGsi()
