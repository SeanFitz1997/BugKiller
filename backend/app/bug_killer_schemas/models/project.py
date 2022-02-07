from typing import List

from pydantic import validator, Field

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.models.bug import Bug
from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.model.fields.arrow import ArrowField


class Project(BkBaseModel):
    id: str
    title: str
    description: str
    manager: str
    created_on: ArrowField
    last_updated_on: ArrowField
    tags: List[str] = Field(default_factory=list)
    members: List[str] = Field(default_factory=list)
    bugs: List[Bug] = Field(default_factory=list)

    @validator('tags', 'members')
    def set_lst_str_values(cls, value: List[str]) -> List[str]:
        return sorted(remove_duplicates_in_list(value))

    @validator('bugs')
    def set_bugs_str_values(cls, bugs: List[Bug]) -> List[Bug]:
        sort_by_create_date(bugs)
        return bugs
