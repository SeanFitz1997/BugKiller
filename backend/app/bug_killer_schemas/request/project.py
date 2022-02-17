from typing import Optional, List

from pydantic import Field, validator

from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel


class CreateProjectPayload(BkBaseModel):
    """ Payload used to create a new project """
    title: str = Field(description='The title of the project to create')
    description: str = Field(description='The title of the project to create')
    members: List[str] = Field(
        default_factory=list,
        description='List of members to be added to the project. It should be a list of cognito user ids'
    )
    tags: List[str] = Field(default_factory=list, description='List of tags to be added to the project to create')

    @validator('members', 'tags', pre=True)
    def set_values(cls, value: List[str]) -> List[str]:
        return sorted(remove_duplicates_in_list(value))


class UpdateProjectPayload(BkBaseModel):
    """ Payload used to update an existing project """
    title: Optional[str] = Field(None, description='The new title to set')
    description: Optional[str] = Field(None, description='The new description to set')
    manager: Optional[str] = Field(None, description='The cognito user id of the new manager of the project')
    members: Optional[List[str]] = Field(None, description='The new list of members that the project should have')
    tags: Optional[List[str]] = Field(None, description='The new list of tags to set')

    @validator('members', 'tags')
    def set_values(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        return sorted(remove_duplicates_in_list(value))
