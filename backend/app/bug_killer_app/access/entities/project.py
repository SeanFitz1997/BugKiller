import asyncio
import logging
from typing import List, Tuple

from bug_killer_app.access.datastore.project import get_user_association_items, create_project_items, \
    update_project_items, delete_project_items, get_all_project_items
from bug_killer_app.access.entities.permission import assert_user_has_project_manager_access
from bug_killer_app.datastore.project_table.project_item import ProjectItem, ProjectAssociationPrefix
from bug_killer_app.domain.exceptions import EmptyUpdateException, NoChangesInUpdateException
from bug_killer_app.domain.types import AllProjectItems
from bug_killer_app.models.project import BkAppProject
from bug_killer_schemas.request.project import UpdateProjectPayload, CreateProjectPayload
from bug_killer_utils.collections import is_dict_empty
from bug_killer_utils.strings import remove_prefix


async def get_users_projects(user_id: str) -> Tuple[List[BkAppProject], List[BkAppProject]]:
    logging.info(f'Getting the projects user {user_id} is a member or manager of')

    # Get users project ids
    manager_association_items, member_association_items = await get_user_association_items(user_id)
    manager_project_ids = set([item.project_id for item in manager_association_items])
    member_project_ids = set([item.project_id for item in member_association_items])

    # Get Projects
    projects = await asyncio.gather(
        *[get_project(project_id) for project_id in manager_project_ids | member_project_ids]
    )
    manager_projects = projects[:len(manager_project_ids)]
    member_projects = projects[len(manager_project_ids):]

    return manager_projects, member_projects


async def get_project(project_id: str) -> BkAppProject:
    logging.info(f'Getting project by id: {project_id}')
    project_items = await get_all_project_items(project_id)
    return BkAppProject.from_db_items(*project_items)


async def create_project(manager_id: str, payload: CreateProjectPayload) -> BkAppProject:
    logging.info(f"Creating project with {manager_id = } {payload = }")
    project_item, manager_item, member_items = await create_project_items(manager_id, payload)

    project = BkAppProject.from_db_items(
        project_item,
        manager_item=manager_item,
        member_items=member_items,
        bug_items=[]
    )

    logging.info(f'Created {project = }')
    return project


async def update_project(user_id: str, project_id: str, payload: UpdateProjectPayload) -> BkAppProject:
    logging.info(f"Updating project with {user_id = } {project_id = } {payload = }")

    if is_dict_empty(payload.to_dict()):
        raise EmptyUpdateException()

    project = await get_project(project_id)
    assert_user_has_project_manager_access(user_id, project)

    project_items = project.to_db_items()
    items_to_update = _get_project_items_to_update(payload, project_items)
    if not items_to_update:
        raise NoChangesInUpdateException()

    project_item = project_items[0]
    update_project_items(project_item, items_to_update)

    project = BkAppProject.from_db_items(*project_items)
    return project


def _get_project_items_to_update(
        payload: UpdateProjectPayload,
        project_items: AllProjectItems
) -> List[ProjectItem]:
    project_item, manager_item, _, _ = project_items
    manager = remove_prefix(ProjectAssociationPrefix.MANAGER.value, manager_item.project_association)

    items_to_update = []
    if (payload.title and payload.title != project_item.title) or \
            (payload.description and payload.description != project_item.description):
        logging.info("Updating project title and/or description")
        project_item.title = payload.title if payload.title else project_item.title
        project_item.description = payload.description if payload.description else project_item.description
        items_to_update.append(project_item)

    if payload.manager and payload.manager != manager:
        logging.info("Updating project manager")
        manager_item.project_association = ProjectAssociationPrefix.MANAGER.value + payload.manager
        items_to_update.append(manager_item)

    return items_to_update


async def delete_project(user_id: str, project_id: str) -> BkAppProject:
    logging.info(f"Deleting project with {user_id = } {project_id = }")
    project = await get_project(project_id)

    assert_user_has_project_manager_access(user_id, project)

    logging.info(f"Deleting {project = }")
    await delete_project_items(project.to_db_items())

    return project
