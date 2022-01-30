from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

from bug_killer_app.domain.enviorment import DdbVariables


class UserProjectGsi(GlobalSecondaryIndex):
    class Meta:
        index_name = DdbVariables.USER_PROJECT_GSI_NAME
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()


    project_association = UnicodeAttribute(attr_name=DdbVariables.AttributeNames.PROJECT_ASSOCIATION, hash_key=True)
