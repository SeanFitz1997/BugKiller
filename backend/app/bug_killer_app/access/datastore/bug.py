import logging
import uuid

import arrow

from bug_killer_api_interface.schemas.request.bug import CreateBugPayload, UpdateBugPayload
from bug_killer_app.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.domain.exceptions import NoChangesInUpdateException, BugNotFoundException, MultipleBugMatchException


async def get_bug_item_by_id(bug_id: str) -> ProjectItem:
    hk = ProjectAssociationPrefix.BUG.value + bug_id
    logging.info(f'Getting bug db item by {hk = }')

    bug_items = list(ProjectItem.user_project_index.query(hk))

    if not bug_items:
        raise BugNotFoundException(bug_id)
    if len(bug_items) > 1:
        raise MultipleBugMatchException(bug_id, len(bug_items))
    return bug_items[0]


async def create_bug_item(payload: CreateBugPayload) -> ProjectItem:
    bug_id = str(uuid.uuid4())
    now = arrow.utcnow()

    bug_item = ProjectItem(
        project_id=payload.project_id,
        project_association=ProjectAssociationPrefix.BUG.value + bug_id,
        title=payload.title,
        description=payload.description,
        tags=payload.tags,
        created_on=now,
        last_updated_on=now,
    )

    logging.info(f'Creating {bug_item = }')
    bug_item.save()

    return bug_item


async def update_bug_item(bug_item: ProjectItem, payload: UpdateBugPayload) -> ProjectItem:
    has_item_updated = False

    if payload.title and payload.title != bug_item.title:
        has_item_updated = True
        bug_item.title = payload.title

    if payload.description and payload.description != bug_item.description:
        has_item_updated = True
        bug_item.description = payload.description

    if payload.tags and payload.tags != bug_item.tags:
        has_item_updated = True
        bug_item.tags = set(payload.tags)

    if has_item_updated:
        bug_item.save()
    else:
        raise NoChangesInUpdateException()

    return bug_item


async def resolve_bug_item(bug_item: ProjectItem, resolution: BugResolutionMapAttribute) -> ProjectItem:
    bug_item.bug_resolution = resolution

    logging.info(f'Resolving {bug_item = }')
    bug_item.save()

    return bug_item
