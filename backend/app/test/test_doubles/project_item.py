from datetime import datetime
from typing import Optional, Set

from bug_killer.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer.datastore.project_item import ProjectItem


def create_test_project_item(
        project_id: Optional[str] = '123',
        manager_id: Optional[str] = 'm1',
        title: Optional[str] = 'test project',
        description: Optional[str] = 'this is a test project',
        created_on: Optional[datetime] = None,
        last_updated_on: Optional[datetime] = None,
        tags: Optional[Set[str]] = set(['test'])
) -> ProjectItem:
    if created_on is None:
        created_on = datetime.now()

    if last_updated_on is None:
        last_updated_on = datetime.now()

    return ProjectItem(
        hash_key=project_id,
        range_key=ProjectItem.PROJECT_SK_PREFIX + project_id,
        project_manager_id=manager_id,
        title=title,
        description=description,
        created_on=created_on,
        last_updated_on=last_updated_on,
        tags=tags
    )


def create_test_bug_item(
        bug_id: Optional[str] = 'abc',
        title: Optional[str] = 'test',
        description: Optional[str] = 'this is a test bug',
        created_on: Optional[datetime] = None,
        last_updated_on: Optional[datetime] = None,
        tags: Optional[Set[str]] = set(['test']),
        bug_resolution: Optional[BugResolutionMapAttribute] = None
):
    if created_on is None:
        created_on = datetime.now()

    if last_updated_on is None:
        last_updated_on = datetime.now()

    return ProjectItem(
        hash_key=bug_id,
        range_key=ProjectItem.BUG_SK_PREFIX + bug_id,
        title=title,
        description=description,
        created_on=created_on,
        last_updated_on=last_updated_on,
        tags=tags,
        bug_resolution=bug_resolution
    )
