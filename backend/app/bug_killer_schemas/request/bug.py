from dataclasses import dataclass
from typing import Optional, List

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class CreateBugPayload(DefaultDictCasting):
    project_id: str
    title: str
    description: str
    tags: Optional[List[str]] = None

    def __post_init__(self):
        self.tags = sorted(remove_duplicates_in_list(self.tags or []))


@dataclass
class UpdateBugPayload(DefaultDictCasting):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if self.tags:
            self.tags = sorted(remove_duplicates_in_list(self.tags or []))
