from typing import Optional, List

from bug_killer_schemas.request.project import CreateProjectPayload
from bug_killer_schemas.test.doubles.default_values import mock_project_title, mock_project_description, \
    mock_team_member_id, mock_project_tags


def create_test_create_project_payload(
        title: Optional[str] = None,
        description: Optional[str] = None,
        members: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
) -> CreateProjectPayload:
    return CreateProjectPayload(
        title=title or mock_project_title,
        description=description or mock_project_description,
        members=members or [mock_team_member_id],
        tags=tags or mock_project_tags
    )
