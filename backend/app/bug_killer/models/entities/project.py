from typing import Any, Dict, List, Optional

import arrow
from arrow import Arrow

from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.models.entities.bug import Bug
from bug_killer.util.dates import to_utc_str
from bug_killer.util.entity import remove_prefix
from bug_killer.util.type_util import OptionalProjectItems


class Project:

    def __init__(
            self,
            id: str,
            title: str,
            description: str,
            tags: List[str],
            created_on: Arrow,
            last_updated_on: Arrow,
            manager: Optional[str] = None,
            members: Optional[List[str]] = None,
            bugs: Optional[List[Bug]] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags
        self.created_on = created_on
        self.last_updated_on = last_updated_on
        self.manager = manager
        self.members = members
        self.bugs = bugs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tags": list(self.tags) if self.tags else None,
            "createdOn": to_utc_str(self.created_on),
            "lastUpdatedOn": to_utc_str(self.last_updated_on),
            "manager": self.manager,
            "members": self.members,
            'bugs': [bug.to_dict() for bug in self.bugs] if self.bugs is not None else None
        }

    def __repr__(self) -> str:
        return str(self.to_dict())

    @staticmethod
    def from_db_items(
            project_item: ProjectItem,
            manager_item: Optional[ProjectItem] = None,
            member_items: Optional[List[ProjectItem]] = None,
            bug_items: Optional[List[ProjectItem]] = None,
    ) -> "Project":
        manager = remove_prefix(ProjectItem.MANAGER_SK_PREFIX, manager_item.project_bug_manager_member_id) \
            if manager_item else None

        members = [
            remove_prefix(ProjectItem.MEMBER_SK_PREFIX, member.project_bug_manager_member_id)
            for member in member_items
        ] if member_items is not None else None

        bugs = [Bug.from_db_item(bug) for bug in bug_items] if bug_items is not None else None

        return Project(
            id=project_item.project_id,
            title=project_item.title,
            description=project_item.description,
            tags=project_item.tags,
            created_on=arrow.get(project_item.created_on),
            last_updated_on=arrow.get(project_item.last_updated_on),
            manager=manager,
            members=members,
            bugs=bugs,
        )

    def to_db_items(self) -> OptionalProjectItems:
        project_item = ProjectItem(
            project_id=self.id,
            project_bug_manager_member_id=ProjectItem.PROJECT_SK_PREFIX + self.id,
            title=self.title,
            description=self.description,
            created_on=self.created_on,
            last_updated_on=self.last_updated_on,
            tags=self.tags,
        )

        manager_item = (
            ProjectItem(self.id, ProjectItem.MANAGER_SK_PREFIX + self.manager)
            if self.manager
            else None
        )

        member_items = (
            [
                ProjectItem(self.id, ProjectItem.MEMBER_SK_PREFIX + member)
                for member in self.members
            ]
            if self.members
            else None
        )

        bug_items = (
            [
                ProjectItem(
                    project_id=self.id,
                    project_bug_manager_member_id=ProjectItem.BUG_SK_PREFIX + bug.id,
                    title=bug.title,
                    description=bug.description,
                    created_on=bug.created_on,
                    last_updated_on=bug.last_updated_on,
                    tags=bug.tags,
                    bug_resolution=None,  # TODO Add attribute data
                )
                for bug in self.bugs
            ]
            if self.bugs
            else None
        )

        return project_item, manager_item, member_items, bug_items
