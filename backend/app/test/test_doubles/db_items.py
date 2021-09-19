from typing import Optional, Set

import arrow
from arrow import Arrow

from bug_killer.datastore.attributes.bug_resolution_map import \
    BugResolutionMapAttribute
from bug_killer.datastore.project_table.project_item import ProjectItem
from test.test_doubles.default_values import *


def create_test_project_item(
        project_id: Optional[str] = mock_project_id,
        title: Optional[str] = mock_project_title,
        description: Optional[str] = mock_project_description,
        tags: Optional[Set[str]] = mock_project_tags,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
) -> ProjectItem:
    if created_on is None:
        created_on = arrow.utcnow()

    if last_updated_on is None:
        last_updated_on = arrow.utcnow()

    return ProjectItem(
        project_id=project_id,
        project_bug_manager_member_id=ProjectItem.PROJECT_SK_PREFIX + project_id,
        title=title,
        description=description,
        created_on=created_on,
        last_updated_on=last_updated_on,
        tags=tags,
    )


def create_test_manager_item(
        project_id: Optional[str] = mock_project_id,
        manager_id: Optional[str] = mock_manager_id,
) -> ProjectItem:
    return _create_test_project_member(
        project_id, manager_id, ProjectItem.MANAGER_SK_PREFIX
    )


def create_test_member_item(
        project_id: Optional[str] = mock_project_id,
        member_id: Optional[str] = mock_team_member_id,
) -> ProjectItem:
    return _create_test_project_member(
        project_id, member_id, ProjectItem.MEMBER_SK_PREFIX
    )


def create_test_bug_resolution(
        resolver_id: Optional[str] = mock_team_member_id,
        resolved_on: Optional[Arrow] = None,
) -> BugResolutionMapAttribute:
    if resolved_on is None:
        resolved_on = arrow.utcnow()

    return BugResolutionMapAttribute(resolver_id=resolver_id, resolved_on=resolved_on)


def create_test_bug_item(
        bug_id: str = mock_bug_id,
        title: str = mock_bug_title,
        description: str = mock_bug_description,
        tags: Set[str] = mock_bug_tags,
        bug_resolution: BugResolutionMapAttribute = create_test_bug_resolution(),
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
) -> ProjectItem:
    if created_on is None:
        created_on = arrow.utcnow()

    if last_updated_on is None:
        last_updated_on = arrow.utcnow()

    return ProjectItem(
        hash_key=bug_id,
        range_key=ProjectItem.BUG_SK_PREFIX + bug_id,
        title=title,
        description=description,
        created_on=created_on,
        last_updated_on=last_updated_on,
        tags=tags,
        bug_resolution=bug_resolution,
    )


def _create_test_project_member(
        project_id: str, user_id: str, user_type_prefix: str
) -> ProjectItem:
    return ProjectItem(
        project_id=project_id,
        project_bug_manager_member_id=user_type_prefix + user_id,
    )
