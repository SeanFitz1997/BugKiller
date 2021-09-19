import logging
import uuid
from functools import partial
from typing import List, Sequence, Tuple

import arrow

from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.domain.exceptions import ProjectNotFoundException
from bug_killer.models.dto.bug import DeleteBugPayload
from bug_killer.models.dto.project import CreateProjectPayload
from bug_killer.util.collections import flatten
from bug_killer.util.concurrency import run_concurrently
from bug_killer.util.type_util import AllProjectItems


def get_user_project_items(user_id: str) -> Tuple[List[ProjectItem], List[ProjectItem]]:
    manager_items, member_items = get_user_association_items(user_id)

    manager_project_ids = set([item.project_id for item in manager_items])
    member_project_ids = set([item.project_id for item in member_items])

    results, _ = run_concurrently(
        partial(get_project_items_by_ids, manager_project_ids),
        partial(get_project_items_by_ids, member_project_ids),
    )
    manager_project_items, member_project_items = results

    logging.info(f"Got manager project items {manager_project_items}")
    logging.info(f"Got member project items {member_project_items}")
    return manager_project_items, member_project_items


def get_user_association_items(user_id: str) -> Tuple[List[ProjectItem], List[ProjectItem]]:
    logging.info(f"Getting user {user_id} project association items")
    results, _ = run_concurrently(
        partial(_get_user_project_association_items, ProjectItem.MANAGER_SK_PREFIX + user_id),
        partial(_get_user_project_association_items, ProjectItem.MEMBER_SK_PREFIX + user_id),
    )
    manager_items, member_items = results
    return manager_items, member_items


def _get_user_project_association_items(hk: str) -> List[ProjectItem]:
    logging.info(f"Getting user project association items by HK: {hk}")
    association_items = list(ProjectItem.user_project_index.query(hash_key=hk))
    logging.info(f"Got {association_items =}")
    return association_items


def get_project_items_by_ids(project_ids: Sequence[str]) -> List[ProjectItem]:
    logging.info(f"Getting project items by ids: {project_ids}")
    project_look_ups = [(id, ProjectItem.PROJECT_SK_PREFIX + id) for id in project_ids]
    projects = list(ProjectItem.batch_get(project_look_ups))
    logging.info(f"Got project items {projects}")
    return projects


def create_bug_item(payload: CreateProjectPayload) -> ProjectItem:
    bug_id = str(uuid.uuid4())
    now = arrow.utcnow()
    bug_item = ProjectItem(
        project_id=payload.project_id,
        project_bug_manager_member_id=ProjectItem.BUG_SK_PREFIX + bug_id,
        title=payload.title,
        description=payload.description,
        tags=payload.tags,
        created_on=now,
        last_updated_on=now,
    )
    logging.info(f"Creating {bug_item =}")
    bug_item.save()
    return bug_item


def create_project_items(payload: CreateProjectPayload) -> Tuple[ProjectItem, ProjectItem, List[ProjectItem]]:
    project_id = str(uuid.uuid4())
    now = arrow.utcnow()
    tags = payload.tags or set()
    project_item = ProjectItem(
        project_id=project_id,
        project_bug_manager_member_id=ProjectItem.PROJECT_SK_PREFIX + project_id,
        title=payload.title,
        description=payload.description,
        tags=tags,
        created_on=now,
        last_updated_on=now,
    )
    manager_item = ProjectItem(project_id, ProjectItem.MANAGER_SK_PREFIX + payload.manager)
    member_items = [
        ProjectItem(project_id, ProjectItem.MEMBER_SK_PREFIX + member)
        for member in payload.members
    ]

    logging.info(f"Creating project: {project_id} with items {project_item =}, {manager_item =}, {member_items =}")
    with ProjectItem.batch_write() as batch:
        [batch.save(item) for item in flatten([project_item, manager_item, member_items])]

    return project_item, manager_item, member_items


def delete_bug_item(payload: DeleteBugPayload) -> ProjectItem:
    bug_item = get_bug_item_by_project_bug_id(payload.project_id, payload.bug_id)
    logging.info(f"Deleting {bug_item =}")
    bug_item.delete()
    return bug_item


def get_all_project_items(project_id: str) -> AllProjectItems:
    logging.info(f"Getting all project items with HK: {project_id}")
    items = ProjectItem.query(project_id)
    logging.info(f"Got project items {items}")

    if not items:
        raise ProjectNotFoundException(project_id)

    return group_project_items(items)


def bulk_get_all_project_items(project_ids: List[str]) -> List[AllProjectItems]:
    logging.info(f'Getting all projects items concurrently for {project_ids}')
    projects_items, time_taken = run_concurrently(
        *[partial(get_all_project_items, project_id) for project_id in project_ids]
    )
    logging.info(f'Got all items for projects in {time_taken} ms')
    return projects_items


def group_project_items(items: List[ProjectItem]) -> AllProjectItems:
    project_item = None
    manager_item = None
    member_items = []
    bug_items = []

    for item in items:
        sk = item.project_bug_manager_member_id
        if sk.startswith(ProjectItem.PROJECT_SK_PREFIX):
            project_item = item
        elif sk.startswith(ProjectItem.MANAGER_SK_PREFIX):
            manager_item = item
        elif sk.startswith(ProjectItem.MEMBER_SK_PREFIX):
            member_items.append(item)
        elif sk.startswith(ProjectItem.BUG_SK_PREFIX):
            bug_items.append(item)

    logging.info(f"Grouped items: {project_item=}, {manager_item=}, {member_items=}, {bug_items=}")
    return project_item, manager_item, member_items, bug_items


def get_bug_item_by_project_bug_id(project_id: str, bug_id: str) -> ProjectItem:
    sort_key = ProjectItem.BUG_SK_PREFIX + bug_id
    logging.info(f"Getting bug db items by HK: {project_id}, SK: {sort_key}")
    bug_item = ProjectItem.get(project_id, sort_key)
    logging.info(f"Got bug item {bug_item}")
    return bug_item
