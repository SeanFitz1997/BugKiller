from typing import List, Optional

import arrow

from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.domain.types import AllProjectItems
from bug_killer_app.models.bug import BkAppBug
from bug_killer_api_interface.schemas.entities.project import Project
from bug_killer_utils.strings import remove_prefix


class BkAppProject(Project):

    @classmethod
    def from_db_items(
            cls: type,
            project_item: ProjectItem,
            manager_item: ProjectItem,
            member_items: Optional[List[ProjectItem]] = None,
            bug_items: Optional[List[ProjectItem]] = None,
    ) -> 'BkAppProject':
        manager = remove_prefix(ProjectAssociationPrefix.MANAGER.value, manager_item.project_association)
        tags = list(project_item.tags) if project_item.tags else []

        members = [
            remove_prefix(ProjectAssociationPrefix.MEMBER.value, member.project_association)
            for member in member_items
        ] if member_items else []

        bugs = [BkAppBug.from_db_item(bug) for bug in bug_items] if bug_items else []

        return cls(
            id=project_item.project_id,
            title=project_item.title,
            description=project_item.description,
            tags=tags,
            created_on=arrow.get(project_item.created_on),
            last_updated_on=arrow.get(project_item.last_updated_on),
            manager=manager,
            members=members,
            bugs=bugs,
        )

    def to_db_items(self) -> AllProjectItems:
        if all(isinstance(bug, BkAppBug) for bug in self.bugs):
            bug_items = [bug.to_db_item(project_id=self.id) for bug in self.bugs]  # type: ignore[attr-defined]
        else:
            raise ValueError(f'BkAppProject bugs must be a list of BkAppBug')

        project_item = ProjectItem(
            project_id=self.id,
            project_association=ProjectAssociationPrefix.PROJECT.value + self.id,
            title=self.title,
            description=self.description,
            created_on=self.created_on,
            last_updated_on=self.last_updated_on,
            tags=self.tags,
        )

        manager_item = ProjectItem(self.id, ProjectAssociationPrefix.MANAGER.value + self.manager)

        member_items = [
            ProjectItem(self.id, ProjectAssociationPrefix.MEMBER.value + member)
            for member in self.members
        ]

        return project_item, manager_item, member_items, bug_items
