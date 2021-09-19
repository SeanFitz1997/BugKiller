from typing import Any, Dict, List, Optional

from bug_killer.models.entities.project import Project


class CreateProjectPayload:

    def __init__(
            self,
            title: str,
            description: str,
            manager: str,
            members: Optional[List[str]] = [],
            tags: Optional[List[str]] = [],
    ):
        self.title = title
        self.description = description
        self.manager = manager
        self.members = members
        self.tags = tags

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CreateProjectPayload":
        return CreateProjectPayload(
            title=data["title"],
            description=data["description"],
            manager=data["manager"],
            members=data["members"],
            tags=data["tags"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "manager": self.manager,
            "members": self.members,
            "tags": self.tags,
        }

    def __repr__(self) -> str:
        return str(self.to_dict())


class UserProjectsResponse:

    def __init__(
            self,
            manger_projects: Optional[List[Project]] = None,
            member_projects: Optional[List[Project]] = None
    ):
        self.manger_projects = manger_projects or []
        self.member_projects = member_projects or []

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UserProjectsResponse":
        return UserProjectsResponse(
            manger_projects=data["managerProjects"],
            member_projects=data["memberProjects"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "managerProjects": [project.to_dict() for project in self.manger_projects],
            "memberProjects": [project.to_dict() for project in self.member_projects],
        }

    def __repr__(self) -> str:
        return str(self.to_dict())


class UpdateProjectPayload:

    def __init__(
            self,
            project_id: str,
            actor: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            manager: Optional[str] = None,
    ):
        self.project_id = project_id
        self.actor = actor
        self.title = title
        self.description = description
        self.manager = manager

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UpdateProjectPayload":
        return UpdateProjectPayload(
            project_id=data["projectId"],
            actor=data['actor'],
            title=data.get("title"),
            description=data.get("description"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "projectId": self.project_id,
            'actor': self.actor,
            "title": self.title,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return str(self.to_dict())


class ProjectResponse:

    def __init__(self, project: Project):
        self.project = project

    def to_dict(self) -> Dict[str, Any]:
        return {"project": self.project.to_dict()}

    def __repr__(self) -> str:
        return str(self.to_dict())


class DeleteProjectPayload:

    def __init__(self, actor: str, project_id: str):
        self.actor = actor
        self.project_id = project_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'actor': self.actor,
            'projectId': self.project_id
        }

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'DeleteProjectPayload':
        return DeleteProjectPayload(actor=data['actor'], project_id=data['projectId'])

    def __repr__(self) -> str:
        return str(self.to_dict())
