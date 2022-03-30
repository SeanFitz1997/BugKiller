from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from bug_killer_api_interface.schemas.entities.bug import BugResolution
from bug_killer_app.domain.enums import ResourceType, ParameterType
from bug_killer_app.domain.response import HttpResponse, message_body
from bug_killer_utils.http import HttpStatusCode


class ApiException(Exception, ABC):
    """ Base API Exception class that define the interface for API exceptions must follow """

    @abstractmethod
    def get_message(self) -> str:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_status_code(cls) -> HttpStatusCode:
        raise NotImplementedError()

    def get_api_response(self) -> HttpResponse:
        return HttpResponse(status_code=self.get_status_code(), body=message_body(self.get_message()))


# 400 Exceptions
class BadRequestApiException(ApiException, ABC):

    @classmethod
    def get_status_code(cls) -> HttpStatusCode:
        return HttpStatusCode.BAD_REQUEST_STATUS


class MissingRequiredRequestParamException(BadRequestApiException):

    def __init__(self, param_type: ParameterType, param_name: str):
        super().__init__()
        self.param_type = param_type
        self.param_name = param_name

    def get_message(self) -> str:
        return f'Missing required {self.param_type.value} parameter "{self.param_name}" in request'


class EmptyUpdateException(BadRequestApiException):

    def get_message(self) -> str:
        return 'No changes provided in update payload'


class NoChangesInUpdateException(BadRequestApiException):

    def get_message(self) -> str:
        return 'All changes in payload matches the existing record'


class AlreadyResolvedBugException(BadRequestApiException):

    def __init__(self, bug_id: str, existing_resolution: BugResolution):
        super().__init__()
        self.bug_id = bug_id
        self.existing_resolution = existing_resolution

    def get_message(self) -> str:
        return f'Bug {self.bug_id} has already been resolved by {self.existing_resolution.resolver_id} ' \
               f'on {self.existing_resolution.resolved_on}'


# 401 Exceptions
class UnauthorizedApiException(ApiException, ABC):

    @classmethod
    def get_status_code(cls) -> HttpStatusCode:
        return HttpStatusCode.UNAUTHORIZED_STATUS


class MissingAuthHeaderException(UnauthorizedApiException):

    def get_message(self) -> str:
        return 'Missing authorization header value'


# 403 Exceptions
class ForbiddenApiException(ApiException, ABC):

    @classmethod
    def get_status_code(cls) -> HttpStatusCode:
        return HttpStatusCode.FORBIDDEN_STATUS


class UnauthorizedProjectAccessException(ForbiddenApiException, ABC):
    class ProjectOperation(str, Enum):
        READ = 'read'
        UPDATE = 'update'


    def __init__(self, user_id: str, project_id: str, operation: ProjectOperation):
        super().__init__()
        self.user_id = user_id
        self.project_id = project_id
        self.operation = operation

    def get_message(self) -> str:
        return f'{self.user_id} does not have permission to {self.operation.value} project {self.project_id}'


class UnauthorizedProjectReadException(UnauthorizedProjectAccessException):

    def __init__(self, user_id: str, project_id: str):
        super().__init__(user_id, project_id, UnauthorizedProjectAccessException.ProjectOperation.READ)


class UnauthorizedProjectUpdateException(UnauthorizedProjectAccessException):

    def __init__(self, user_id: str, project_id: str):
        super().__init__(user_id, project_id, UnauthorizedProjectAccessException.ProjectOperation.UPDATE)


# 404 Exceptions
class NotFoundApiException(ApiException, ABC):

    @classmethod
    def get_status_code(cls) -> HttpStatusCode:
        return HttpStatusCode.NOT_FOUND_STATUS


class ResourceNotFoundException(NotFoundApiException, ABC):

    def __init__(self, resource_type: ResourceType, resource_id: str):
        super().__init__()
        self.resource_type = resource_type
        self.resource_id = resource_id

    def get_message(self) -> str:
        return f'No {self.resource_type.value} found with id: "{self.resource_id}"'


class ProjectNotFoundException(ResourceNotFoundException):

    def __init__(self, resource_id: str):
        super().__init__(ResourceType.PROJECT, resource_id)


class BugNotFoundException(ResourceNotFoundException):

    def __init__(self, resource_id: str):
        super().__init__(ResourceType.BUG, resource_id)


# 500 Exceptions
class InternalServerErrorApiException(ApiException, ABC):

    @classmethod
    def get_status_code(cls) -> HttpStatusCode:
        return HttpStatusCode.INTERNAL_SERVER_ERROR_STATUS


class ManagerNotFoundException(InternalServerErrorApiException):

    def __int__(self, project_id: str):
        super().__init__()
        self.project_id = project_id

    def get_message(self) -> str:
        return f'No manager found for project {self.project_id}'


class MultipleMatchException(InternalServerErrorApiException, ABC):

    def __init__(self, resource_type: ResourceType, resource_id: Optional[str], match_count: Optional[int]):
        super().__init__()
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.match_count = match_count

    def get_message(self) -> str:
        id_message = f" with ID: {self.resource_id}" if self.resource_id is not None else ""
        match_count_message = str(self.match_count) if self.match_count is not None else 'multiple'
        return 'Unique constraint violation. ' \
               f'Only 1 {self.resource_type.value}{id_message} is expected, ' \
               f'but {match_count_message} were found'


class MultipleProjectMatchException(MultipleMatchException):

    def __init__(self, resource_id: str, match_count: Optional[int] = None):
        super().__init__(ResourceType.PROJECT, resource_id, match_count)


class MultipleBugMatchException(MultipleMatchException):

    def __init__(self, resource_id: str, match_count: Optional[int] = None):
        super().__init__(ResourceType.BUG, resource_id, match_count)


class MultipleManagerMatchException(MultipleMatchException):

    def __init__(self, resource_id: Optional[str] = None, match_count: Optional[int] = None):
        super().__init__(ResourceType.MANAGER, resource_id, match_count)
