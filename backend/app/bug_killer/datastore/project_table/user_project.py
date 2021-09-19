from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

from bug_killer.domain.enviorment import DdbVariables


class UserProjectGsi(GlobalSecondaryIndex):
    class Meta:
        index_name = DdbVariables.USER_PROJECT_GSI_NAME
        read_capacity_units = 1
        write_capacity_units = 1
        projection = KeysOnlyProjection()


    project_bug_manager_member_id = UnicodeAttribute(hash_key=True)
