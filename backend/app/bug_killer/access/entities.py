import logging
from typing import List, NoReturn, Tuple

import arrow
from pynamodb.exceptions import DoesNotExist

from bug_killer.access.project_item import create_bug_item, delete_bug_item
from bug_killer.access.project_item import (
    create_project_items,
    get_all_project_items,
    get_user_project_items,
    bulk_get_all_project_items
)
from bug_killer.datastore.project_table.project_item import ProjectItem
from bug_killer.domain.exceptions import (
    UnauthorizedProjectAccessException,
    ProjectNotFoundException,
    BugNotFoundException
)
from bug_killer.models.dto.bug import CreateBugPayload, DeleteBugPayload
from bug_killer.models.dto.project import (
    CreateProjectPayload,
    UpdateProjectPayload,
    DeleteProjectPayload
)
from bug_killer.models.entities.bug import Bug
from bug_killer.models.entities.project import Project
from bug_killer.util.collections import flatten
from bug_killer.util.entity import remove_prefix, sort_by_create_date


def check_actor_can_access_project(actor: str, project: Project) -> NoReturn:
    if actor != project.manager and actor not in project.members:
        raise UnauthorizedProjectAccessException(actor, project.id)


def get_project(project_id: str) -> Project:
    logging.info(f'Getting project with id: {project_id}')
    project_items = get_all_project_items(project_id)

    project_item, _, _, _ = project_items
    if not project_item:
        raise ProjectNotFoundException(project_id)

    return Project.from_db_items(*project_items)


def get_users_projects(user_id: str) -> Tuple[List[Project], List[Project]]:
    logging.info(f'Getting the projects user {user_id} is a member or manager of')
    manager_project_items, member_project_items = get_user_project_items(user_id)

    all_projects_items = bulk_get_all_project_items(
        [item.project_id for item in manager_project_items + member_project_items]
    )
    all_projects = [Project.from_db_items(*items) for items in all_projects_items]
    manager_projects = all_projects[:len(manager_project_items)]
    member_projects = all_projects[len(manager_project_items):]

    sort_by_create_date(manager_projects)
    sort_by_create_date(member_projects)
    return manager_projects, member_projects


def create_project(payload: CreateProjectPayload) -> Project:
    logging.info(f"Creating project with {payload =}")
    project_item, manager_item, member_items = create_project_items(payload)
    return Project.from_db_items(
        project_item,
        manager_item=manager_item,
        member_items=member_items,
        bug_items=[]
    )


def update_project(payload: UpdateProjectPayload) -> Project:
    logging.info(f"Updating project with {payload =}")
    project_item, manager_item, member_items, bug_items = get_all_project_items(payload.project_id)

    if not project_item:
        raise ProjectNotFoundException(payload.project_id)

    manager = remove_prefix(ProjectItem.MANAGER_SK_PREFIX, manager_item.project_bug_manager_member_id)
    if payload.actor != manager:
        raise UnauthorizedProjectAccessException(payload.actor, project_item.project_id)

    items_to_update = []
    if payload.title or payload.description:
        logging.info("Updating project title and/or description")
        project_item.title = payload.title if payload.title else project_item.title
        project_item.description = payload.description if payload.description else project_item.description
        items_to_update.append(project_item)

    if payload.manager:
        logging.info("Updating project manager")
        manager_item.project_bug_manager_member_id = ProjectItem.MANAGER_SK_PREFIX + payload.manager
        items_to_update.append(manager_item)

    logging.info(f"Batch writing items {items_to_update}")
    if items_to_update:
        project_item.last_updated_on = arrow.utcnow()
        with ProjectItem.batch_write() as batch:
            for item in items_to_update:
                batch.save(item)

    project = Project.from_db_items(project_item, manager_item, member_items, bug_items)
    return project


def delete_project(payload: DeleteProjectPayload) -> Project:
    logging.info(f"Deleting project with {payload =}")
    project = get_project(payload.project_id)
    if project.manager != payload.actor:
        raise UnauthorizedProjectAccessException(payload.actor, project.id)

    logging.info(f"Deleting {project =}")
    with ProjectItem.batch_write() as batch:
        [batch.delete(item) for item in flatten([project.to_db_items()]) if item is not None]

    return project


def create_project_bug(payload: CreateBugPayload) -> Bug:
    logging.info(f"Creating project bug with {payload =}")
    project = get_project(payload.project_id)
    check_actor_can_access_project(payload.actor, project)
    bug_item = create_bug_item(payload)
    return Bug.from_db_item(bug_item)


def delete_project_bug(payload: DeleteBugPayload) -> Bug:
    logging.info(f"Deleting project bug with {payload =}")
    project = get_project(payload.project_id)
    check_actor_can_access_project(payload.actor, project)

    try:
        bug_item = delete_bug_item(payload)
        return Bug.from_db_item(bug_item)
    except DoesNotExist:
        raise BugNotFoundException(payload.bug_id)
