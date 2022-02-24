import uuid
from typing import Optional, List

import arrow
from arrow import Arrow
from pydantic import validator, Field

from bug_killer_schemas.test.doubles.default_values import mock_user_id, mock_bug_title, mock_bug_description, \
    mock_bug_tags
from bug_killer_utils.collections import remove_duplicates_in_list
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.model.types.arrow import ArrowType


class BugResolution(BkBaseModel):
    """ Details on a bug resolution """
    resolver_id: str = Field(description='The cognito id of the user who resolved the bug')
    resolved_on: ArrowType = Field(
        description='The datetime that the bug was resolved on as an ISO 8601 datetime string')

    @classmethod
    def test_double(
            cls, *,
            resolver_id: Optional[str] = None,
            resolved_on: Optional[Arrow] = None
    ) -> 'BkAppBugResolution':
        dt = arrow.utcnow().floor('second')
        return cls(resolver_id=resolver_id or mock_user_id, resolved_on=resolved_on or dt)


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

    @classmethod
    def test_double(
            cls, *,
            bug_id: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            tags: Optional[List[str]] = None,
            created_on: Optional[Arrow] = None,
            last_updated_on: Optional[Arrow] = None,
            resolved: Optional[BugResolution] = None,
    ) -> 'Bug':
        dt = arrow.utcnow().floor('second')
        return Bug(
            id=bug_id or str(uuid.uuid4()),
            title=title or mock_bug_title,
            description=description or mock_bug_description,
            tags=tags or mock_bug_tags,
            created_on=created_on or dt,
            last_updated_on=last_updated_on or dt,
            resolved=resolved,
        )
