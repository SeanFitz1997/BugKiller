class MissingAuthHeaderException(Exception):

    def __init__(self):
        self.message = 'Missing authorization header value'


class MissingRequiredRequestParamException(Exception):

    def __init__(self, param_type: str, param_name: str):
        self.message = f'Missing required {param_type} parameter "{param_name}" in request'


class UnauthorizedProjectAccessException(Exception):

    def __init__(self, username: str, project_id: str):
        self.message = f'"{username}" does not have permission to make changes to project {project_id}'


class NotFoundException(Exception):

    def __init__(self, type: str, id: str):
        self.message = f'No {type} found with id: "{id}"'


class ProjectNotFoundException(NotFoundException):

    def __init__(self, id: str):
        super().__init__('project', id)


class BugNotFoundException(NotFoundException):

    def __init__(self, id: str):
        super().__init__('bug', id)
