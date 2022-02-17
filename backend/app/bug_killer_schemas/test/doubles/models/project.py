import uuid
from typing import Optional, List

import arrow
from arrow import Arrow

from bug_killer_schemas.entities.bug import Bug
from bug_killer_schemas.entities.project import Project
from bug_killer_schemas.test.doubles.default_values import mock_project_title, mock_project_description, \
    mock_manager_id, mock_project_tags, mock_team_member_id
from bug_killer_schemas.test.doubles.models.bug import create_test_bug


def create_test_project(
        project_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        manager: Optional[str] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        tags: Optional[List[str]] = None,
        members: Optional[List[str]] = None,
        bugs: Optional[List[Bug]] = None

) -> Project:
    dt = arrow.utcnow().floor('second')
    return Project(
        id=project_id or str(uuid.uuid4()),
        title=title or mock_project_title,
        description=description or mock_project_description,
        manager=manager or mock_manager_id,
        created_on=created_on or dt,
        last_updated_on=last_updated_on or dt,
        tags=tags or mock_project_tags,
        members=members or [mock_team_member_id],
        bugs=bugs or [create_test_bug()]
    )
