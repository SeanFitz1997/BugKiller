from typing import List

from pydantic import validator, Field

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.entities.bug import Bug
from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.model.types.arrow import ArrowType


class Project(BkBaseModel):
    """ A project to track a list of bugs """
    id: str
    title: str
    description: str
    manager: str = Field('The cognito user id of the project manager')
    created_on: ArrowType
    last_updated_on: ArrowType
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
