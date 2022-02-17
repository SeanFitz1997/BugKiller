from typing import Optional, List

from pydantic import validator, Field

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.model.types.arrow import ArrowType


class BugResolution(BkBaseModel):
    """ Details on a bug resolution """
    resolver_id: str = Field(description='The cognito id of the user who resolved the bug')
    resolved_on: ArrowType = Field(
        description='The datetime that the bug was resolved on as an ISO 8601 datetime string')


class Bug(BkBaseModel):
    """ A bug assigned to a project """
    id: str
    title: str
    description: str
    created_on: ArrowType = Field(description='The datetime that the bug was created on as an ISO 8601 datetime string')
    last_updated_on: ArrowType = Field(
        description='The datetime that the bug was last updated on as an ISO 8601 datetime string')
    tags: Optional[List[str]] = None
    resolved: Optional[BugResolution] = None

    @validator('tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))
