from typing import Any, Dict, Optional, Set

import arrow
from arrow import Arrow

from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.models.entities.bug_resolution import BugResolution
from bug_killer.util.dates import to_utc_str
from bug_killer.util.entity import remove_prefix


class Bug:

    def __init__(
            self,
            id: str,
            title: str,
            description: str,
            tags: Set[str],
            created_on: Arrow,
            last_updated_on: Arrow,
            resolved: Optional[BugResolution] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags
        self.created_on = created_on
        self.last_updated_on = last_updated_on
        self.resolved = resolved

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Bug":
        return Bug(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            tags=data["tags"],
            created_on=arrow.get(data["createdOn"]),
            last_updated_on=arrow.get(data["lastUpdatedOn"]),
            resolved=data["resolved"],
        )

    @staticmethod
    def from_db_item(db_item: ProjectItem) -> "Bug":
        bug_id = remove_prefix(
            ProjectItem.BUG_SK_PREFIX, db_item.project_bug_manager_member_id
        )
        bug_resolution = (
            BugResolution.from_db_attribute(db_item.bug_resolution)
            if db_item.bug_resolution
            else None
        )
        return Bug(
            id=bug_id,
            title=db_item.title,
            description=db_item.description,
            tags=db_item.tags,
            created_on=arrow.get(db_item.created_on),
            last_updated_on=arrow.get(db_item.last_updated_on),
            resolved=bug_resolution,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tags": list(self.tags),
            "createdOn": to_utc_str(self.created_on),
            "lastUpdatedOn": to_utc_str(self.last_updated_on),
            "resolved": self.resolved.to_dict() if self.resolved else None,
        }

    def __repr__(self) -> str:
        return str(self.to_dict())
