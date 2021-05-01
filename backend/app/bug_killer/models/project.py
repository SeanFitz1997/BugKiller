from datetime import datetime
from typing import List, Optional, Set

import arrow
from pydantic import BaseModel

from bug_killer.datastore.project_item import ProjectItem
from bug_killer.models.bug import Bug
from bug_killer.models.user import User


class Project(BaseModel):
    id: str
    title: str
    description: str
    tags: Set[str]
    created_on: datetime
    last_updated_on: datetime
    manager: Optional[User] = None
    team: Optional[List[User]] = None
    bugs: Optional[List[Bug]] = None


    @staticmethod
    def from_db_item(db_item: ProjectItem) -> 'Project':
        return Project(
            id=db_item.project_id,
            title=db_item.title,
            description=db_item.description,
            tags=db_item.tags,
            created_on=arrow.get(db_item.created_on).datetime,
            last_updated_on=arrow.get(db_item.last_updated_on).datetime
        )
