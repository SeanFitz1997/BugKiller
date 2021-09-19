from pynamodb.attributes import (
    UnicodeAttribute,
    UnicodeSetAttribute,
    UTCDateTimeAttribute
)
from pynamodb.models import Model

from bug_killer.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer.datastore.project_table.user_project import UserProjectGsi
from bug_killer.domain.enviorment import DdbVariables


class ProjectItem(Model):
    class Meta:
        table_name = DdbVariables.PROJECT_TABLE_NAME
        read_capacity_units = 1
        write_capacity_units = 1
        region = "eu-west-1"


    PROJECT_SK_PREFIX = "P"
    BUG_SK_PREFIX = "B"
    MANAGER_SK_PREFIX = "MA"
    MEMBER_SK_PREFIX = "ME"

    # Table Keys
    project_id = UnicodeAttribute(hash_key=True)
    project_bug_manager_member_id = UnicodeAttribute(range_key=True)

    # Bug Attributes
    bug_resolution = BugResolutionMapAttribute(null=True)

    # Common Attributes
    title = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    created_on = UTCDateTimeAttribute(null=True)
    last_updated_on = UTCDateTimeAttribute(null=True)
    tags = UnicodeSetAttribute(null=True)

    # Indexes
    user_project_index = UserProjectGsi()
