from typing import Optional, List

from pydantic import validator, Field

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel


class CreateBugPayload(BkBaseModel):
    """ Details to create a new bug for a project """
    project_id: str = Field(description='The id of the project to add the bug to')
    title: str = Field(description='The title of the bug to create')
    description: str = Field(description='The description of the bug to create')
    tags: Optional[List[str]] = Field(None, description='List of tags to be added to the bug to create')

    @validator('tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))


class UpdateBugPayload(BkBaseModel):
    """ Details to update an existing bug """
    title: Optional[str] = Field(None, description='The new title to se')
    description: Optional[str] = Field(None, description='The new description to set')
    tags: Optional[List[str]] = Field(None, description='The list of tags to set')

    @validator('tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))
