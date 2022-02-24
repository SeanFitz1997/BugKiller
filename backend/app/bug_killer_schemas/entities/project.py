import uuid
from typing import List, Optional

import arrow
from arrow import Arrow
from pydantic import validator, Field

from bug_killer_app.util.entity import sort_by_create_date
from bug_killer_schemas.entities.bug import Bug
from bug_killer_schemas.test.doubles.default_values import mock_project_title, mock_project_description, \
    mock_manager_id, mock_project_tags, mock_team_members
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

    @classmethod
    def test_double(
            cls, *,
            project_id: Optional[str] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            manager: Optional[str] = None,
            created_on: Optional[Arrow] = None,
            last_updated_on: Optional[Arrow] = None,
            tags: Optional[List[str]] = None,
            members: Optional[List[str]] = None,
            bugs: Optional[List[Bug]] = None,
    ) -> 'Project':
        dt = arrow.utcnow().floor('second')
        return Project(
            id=project_id or str(uuid.uuid4()),
            title=title or mock_project_title,
            description=description or mock_project_description,
            manager=manager or mock_manager_id,
            created_on=created_on or dt,
            last_updated_on=last_updated_on or dt,
            tags=tags or mock_project_tags,
            members=members or mock_team_members,
            bugs=bugs or [Bug.test_double()]
        )
