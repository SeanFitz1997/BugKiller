from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from arrow import Arrow

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.dates import to_utc_str, try_parse_arrow
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class BugResolution(DefaultDictCasting):
    resolver_id: str
    resolved_on: Arrow

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['resolvedOn'] = to_utc_str(self.resolved_on)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BugResolution':
        data['resolvedOn'] = try_parse_arrow(data['resolvedOn'])
        return super().from_dict(data)


@dataclass
class Bug(DefaultDictCasting):
    id: str
    title: str
    description: str
    created_on: Arrow
    last_updated_on: Arrow
    tags: Optional[List[str]] = None
    resolved: Optional[BugResolution] = None

    _BUG_RESOLUTION_CLS = BugResolution

    def __post_init__(self):
        self.tags = sorted(remove_duplicates_in_list(self.tags or []))

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['createdOn'] = to_utc_str(self.created_on)
        data['lastUpdatedOn'] = to_utc_str(self.last_updated_on)
        data['resolved'] = self.resolved.to_dict() if self.resolved else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bug':
        data['createdOn'] = try_parse_arrow(data['createdOn'])
        data['lastUpdatedOn'] = try_parse_arrow(data['lastUpdatedOn'])
        data['resolved'] = Bug._BUG_RESOLUTION_CLS.from_dict(data['resolved']) if data.get('resolved') else None
        return super().from_dict(data)
