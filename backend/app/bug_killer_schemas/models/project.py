from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from arrow import Arrow

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.models.bug import Bug
from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.dates import to_utc_str, try_parse_arrow
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class Project(DefaultDictCasting):
    id: str
    title: str
    description: str
    manager: str
    created_on: Arrow
    last_updated_on: Arrow
    tags: Optional[List[str]] = None
    members: Optional[List[str]] = None
    bugs: Optional[List[Bug]] = None

    _BUG_CLS = Bug

    def __post_init__(self):
        self.tags = sorted(remove_duplicates_in_list(self.tags or []))
        self.members = sorted(remove_duplicates_in_list(self.members or []))

        self.bugs = self.bugs or []
        sort_by_create_date(self.bugs)

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['createdOn'] = to_utc_str(self.created_on)
        data['lastUpdatedOn'] = to_utc_str(self.last_updated_on)
        data['bugs'] = [bug.to_dict() for bug in self.bugs]

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        data['createdOn'] = try_parse_arrow(data['createdOn'])
        data['lastUpdatedOn'] = try_parse_arrow(data['lastUpdatedOn'])
        data['bugs'] = [Project._BUG_CLS.from_dict(bug_data) for bug_data in data['bugs']]

        return super().from_dict(data)
