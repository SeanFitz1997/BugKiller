import uuid
from typing import List, Optional

import arrow
from arrow import Arrow

from bug_killer_app.models.bug import Bug, BkAppBug
from bug_killer_app.models.bug_resolution import BkAppBugResolution
from bug_killer_app.models.project import BkAppProject
from bug_killer_app.test.test_doubles.default_values import mock_member_id, mock_project_title, \
    mock_project_description, mock_project_tags, mock_manager_id, mock_bug_title, mock_bug_description, mock_bug_tags, \
    mock_user_id


def create_test_project(
        project_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        manager: Optional[str] = None,
        members: Optional[List[str]] = None,
        bugs: Optional[List[Bug]] = None,
) -> BkAppProject:
    now = arrow.utcnow()
    return BkAppProject(
        id=project_id or str(uuid.uuid4()),
        title=title or mock_project_title,
        description=description or mock_project_description,
        tags=tags or mock_project_tags,
        created_on=created_on or now,
        last_updated_on=last_updated_on or now,
        manager=manager or mock_manager_id,
        members=members or [mock_member_id],
        bugs=bugs or [create_test_bug()],
    )


def create_test_bug(
        bug_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        resolved: Optional[BkAppBugResolution] = None,
) -> BkAppBug:
    now = arrow.utcnow()
    return BkAppBug(
        id=bug_id or str(uuid.uuid4()),
        title=title or mock_bug_title,
        description=description or mock_bug_description,
        tags=tags or mock_bug_tags,
        created_on=created_on or now,
        last_updated_on=last_updated_on or now,
        resolved=resolved,
    )


def create_test_bug_resolution(
        resolver_id: Optional[str] = None,
        resolved_on: Optional[Arrow] = None
) -> BkAppBugResolution:
    return BkAppBugResolution(resolver_id=resolver_id or mock_user_id, resolved_on=resolved_on or arrow.utcnow())
