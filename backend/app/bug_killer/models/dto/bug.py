from typing import Any, Dict, Optional, Set

from bug_killer.models.entities.bug import Bug


class CreateBugPayload:

    def __init__(
            self,
            actor: str,
            project_id: str,
            title: str,
            description: str,
            tags: Optional[Set[str]] = None,
    ):
        self.actor = actor
        self.project_id = project_id
        self.title = title
        self.description = description
        self.tags = tags

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CreateBugPayload":
        return CreateBugPayload(
            actor=data['actor'],
            project_id=data["projectId"],
            title=data["title"],
            description=data["description"],
            tags=set(data.get("tags")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'actor': self.actor,
            "projectId": self.project_id,
            "title": self.title,
            "description": self.description,
            "tags": list(self.tags) if self.tags else None,
        }

    def __repr__(self) -> str:
        return str(self.to_dict())


class DeleteBugPayload:

    def __init__(self, actor: str, project_id: str, bug_id: str):
        self.actor = actor
        self.project_id = project_id
        self.bug_id = bug_id

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeleteBugPayload":
        return DeleteBugPayload(
            actor=data['actor'],
            project_id=data["projectId"],
            bug_id=data["bug_id"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'actor': self.actor,
            "projectId": self.project_id,
            "bugId": self.bug_id
        }

    def __repr__(self) -> str:
        return str(self.to_dict())


class BugResponse:

    def __init__(self, project_id: str, bug: Bug):
        self.project_id = project_id
        self.bug = bug

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BugResponse":
        return BugResponse(
            project_id=data["project_id"],
            bug=data["bug"]
            if isinstance(data["bug"], Bug)
            else Bug.from_dict(data["bug"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"projectId": self.project_id, "bug": self.bug.to_dict()}

    def __repr__(self) -> str:
        return str(self.to_dict())
