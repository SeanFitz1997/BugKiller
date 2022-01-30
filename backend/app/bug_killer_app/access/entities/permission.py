from typing import NoReturn

from bug_killer_app.domain.exceptions import UnauthorizedProjectReadException, UnauthorizedProjectUpdateException
from bug_killer_app.models.project import BkAppProject


def assert_user_has_project_member_access(user_id: str, project: BkAppProject) -> NoReturn:
    if user_id != project.manager and user_id not in project.members:
        raise UnauthorizedProjectReadException(user_id, project.id)


def assert_user_has_project_manager_access(user_id: str, project: BkAppProject) -> NoReturn:
    if user_id != project.manager:
        raise UnauthorizedProjectUpdateException(user_id, project.id)
