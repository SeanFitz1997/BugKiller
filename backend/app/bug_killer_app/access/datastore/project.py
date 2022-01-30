import asyncio
import logging
import uuid
from typing import List, Tuple, NoReturn

import arrow
from pynamodb.connection import Connection
from pynamodb.transactions import TransactWrite

from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.domain.enviorment import DdbVariables
from bug_killer_app.domain.exceptions import MultipleProjectMatchException, ProjectNotFoundException, \
    ManagerNotFoundException, MultipleManagerMatchException
from bug_killer_app.domain.types import AllProjectItems
from bug_killer_schemas.request.project import CreateProjectPayload
from bug_killer_utils.collections import flatten


async def get_user_association_items(user_id: str) -> Tuple[List[ProjectItem], List[ProjectItem]]:
    logging.info(f"Getting user {user_id} project association items")
    manager_items, member_items = await asyncio.gather(
        _get_user_project_association_items(ProjectAssociationPrefix.MANAGER.value + user_id),
        _get_user_project_association_items(ProjectAssociationPrefix.MEMBER.value + user_id)
    )
    logging.info(f'Got association items {manager_items = } {member_items = }')
    return manager_items, member_items


async def _get_user_project_association_items(hk: str) -> List[ProjectItem]:
    logging.info(f"Getting user project association items by HK: {hk}")
    association_items = list(ProjectItem.user_project_index.query(hash_key=hk))
    logging.info(f"Got {association_items = }")
    return association_items


async def get_all_project_items(project_id: str) -> AllProjectItems:
    logging.info(f"Getting all project items with HK: {project_id}")
    items = list(ProjectItem.query(project_id))
    logging.info(f"Got project {items = }")
    return group_project_items(project_id, items)


def group_project_items(project_id: str, items: List[ProjectItem]) -> AllProjectItems:
    project_item, manager_item, member_items, bug_items = None, None, [], []

    # Group items
    for item in items:
        sk = item.project_association

        if sk.startswith(ProjectAssociationPrefix.PROJECT.value):
            if project_item:
                # Assert only one project item
                raise MultipleProjectMatchException(project_item.project_id)
            project_item = item

        elif sk.startswith(ProjectAssociationPrefix.MANAGER.value):
            if manager_item:
                raise MultipleManagerMatchException()
            manager_item = item

        elif sk.startswith(ProjectAssociationPrefix.MEMBER.value):
            member_items.append(item)

        elif sk.startswith(ProjectAssociationPrefix.BUG.value):
            bug_items.append(item)

    # Assert project has required items
    if not project_item:
        raise ProjectNotFoundException(project_id)
    if not manager_item:
        raise ManagerNotFoundException(project_id)

    logging.info(f"Grouped items: {project_item = }, {manager_item = }, {member_items = }, {bug_items = }")
    return project_item, manager_item, member_items, bug_items


async def create_project_items(
        manager_id: str,
        payload: CreateProjectPayload
) -> Tuple[ProjectItem, ProjectItem, List[ProjectItem]]:
    project_id = str(uuid.uuid4())
    now = arrow.utcnow()

    project_item = ProjectItem(
        project_id=project_id,
        project_association=ProjectAssociationPrefix.PROJECT.value + project_id,
        title=payload.title,
        description=payload.description,
        tags=payload.tags,
        created_on=now,
        last_updated_on=now,
    )

    manager_item = ProjectItem(project_id, ProjectAssociationPrefix.MANAGER.value + manager_id)
    member_items = [
        ProjectItem(project_id, ProjectAssociationPrefix.MEMBER.value + member)
        for member in payload.members
    ]

    await _create_project_items(project_item, manager_item, member_items, [])

    return project_item, manager_item, member_items


async def _create_project_items(*project_items: AllProjectItems) -> NoReturn:
    project_item, manager_item, member_items, _ = project_items
    with TransactWrite(connection=Connection(region=DdbVariables.TABLE_REGION)) as transaction:
        logging.info(f'Transaction Write {project_item = } {manager_item = } {member_items = }')
        transaction.save(project_item)
        manager_item.save()
        [transaction.save(item) for item in member_items]


def update_project_items(project_item: ProjectItem, update_items: List[ProjectItem]) -> NoReturn:
    project_item.last_updated_on = arrow.utcnow()
    # Ensure that project item in updated too
    update_items = set(update_items + [project_item])
    with TransactWrite(connection=Connection(region=DdbVariables.TABLE_REGION)) as transaction:
        logging.info(f'Transaction Update {update_items = }')
        [transaction.save(item) for item in update_items]


async def delete_project_items(project_items: AllProjectItems) -> NoReturn:
    project_item, manager_item, member_items, bugs_items = project_items
    with TransactWrite(connection=Connection(region=DdbVariables.TABLE_REGION)) as transaction:
        logging.info(f'Transaction Delete {project_item = } {manager_item = } {member_items = } {bugs_items = }')
        [transaction.delete(item) for item in flatten(project_items)]
