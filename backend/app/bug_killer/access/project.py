import logging
from typing import Optional

from pynamodb.exceptions import DoesNotExist

from bug_killer.access.bug import get_bugs_by_project_id
from bug_killer.datastore.project_item import get_project_item_by_id
from bug_killer.models.project import Project


def get_project_by_id(
        project_id: str,
        with_manager: bool = False,
        with_team: bool = False,
        with_bugs: bool = False
) -> Optional[Project]:
    try:
        logging.info(f'Getting project by id: {project_id}. {with_manager = }, {with_team = }, {with_bugs = }')
        project_db_item = get_project_item_by_id(project_id)
        project = Project.from_db_item(project_db_item)

        if with_bugs:
            logging.info(f'Adding bug details to project {project.id}')
            project.bugs = get_bugs_by_project_id(project.id)

        return project

    except DoesNotExist:
        logging.warning(f'Could not find project with id: f{project_id}')
        return None
