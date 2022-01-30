from abc import ABC
from typing import Optional

from bug_killer_schemas.models.bug import BugResolution


# 400 Exceptions

class MissingRequiredRequestParamException(Exception):

    def __init__(self, param_type: str, param_name: str):
        self.message = f'Missing required {param_type} parameter "{param_name}" in request'
        super().__init__(self.message)


class EmptyUpdateException(Exception):

    def __init__(self):
        self.message = 'No changes provided in update payload'
        super().__init__(self.message)


class NoChangesInUpdateException(Exception):

    def __init__(self):
        self.message = 'All changes in payload matches the existing record'
        super().__init__(self.message)


class AlreadyResolvedBugException(Exception):

    def __init__(self, bug_id: str, existing_resolution: BugResolution):
        self.message = f'Bug {bug_id} has already been resolved by {existing_resolution.resolver_id} ' \
                       f'on {existing_resolution.resolved_on}'
        super().__init__(self.message)


# 403 Exceptions

class MissingAuthHeaderException(Exception):

    def __init__(self):
        self.message = 'Missing authorization header value'
        super().__init__(self.message)


class UnauthorizedProjectAccessException(Exception, ABC):

    def __init__(self, user_id: str, operation: str, project_id: str):
        self.message = f'{user_id} does not have permission to {operation} project {project_id}'
        super().__init__(self.message)


class UnauthorizedProjectReadException(UnauthorizedProjectAccessException):

    def __init__(self, user_id: str, project_id: str):
        super().__init__(user_id, 'read', project_id)


class UnauthorizedProjectUpdateException(UnauthorizedProjectAccessException):

    def __init__(self, user_id: str, project_id: str):
        super().__init__(user_id, 'update', project_id)


# 404 Exceptions

class NotFoundException(Exception, ABC):

    def __init__(self, type: str, id: str):
        self.message = f'No {type} found with id: "{id}"'
        super().__init__(self.message)


class ProjectNotFoundException(NotFoundException):

    def __init__(self, id: str):
        super().__init__('project', id)


class BugNotFoundException(NotFoundException):

    def __init__(self, id: str):
        super().__init__('bug', id)


# 500 Exceptions

class ManagerNotFoundException(Exception):

    def __init__(self, project_id: str):
        self.message = f'No manager found for project {project_id}'
        super().__init__(self.message)


class MultipleMatchException(Exception, ABC):

    def __init__(self, type: str, id: Optional[str], match_count: Optional[int] = None):
        self.message = 'Unique constraint violation. ' \
                       f'Only 1 {type} {f"with {id = }" if id is not None else ""} is expected, ' \
                       f'but {"multiple" if match_count is None else match_count} were found'
        super().__init__(self.message)


class MultipleProjectMatchException(MultipleMatchException):

    def __init__(self, id: str, match_count: Optional[int] = None):
        super().__init__('project', id, match_count)


class MultipleBugMatchException(MultipleMatchException):

    def __init__(self, id: str, match_count: Optional[int] = None):
        super().__init__('bug', id, match_count)


class MultipleManagerMatchException(MultipleMatchException):

    def __init__(self, match_count: Optional[int] = None):
        super().__init__('manager', None, match_count)
