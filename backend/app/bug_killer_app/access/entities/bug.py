import logging
from typing import Tuple

import arrow

from bug_killer_app.access.datastore.bug import create_bug_item, resolve_bug_item, get_bug_item_by_id, \
    update_bug_item
from bug_killer_app.access.entities.permission import assert_user_has_project_manager_access, \
    assert_user_has_project_member_access
from bug_killer_app.access.entities.project import get_project
from bug_killer_app.domain.exceptions import EmptyUpdateException, AlreadyResolvedBugException
from bug_killer_app.models.bug import BkAppBug
from bug_killer_app.models.bug_resolution import BkAppBugResolution
from bug_killer_schemas.request.bug import CreateBugPayload
from bug_killer_schemas.request.project import UpdateProjectPayload
from bug_killer_utils.collections import is_dict_empty


async def get_bug(user_id: str, bug_id: str) -> Tuple[str, BkAppBug]:
    bug_item = await get_bug_item_by_id(bug_id)

    project = await get_project(bug_item.project_id)
    assert_user_has_project_member_access(user_id, project)

    return project.id, BkAppBug.from_db_item(bug_item)


async def create_project_bug(user_id: str, payload: CreateBugPayload) -> BkAppBug:
    logging.info(f"Creating project bug with {payload = }")

    project = await get_project(payload.project_id)
    assert_user_has_project_manager_access(user_id, project)

    bug_item = await create_bug_item(payload)
    return BkAppBug.from_db_item(bug_item)


async def update_project_bug(user_id: str, bug_id: str, payload: UpdateProjectPayload) -> Tuple[str, BkAppBug]:
    logging.info(f'Updating bug {bug_id} with {payload = }')

    if is_dict_empty(payload.to_dict()):
        raise EmptyUpdateException()

    project_id, bug = await get_bug(user_id, bug_id)

    bug_item = await update_bug_item(bug.to_db_item(project_id), payload)
    return bug_item.project_id, BkAppBug.from_db_item(bug_item)


async def resolve_project_bug(user_id: str, bug_id: str) -> Tuple[str, BkAppBug]:
    logging.info(f'User {user_id} resolving Bug {bug_id}')
    resolution = BkAppBugResolution(
        resolver_id=user_id,
        resolved_on=arrow.utcnow()
    )

    project_id, bug = await get_bug(user_id, bug_id)
    if bug.resolved:
        raise AlreadyResolvedBugException(bug.id, bug.resolved)

    bug_item = await resolve_bug_item(bug.to_db_item(project_id), resolution.to_db_attribute())

    return bug_item.project_id, BkAppBug.from_db_item(bug_item)


async def delete_project_bug(user_id: str, bug_id: str) -> Tuple[str, BkAppBug]:
    logging.info(f"Deleting project bug {user_id = } {bug_id = }")

    project_id, bug = await get_bug(user_id, bug_id)

    bug_item = bug.to_db_item(project_id)

    bug_item.delete()
    return project_id, bug
