from typing import List, Optional

from pydantic import Field, validator

from bug_killer_api_interface.schemas.entities.project import Project
from bug_killer_utils.model.bk_base_model import BkBaseModel


class UserProjectsResponse(BkBaseModel):
    """ Details on all the projects that the user is a member or manager of """
    manager_projects: List[Project] = Field(default_factory=list)
    member_projects: List[Project] = Field(default_factory=list)

    @validator('manager_projects', 'member_projects')
    def set_values(cls, projects: List[Project]) -> List[Project]:
        projects.sort(key=lambda x: x.created_on, reverse=True)
        return projects

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            manager_projects: Optional[List[Project]] = None,
            member_projects: Optional[List[Project]] = None
    ) -> 'UserProjectsResponse':
        return UserProjectsResponse(
            manager_projects=manager_projects or [Project.test_double()],
            member_projects=member_projects or [Project.test_double()]
        )


class ProjectResponse(BkBaseModel):
    """ Details on a single project """
    project: Project

    @classmethod
    def test_double(cls, *, project: Optional[Project] = None) -> 'ProjectResponse':  # type: ignore[override]
        return ProjectResponse(
            project=project or Project.test_double()
        )
