import os


class DdbVariables:
    class Defaults:
        PROJECT_TABLE_NAME = 'projectTable'
        USER_PROJECT_GSI_NAME = 'userProjectGsi'
        TABLE_REGION = 'eu-west-1'


    class AttributeNames:
        # Table Keys
        PROJECT_ID = 'pi'
        PROJECT_ASSOCIATION = 'pa'

        # Bug Attributes
        BUG_RESOLUTION = 'br'

        # Common Attributes
        TITLE = 't'
        DESCRIPTION = 'd'
        CREATED_ON = 'co'
        LAST_UPDATED_ON = 'lu'
        TAGS = 'tg'


    PROJECT_TABLE_NAME = os.environ.get('PROJECT_TABLE_NAME', Defaults.PROJECT_TABLE_NAME)
    USER_PROJECT_GSI_NAME = os.environ.get('USER_PROJECT_GSI_NAME', Defaults.USER_PROJECT_GSI_NAME)
    TABLE_REGION = os.environ.get('TABLE_REGION', Defaults.TABLE_REGION)
