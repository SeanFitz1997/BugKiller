from typing import Optional, List

from bug_killer_schemas.models.project import Project
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse
from bug_killer_schemas.test.doubles.models.project import create_test_project


def create_test_user_projects_rsp(
        manager_projects: Optional[List[Project]] = None,
        member_projects: Optional[List[Project]] = None
) -> UserProjectsResponse:
    return UserProjectsResponse(
        manager_projects=manager_projects or [create_test_project()],
        member_projects=member_projects or [create_test_project()]
    )


def create_test_project_rsp(project: Optional[Project] = None) -> ProjectResponse:
    return ProjectResponse(
        project=project or create_test_project()
    )
