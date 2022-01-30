from typing import Optional, Set, List

import arrow
from arrow import Arrow

from bug_killer_app.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.test.test_doubles.default_values import mock_project_title, mock_project_description, \
    mock_bug_tags, mock_manager_id, mock_user_id, mock_bug_title, mock_member_id


def create_test_project_item(
        project_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[Set[str]] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
) -> ProjectItem:
    now = arrow.utcnow()
    return ProjectItem(
        project_id=project_id,
        project_association=ProjectAssociationPrefix.PROJECT.value + project_id,
        title=title or mock_project_title,
        description=description or mock_project_description,
        created_on=created_on or now,
        last_updated_on=last_updated_on or now,
        tags=tags or mock_bug_tags,
    )


def create_test_bug_item(
        project_id: str,
        bug_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        bug_resolution: Optional[BugResolutionMapAttribute] = None,
) -> ProjectItem:
    now = arrow.utcnow()
    return ProjectItem(
        project_id=project_id,
        project_association=ProjectAssociationPrefix.BUG.value + bug_id,
        title=title or mock_bug_title,
        description=description or mock_project_description,
        created_on=created_on or now,
        last_updated_on=last_updated_on or now,
        tags=tags or mock_bug_tags,
        bug_resolution=bug_resolution,
    )


def create_test_bug_resolution_attribute(
        resolver_id: Optional[str] = None,
        resolved_on: Optional[Arrow] = None
) -> BugResolutionMapAttribute:
    return BugResolutionMapAttribute(
        resolver_id=resolver_id or mock_user_id,
        resolved_on=resolved_on or arrow.utcnow()
    )


def create_test_manager_item(project_id: str, manager_id: Optional[str] = None) -> ProjectItem:
    return _create_test_project_member(
        project_id, manager_id or mock_manager_id, ProjectAssociationPrefix.MANAGER)


def create_test_member_item(project_id: str, member_id: Optional[str] = None) -> ProjectItem:
    return _create_test_project_member(
        project_id, member_id or mock_member_id, ProjectAssociationPrefix.MEMBER)


def _create_test_project_member(
        project_id: str,
        user_id: str,
        user_type_prefix: ProjectAssociationPrefix) -> ProjectItem:
    return ProjectItem(
        project_id=project_id,
        project_association=user_type_prefix.value + user_id,
    )
