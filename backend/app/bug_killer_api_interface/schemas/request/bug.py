import uuid
from typing import Optional, List

from pydantic import validator, Field

from bug_killer_api_interface.test.test_doubles.default_values import mock_bug_title, mock_bug_description, \
    mock_bug_tags
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

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            project_id: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[List[str]] = None
    ) -> 'CreateBugPayload':
        return cls(
            project_id=project_id or str(uuid.uuid4()),
            title=title or mock_bug_title,
            description=description or mock_bug_description,
            tags=tags or mock_bug_tags
        )


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

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            title: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[List[str]] = None,
    ) -> 'UpdateBugPayload':
        return UpdateBugPayload(
            title=title or mock_bug_title,
            description=description or mock_bug_description,
            tags=tags or mock_bug_tags
        )
