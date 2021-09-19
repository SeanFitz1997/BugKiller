import uuid
from typing import List, Optional, Set

from arrow import Arrow

from bug_killer.models.entities.bug import Bug
from bug_killer.models.entities.bug_resolution import BugResolution
from bug_killer.models.entities.project import Project
from bug_killer.models.entities.user import User
from test.test_doubles.default_values import *


def create_test_user(
        user_id: str = mock_user_id,
        first_name: str = mock_fist_name,
        last_name: str = mock_last_name,
        email: str = mock_email,
) -> User:
    return User(id=user_id, first_name=first_name, last_name=last_name, email=email)


def create_test_manager(
        user_id: str = mock_manager_id,
        first_name: str = mock_fist_name,
        last_name: str = mock_last_name,
        email: str = mock_email,
) -> User:
    return create_test_user(user_id, first_name, last_name, email)


def create_test_member(
        user_id: str = mock_team_member_id,
        first_name: str = mock_fist_name,
        last_name: str = mock_last_name,
        email: str = mock_email,
) -> User:
    return create_test_user(user_id, first_name, last_name, email)


def create_test_bug(
        bug_id: Optional[str] = None,
        title: str = mock_bug_title,
        description: str = mock_bug_description,
        tags: Set[str] = mock_bug_tags,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        resolved: Optional[BugResolution] = None,
) -> Bug:
    bug_id = bug_id or str(uuid.uuid4())
    created_on = created_on or Arrow.utcnow()
    last_updated_on = last_updated_on or Arrow.utcnow()

    return Bug(
        id=bug_id,
        title=title,
        description=description,
        tags=tags,
        created_on=created_on,
        last_updated_on=last_updated_on,
        resolved=resolved,
    )


def create_test_resolution(
        resolver_id: str = mock_team_member_id,
        resolved_on: Optional[Arrow] = None
) -> BugResolution:
    resolved_on = resolved_on or Arrow.utcnow()
    return BugResolution(resolver_id=resolver_id, resolved_on=resolved_on)


def create_test_project(
        project_id: Optional[str] = None,
        title: Optional[str] = mock_bug_title,
        description: Optional[str] = mock_bug_description,
        tags: Optional[Set[str]] = mock_bug_tags,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        manager: Optional[str] = create_test_manager().id,
        members: Optional[List[str]] = [create_test_user().id],
        bugs: Optional[List[Bug]] = [create_test_bug()],
) -> Project:
    project_id = project_id or str(uuid.uuid4())
    created_on = created_on or Arrow.utcnow()
    last_updated_on = last_updated_on or Arrow.utcnow()

    return Project(
        id=project_id,
        title=title,
        description=description,
        tags=tags,
        created_on=created_on,
        last_updated_on=last_updated_on,
        manager=manager,
        members=members,
        bugs=bugs,
    )
