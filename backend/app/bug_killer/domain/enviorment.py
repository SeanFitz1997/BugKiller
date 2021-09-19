import os


class DdbVariables:
    class Defaults:
        PROJECT_TABLE_NAME = 'projectTable'
        USER_PROJECT_GSI_NAME = 'userProjectGsi'


    PROJECT_TABLE_NAME = os.environ.get('PROJECT_TABLE_NAME', Defaults.PROJECT_TABLE_NAME)
    USER_PROJECT_GSI_NAME = os.environ.get('USER_PROJECT_GSI_NAME', Defaults.USER_PROJECT_GSI_NAME)
