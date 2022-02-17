from typing import List

from pydantic import Field, validator

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.entities.project import Project
from bug_killer_utils.model.bk_base_model import BkBaseModel


class UserProjectsResponse(BkBaseModel):
    """ Details on all the projects that the user is a member or manager of """
    manager_projects: List[Project] = Field(default_factory=list)
    member_projects: List[Project] = Field(default_factory=list)

    @validator('manager_projects', 'member_projects')
    def set_values(cls, projects: List[Project]) -> List[Project]:
        sort_by_create_date(projects)
        return projects


class ProjectResponse(BkBaseModel):
    """ Details on a single project """
    project: Project
