from datetime import datetime
from typing import Optional, Set

import arrow
from pydantic import BaseModel

from bug_killer.datastore.project_item import ProjectItem
from bug_killer.models.bug_resolution import BugResolution


class Bug(BaseModel):
    id: str
    title: str
    description: str
    tags: Set[str]
    created_on: datetime
    last_updated_on: datetime
    resolved: Optional[BugResolution] = None


    @staticmethod
    def from_db_item(db_item: ProjectItem) -> 'Bug':
        bug_id = db_item.project_bug_user_id.split(ProjectItem.BUG_SK_PREFIX, maxsplit=1)[-1]
        bug_resolution = None  # BugResolution.from_db_attribute(db_item.bug_resolution) if db_item.bug_resolution else None

        return Bug(
            id=bug_id,
            title=db_item.title,
            description=db_item.description,
            tags=db_item.tags,
            created_on=arrow.get(db_item.created_on).datetime,
            last_updated_on=arrow.get(db_item.last_updated_on).datetime,
            resolved=bug_resolution
        )
