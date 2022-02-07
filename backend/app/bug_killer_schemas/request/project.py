from typing import Optional, List

from pydantic import Field, validator

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel


class CreateProjectPayload(BkBaseModel):
    title: str
    description: str
    members: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @validator('members', 'tags', pre=True)
    def set_values(cls, value: List[str]) -> List[str]:
        return sorted(remove_duplicates_in_list(value))


class UpdateProjectPayload(BkBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    manager: Optional[str] = None
    members: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    @validator('members', 'tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))
