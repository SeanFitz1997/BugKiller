from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.models.project import Project
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class UserProjectsResponse(DefaultDictCasting):
    manager_projects: Optional[List[Project]] = None
    member_projects: Optional[List[Project]] = None

    _PROJECT_CLS = Project

    def __post_init__(self):
        self.manager_projects = self.manager_projects or []
        self.member_projects = self.member_projects or []

        sort_by_create_date(self.manager_projects)
        sort_by_create_date(self.member_projects)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['managerProjects'] = [project.to_dict() for project in self.manager_projects]
        data['memberProjects'] = [project.to_dict() for project in self.member_projects]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProjectsResponse':
        data['managerProjects'] = [UserProjectsResponse._PROJECT_CLS.from_dict(project_data)
                                   for project_data in data['managerProjects']]
        data['memberProjects'] = [UserProjectsResponse._PROJECT_CLS.from_dict(project_data)
                                  for project_data in data['memberProjects']]
        return super().from_dict(data)


@dataclass
class ProjectResponse(DefaultDictCasting):
    project: Project

    _PROJECT_CLS = Project

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['project'] = self.project.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        data['project'] = ProjectResponse._PROJECT_CLS.from_dict(data['project'])
        return super().from_dict(data)
