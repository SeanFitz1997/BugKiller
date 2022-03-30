from typing import Optional, List

from pydantic import Field, validator

from bug_killer_api_interface.test.test_doubles.default_values import mock_project_title, mock_project_description, \
    mock_project_tags, mock_member_id
from bug_killer_app.test.test_doubles.default_values import mock_manager_id
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

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            title: Optional[str] = None,
            description: Optional[str] = None,
            members: Optional[List[str]] = None,
            tags: Optional[List[str]] = None
    ) -> 'CreateProjectPayload':
        return cls(
            title=title or mock_project_title,
            description=description or mock_project_description,
            members=members or [mock_member_id],
            tags=tags or mock_project_tags
        )


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

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            title: Optional[str] = None,
            description: Optional[str] = None,
            manager: Optional[str] = None,
            members: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
    ) -> 'UpdateProjectPayload':
        return cls(
            title=title or mock_project_title,
            description=description or mock_project_description,
            manager=manager or mock_manager_id,
            members=members or [mock_member_id],
            tags=tags or mock_project_tags
        )
