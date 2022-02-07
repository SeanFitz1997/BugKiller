from typing import Optional, List

from pydantic import validator

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.model.fields.arrow import ArrowField


class BugResolution(BkBaseModel):
    resolver_id: str
    resolved_on: ArrowField


class Bug(BkBaseModel):
    id: str
    title: str
    description: str
    created_on: ArrowField
    last_updated_on: ArrowField
    tags: Optional[List[str]] = None
    resolved: Optional[BugResolution] = None

    @validator('tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))
  