from dataclasses import dataclass
from typing import Optional, List

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class CreateProjectPayload(DefaultDictCasting):
    title: str
    description: str
    members: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        self.members = sorted(remove_duplicates_in_list(self.members or []))
        self.tags = sorted(remove_duplicates_in_list(self.tags or []))


@dataclass
class UpdateProjectPayload(DefaultDictCasting):
    title: Optional[str] = None
    description: Optional[str] = None
    manager: Optional[str] = None
    members: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if self.members:
            self.members = sorted(remove_duplicates_in_list(self.members))

        if self.tags:
            self.tags = sorted(remove_duplicates_in_list(self.tags))
